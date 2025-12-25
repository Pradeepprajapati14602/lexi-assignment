"""
Chat API endpoints for conversational document drafting.
Handles template matching, Q&A flow, and draft generation.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import uuid
import re

from app.db.database import get_db
from app.db import models
from app.schemas import schemas
from app.services.template_service import template_service
from app.services.gemini_service import gemini_service
from app.services.exa_service import exa_service
from app.core.config import settings

router = APIRouter()

# Store conversation state (in production, use Redis or similar)
conversations: Dict[str, Dict[str, Any]] = {}


@router.post("/message", response_model=schemas.ChatResponse)
async def send_message(
    request: schemas.ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Process chat message and handle drafting flow.
    Supports natural language and slash commands.
    Created by UOIONHHC
    """
    message = request.message.strip()
    conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:12]}"
    
    # Initialize conversation if new
    if conversation_id not in conversations:
        conversations[conversation_id] = {
            "state": "idle",
            "template_id": None,
            "instance_id": None,
            "answers": {},
            "pending_variables": []
        }
    
    conv = conversations[conversation_id]
    
    # Handle slash commands
    if message.startswith("/draft"):
        query = message.replace("/draft", "").strip().strip('"')
        return await handle_draft_request(conversation_id, query, db)
    
    elif message.startswith("/vars"):
        return handle_vars_command(conversation_id, db)
    
    # Handle conversation states
    elif conv["state"] == "awaiting_template_selection":
        return await handle_template_selection(conversation_id, message, db)
    
    elif conv["state"] == "answering_questions":
        return await handle_answer(conversation_id, message, db)
    
    # Default: treat as draft request
    else:
        return await handle_draft_request(conversation_id, message, db)


async def handle_draft_request(
    conversation_id: str,
    query: str,
    db: Session
) -> schemas.ChatResponse:
    """Handle initial draft request"""
    
    # Simple keyword matching first (no AI needed)
    all_templates = db.query(models.Template).all()
    
    if not all_templates:
        return schemas.ChatResponse(
            conversation_id=conversation_id,
            message="❌ No templates available. Upload a document first!",
            message_type="no_templates",
            data=None
        )
    
    query_lower = query.lower()
    matched_template = None
    
    # Keyword matching
    for template in all_templates:
        title_lower = template.title.lower()
        if any(word in query_lower for word in ['lease', 'rent', 'rental']) and 'lease' in title_lower:
            matched_template = template
            break
        elif any(word in query_lower for word in ['employment', 'job', 'offer']) and any(w in title_lower for w in ['employment', 'offer']):
            matched_template = template
            break
    
    # If no keyword match, show all templates
    if not matched_template and all_templates:
        conv = conversations[conversation_id]
        conv["state"] = "awaiting_template_selection"
        conv["user_query"] = query
        
        message = "📋 **Available Templates:**\n\n"
        for i, t in enumerate(all_templates, 1):
            message += f"{i}. **{t.title}** ({len(t.variables)} variables)\n"
        message += "\nReply with the number to select a template."
        
        return schemas.ChatResponse(
            conversation_id=conversation_id,
            message=message,
            message_type="template_list",
            data={"templates": [{"id": t.id, "title": t.title} for t in all_templates]}
        )
    
    # If matched, use it
    if matched_template:
        conv = conversations[conversation_id]
        conv["state"] = "template_matched"
        conv["template_id"] = matched_template.id
        conv["user_query"] = query
        
        return schemas.ChatResponse(
            conversation_id=conversation_id,
            message=f"✅ **{matched_template.title}**\n\nFound {len(matched_template.variables)} variables.\n\nReply 'yes' to proceed!",
            message_type="template_match",
            data={"template_id": matched_template.id}
        )
    
    # Fallback: try AI matching (may fail)
    try:
        match_result = await template_service.match_template(db, query)
    
        if match_result.has_match and match_result.best_match:
            # Found a match
            conv = conversations[conversation_id]
            conv["state"] = "template_matched"
            conv["template_id"] = match_result.best_match.template_id
            conv["user_query"] = query
            
            # Build response with match card
            response_message = f"""📄 **Template Match Found**

**Best Match:** {match_result.best_match.title}
**Confidence:** {match_result.best_match.confidence:.0%}
**Why:** {match_result.best_match.justification}

"""
            
            if match_result.alternatives:
                response_message += "\n**Alternatives:**\n"
                for alt in match_result.alternatives[:2]:
                    response_message += f"- {alt.title} ({alt.confidence:.0%})\n"
            
            response_message += "\n✅ Reply with 'yes' to use this template, or select an alternative."
            
            return schemas.ChatResponse(
                conversation_id=conversation_id,
                message=response_message,
                message_type="template_match",
                data={
                    "best_match": match_result.best_match.dict(),
                    "alternatives": [alt.dict() for alt in match_result.alternatives]
                }
            )
    
    except Exception as e:
        print(f"AI matching failed: {str(e)}")
        # Fallback to showing all templates
        message = "⚠️ AI matching unavailable. **Available Templates:**\n\n"
        for i, t in enumerate(all_templates, 1):
            message += f"{i}. **{t.title}** ({len(t.variables)} variables)\n"
        message += "\nReply with the number to select."
        
        conv = conversations[conversation_id]
        conv["state"] = "awaiting_template_selection"
        conv["user_query"] = query
        
        return schemas.ChatResponse(
            conversation_id=conversation_id,
            message=message,
            message_type="template_list",
            data={"templates": [{"id": t.id, "title": t.title} for t in all_templates]}
        )
    
    # No match - check if exa.ai is available
    if exa_service.is_available():
        return await handle_web_bootstrap(conversation_id, query, db)
    else:
        return schemas.ChatResponse(
            conversation_id=conversation_id,
            message="❌ No matching template found in the database.\n\n💡 Suggestions:\n- Try uploading a similar document\n- Broaden your request\n- Use different keywords",
            message_type="no_match",
            data={"has_exa": False}
        )


async def handle_web_bootstrap(
    conversation_id: str,
    query: str,
    db: Session
) -> schemas.ChatResponse:
    """Handle web bootstrap using exa.ai (BONUS FEATURE)"""
    
    # Search web for similar templates
    results = await exa_service.search_legal_templates(query)
    
    if not results:
        return schemas.ChatResponse(
            conversation_id=conversation_id,
            message="❌ No matching template found locally or on the web.\n\nPlease try:\n- Uploading a document\n- Using different search terms",
            message_type="no_match",
            data={"has_exa": True, "web_results": 0}
        )
    
    # Show web results
    conv = conversations[conversation_id]
    conv["state"] = "web_bootstrap"
    conv["web_results"] = results
    conv["user_query"] = query
    
    response_message = f"""🌐 **No Local Template Found - Web Search Results**

I found {len(results)} similar documents online:

"""
    
    for idx, result in enumerate(results[:3], 1):
        response_message += f"""
**{idx}. {result['title']}**
URL: {result['url'][:60]}...
Preview: {result['text'][:150]}...

"""
    
    response_message += "\n✅ Reply with the number (1-3) to create a template from that document."
    
    return schemas.ChatResponse(
        conversation_id=conversation_id,
        message=response_message,
        message_type="web_results",
        data={"results": results}
    )


async def handle_template_selection(
    conversation_id: str,
    message: str,
    db: Session
) -> schemas.ChatResponse:
    """Handle template or web result selection"""
    
    conv = conversations[conversation_id]
    
    if conv.get("state") == "web_bootstrap":
        # User selected a web result
        try:
            selection = int(message.strip())
            if 1 <= selection <= len(conv["web_results"]):
                result = conv["web_results"][selection - 1]
                
                # Extract template from web document
                extraction = await template_service.extract_template_from_document(
                    result["text"],
                    result["title"]
                )
                
                # Save template
                db_template = template_service.save_template(db, extraction.template)
                
                conv["template_id"] = db_template.id
                conv["state"] = "template_matched"
                
                return schemas.ChatResponse(
                    conversation_id=conversation_id,
                    message=f"✅ Created template: **{db_template.title}**\n\nFound {len(db_template.variables)} variables. Let's fill them in!",
                    message_type="template_created",
                    data={"template_id": db_template.id}
                )
        except (ValueError, IndexError):
            pass
    
    # Default: proceed with current template
    message_lower = message.lower()
    if message_lower in ["yes", "y", "use this", "proceed", "continue"]:
        return await start_questions(conversation_id, db)
    
    # Check if it's a numeric selection
    try:
        selection = int(message.strip())
        all_templates = db.query(models.Template).all()
        if 1 <= selection <= len(all_templates):
            selected_template = all_templates[selection - 1]
            conv["template_id"] = selected_template.id
            conv["state"] = "template_matched"
            
            return schemas.ChatResponse(
                conversation_id=conversation_id,
                message=f"✅ **{selected_template.title}**\n\nFound {len(selected_template.variables)} variables.\n\nReply 'yes' to proceed!",
                message_type="template_match",
                data={"template_id": selected_template.id}
            )
    except (ValueError, IndexError):
        pass
    
    return schemas.ChatResponse(
        conversation_id=conversation_id,
        message="Please confirm by typing 'yes' or select a template by number.",
        message_type="text",
        data=None
    )


async def start_questions(
    conversation_id: str,
    db: Session
) -> schemas.ChatResponse:
    """Start asking questions for variables"""
    
    conv = conversations[conversation_id]
    template_id = conv["template_id"]
    
    template = template_service.get_template_by_id(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Pre-fill variables from user query
    user_query = conv.get("user_query", "")
    variables_data = [
        {
            "key": var.key,
            "label": var.label,
            "description": var.description,
            "example": var.example,
            "required": var.required,
            "dtype": var.dtype
        }
        for var in template.variables
    ]
    
    prefilled = gemini_service.pre_fill_variables(user_query, variables_data)
    conv["answers"] = prefilled
    
    # Generate questions for remaining variables
    remaining_vars = [var for var in variables_data if var["key"] not in prefilled]
    
    if not remaining_vars:
        # All variables pre-filled - generate draft
        return await generate_draft(conversation_id, db)
    
    # Generate human-friendly questions
    questions = gemini_service.generate_questions(remaining_vars, template.title)
    conv["pending_variables"] = questions
    conv["state"] = "answering_questions"
    
    # Create instance
    instance_id = f"inst_{uuid.uuid4().hex[:12]}"
    conv["instance_id"] = instance_id
    
    db_instance = models.Instance(
        id=instance_id,
        template_id=template_id,
        user_query=user_query,
        answers_json=prefilled
    )
    db.add(db_instance)
    db.commit()
    
    # Ask first question
    first_question = questions[0]
    response_message = f"""📝 **Let's fill in the details**

Pre-filled {len(prefilled)} variables from your request.
{len(remaining_vars)} questions remaining.

**Q1/{len(questions)}:** {first_question['question']}
"""
    
    if first_question.get('hint'):
        response_message += f"\n💡 {first_question['hint']}"
    
    return schemas.ChatResponse(
        conversation_id=conversation_id,
        message=response_message,
        message_type="question",
        data={
            "question_index": 0,
            "total_questions": len(questions),
            "variable_key": first_question['variable_key']
        }
    )


async def handle_answer(
    conversation_id: str,
    message: str,
    db: Session
) -> schemas.ChatResponse:
    """Handle answer to a variable question"""
    
    conv = conversations[conversation_id]
    questions = conv["pending_variables"]
    
    # Find current question
    answered_count = len([q for q in questions if conv["answers"].get(q["variable_key"])])
    
    if answered_count >= len(questions):
        # All answered - generate draft
        return await generate_draft(conversation_id, db)
    
    current_question = questions[answered_count]
    
    # Store answer
    conv["answers"][current_question["variable_key"]] = message.strip()
    
    # Update instance
    instance = db.query(models.Instance).filter(
        models.Instance.id == conv["instance_id"]
    ).first()
    
    if instance:
        instance.answers_json = conv["answers"]
        db.commit()
    
    # Check if done
    if answered_count + 1 >= len(questions):
        return await generate_draft(conversation_id, db)
    
    # Ask next question
    next_question = questions[answered_count + 1]
    response_message = f"""✅ Got it!

**Q{answered_count + 2}/{len(questions)}:** {next_question['question']}
"""
    
    if next_question.get('hint'):
        response_message += f"\n💡 {next_question['hint']}"
    
    return schemas.ChatResponse(
        conversation_id=conversation_id,
        message=response_message,
        message_type="question",
        data={
            "question_index": answered_count + 1,
            "total_questions": len(questions),
            "variable_key": next_question['variable_key']
        }
    )


async def generate_draft(
    conversation_id: str,
    db: Session
) -> schemas.ChatResponse:
    """Generate final draft from template and answers"""
    
    conv = conversations[conversation_id]
    template_id = conv["template_id"]
    answers = conv["answers"]
    instance_id = conv["instance_id"]
    
    template = template_service.get_template_by_id(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Replace variables in template
    draft = template.body_md
    
    for key, value in answers.items():
        pattern = f"{{{{{key}}}}}"
        draft = draft.replace(pattern, str(value))
    
    # Update instance with draft
    instance = db.query(models.Instance).filter(
        models.Instance.id == instance_id
    ).first()
    
    if instance:
        instance.draft_md = draft
        db.commit()
    
    # Reset conversation state
    conv["state"] = "draft_generated"
    
    response_message = f"""✅ **Draft Generated Successfully!**

---

{draft}

---

**Actions:**
- Copy the draft above
- Type 'download' for DOCX version
- Type 'edit' to modify variables
- Type 'new' to start a new draft
"""
    
    return schemas.ChatResponse(
        conversation_id=conversation_id,
        message=response_message,
        message_type="draft",
        data={
            "instance_id": instance_id,
            "template_id": template_id,
            "draft_md": draft
        }
    )


def handle_vars_command(
    conversation_id: str,
    db: Session
) -> schemas.ChatResponse:
    """Handle /vars command to show current variable status"""
    
    if conversation_id not in conversations:
        return schemas.ChatResponse(
            conversation_id=conversation_id,
            message="No active drafting session.",
            message_type="text",
            data=None
        )
    
    conv = conversations[conversation_id]
    template_id = conv.get("template_id")
    
    if not template_id:
        return schemas.ChatResponse(
            conversation_id=conversation_id,
            message="No template selected yet.",
            message_type="text",
            data=None
        )
    
    template = template_service.get_template_by_id(db, template_id)
    if not template:
        return schemas.ChatResponse(
            conversation_id=conversation_id,
            message="Template not found.",
            message_type="text",
            data=None
        )
    
    answers = conv.get("answers", {})
    
    filled = []
    missing = []
    
    for var in template.variables:
        if var.key in answers:
            filled.append(f"✅ {var.label}: {answers[var.key]}")
        else:
            status = "Required" if var.required else "Optional"
            missing.append(f"❌ {var.label} ({status})")
    
    message = f"""**Variable Status for {template.title}**

**Filled ({len(filled)}):**
{chr(10).join(filled) if filled else "None"}

**Missing ({len(missing)}):**
{chr(10).join(missing) if missing else "All filled!"}
"""
    
    return schemas.ChatResponse(
        conversation_id=conversation_id,
        message=message,
        message_type="vars_status",
        data={
            "filled_count": len(filled),
            "missing_count": len(missing),
            "total_count": len(template.variables)
        }
    )


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation state"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversations[conversation_id]
