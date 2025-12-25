"""
Gemini AI integration for smart prompting and extraction.
Handles variable extraction, template matching, question generation, and embeddings.
Created by UOIONHHC
"""

import google.generativeai as genai
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from app.core.config import settings
import numpy as np

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiService:
    """Service for Gemini AI operations"""
    
    def __init__(self):
        # Try gemini-pro which is the stable production model
        try:
            self.model = genai.GenerativeModel('gemini-pro')
        except:
            # Fallback to 1.5-flash
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.embedding_model = "models/embedding-001"
    
    def extract_variables_from_chunk(
        self,
        text: str,
        existing_variables: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Extract variables from a document chunk.
        Uses existing variables to prevent duplication.
        
        Args:
            text: Document text chunk
            existing_variables: Previously discovered variables
            
        Returns:
            Dict with variables and similarity_tags
        """
        
        existing_vars_str = ""
        if existing_variables:
            existing_vars_str = "\n\nPreviously discovered variables:\n" + json.dumps(
                existing_variables, indent=2
            )
        
        system_prompt = """You are a legal document templating expert. Extract reusable variables from legal documents to create templates.

CRITICAL RULES:
1. Use snake_case for all variable keys (e.g., claimant_full_name, incident_date)
2. Deduplicate logically identical fields - if a field matches existing variables, REUSE that key
3. Provide clear, professional labels and descriptions
4. Include realistic examples appropriate to the jurisdiction
5. Mark fields as required: true/false based on legal necessity
6. Suggest appropriate data types: string, number, date, enum
7. Add validation regex for structured data (dates, phone, email, policy numbers, etc.)
8. Extract similarity tags for template matching (jurisdiction, doc type, subject matter)

VARIABLE TYPES TO EXTRACT:
- Party names (individuals, companies, entities)
- Dates (incident, execution, expiry, notice)
- Amounts (claims, rents, fees, penalties)
- References (policy numbers, case numbers, registration IDs, FIR numbers)
- Addresses (registered, correspondence, property)
- Contact details (phone, email)
- Legal references (sections, acts, clauses)
- Jurisdictions (courts, forums, arbitration venues)

OUTPUT FORMAT (strict JSON only):
{
  "variables": [
    {
      "key": "variable_name_snake_case",
      "label": "Human Readable Label",
      "description": "Clear description of what this field represents",
      "example": "Realistic example value",
      "required": true,
      "dtype": "string",
      "regex": "^pattern$",
      "enum_values": null
    }
  ],
  "similarity_tags": ["jurisdiction", "doc_type", "subject", "keywords"]
}
"""
        
        user_prompt = f"""Extract variables from this legal document text:

{text}
{existing_vars_str}

IMPORTANT: 
- If existing variables match the meaning of a field in this text, REUSE that variable key
- Only create NEW variables for genuinely new fields
- Ensure all variables have clear labels, descriptions, and examples
- Return ONLY valid JSON"""
        
        try:
            response = self.model.generate_content(
                [system_prompt, user_prompt],
                generation_config={
                    "temperature": settings.GEMINI_TEMPERATURE,
                    "max_output_tokens": settings.GEMINI_MAX_TOKENS,
                }
            )
            
            result_text = response.text.strip()
            
            # Extract JSON from markdown code blocks if present
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            
            result = json.loads(result_text)
            return result
            
        except json.JSONDecodeError as e:
            print(f" JSON decode error: {e}")
            print(f" Response text (first 500 chars): {result_text[:500]}")
            return {"variables": [], "similarity_tags": []}
        except Exception as e:
            print(f" Error extracting variables: {e}")
            import traceback
            traceback.print_exc()
            return {"variables": [], "similarity_tags": []}
    
    def match_template(
        self,
        user_query: str,
        templates: List[Dict[str, Any]],
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Match user query to best template using classification.
        
        Args:
            user_query: User's drafting request
            templates: List of available templates with metadata
            top_k: Number of alternatives to return
            
        Returns:
            Dict with best_match, alternatives, and confidence
        """
        
        if not templates:
            return {
                "best_match": None,
                "alternatives": [],
                "has_match": False,
                "confidence": 0.0
            }
        
        # Prepare template context
        template_context = []
        for idx, tmpl in enumerate(templates):
            context = f"""
Template {idx + 1}:
- ID: {tmpl['id']}
- Title: {tmpl['title']}
- Description: {tmpl.get('file_description', 'N/A')}
- Document Type: {tmpl.get('doc_type', 'N/A')}
- Jurisdiction: {tmpl.get('jurisdiction', 'N/A')}
- Tags: {', '.join(tmpl.get('similarity_tags', []))}
"""
            template_context.append(context)
        
        system_prompt = """You are a legal template matching assistant. Given a user request, find the best matching template from available options.

MATCHING CRITERIA:
1. Document type similarity (notice, agreement, petition, etc.)
2. Jurisdiction match
3. Subject matter relevance
4. Purpose alignment

CONFIDENCE SCORING:
- 0.9-1.0: Exact match (same doc type, jurisdiction, subject)
- 0.7-0.9: Strong match (same doc type, similar purpose)
- 0.5-0.7: Moderate match (related doc type or subject)
- Below 0.5: Poor match (consider no match)

OUTPUT FORMAT (strict JSON):
{
  "best_match": {
    "template_id": "tpl_xxx",
    "confidence": 0.85,
    "justification": "Brief reason why this matches"
  },
  "alternatives": [
    {
      "template_id": "tpl_yyy",
      "confidence": 0.72,
      "justification": "Why this is alternative"
    }
  ]
}

IMPORTANT: If no template has confidence >= 0.6, return best_match as null."""
        
        user_prompt = f"""User request: "{user_query}"

Available templates:
{''.join(template_context)}

Return the best matching template and top alternatives with confidence scores."""
        
        try:
            response = self.model.generate_content(
                [system_prompt, user_prompt],
                generation_config={
                    "temperature": 0.2,  # Lower temperature for consistent matching
                    "max_output_tokens": 2048,
                }
            )
            
            result_text = response.text.strip()
            
            # Extract JSON
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            
            result = json.loads(result_text)
            
            # Validate and enhance result
            best_match = result.get("best_match")
            has_match = best_match is not None and best_match.get("confidence", 0) >= settings.MIN_CONFIDENCE_THRESHOLD
            
            return {
                "best_match": best_match,
                "alternatives": result.get("alternatives", [])[:top_k],
                "has_match": has_match
            }
            
        except Exception as e:
            print(f"Error matching template: {e}")
            return {
                "best_match": None,
                "alternatives": [],
                "has_match": False
            }
    
    def generate_questions(
        self,
        variables: List[Dict[str, Any]],
        template_context: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate human-friendly questions for variables.
        
        Args:
            variables: List of variable definitions
            template_context: Template title/description for context
            
        Returns:
            List of questions with variable metadata
        """
        
        context_str = f"\n\nTemplate context: {template_context}" if template_context else ""
        
        system_prompt = f"""You are a legal assistant helping gather information for document drafting.

Convert technical variable definitions into clear, friendly questions that a user can easily answer.

QUESTION GUIDELINES:
1. Use natural, professional language
2. Provide context about why the information is needed
3. Include format hints (e.g., "YYYY-MM-DD format", "as printed on policy")
4. Be specific and unambiguous
5. No technical jargon or variable names

EXAMPLES:
- Bad: "policy_number?"
- Good: "What is the insurance policy number exactly as it appears on your policy schedule?"

- Bad: "incident_date"
- Good: "On what date did the incident occur? (Please provide in YYYY-MM-DD format)"

- Bad: "demand_amount_inr?"
- Good: "What is the total claim amount you are demanding in Indian Rupees (excluding interest)?"
{context_str}

Return questions as JSON array with this format:
[
  {{
    "variable_key": "key_name",
    "question": "Clear question text",
    "hint": "Additional format/input hints",
    "required": true
  }}
]
"""
        
        variables_json = json.dumps(variables, indent=2)
        user_prompt = f"""Generate questions for these variables:

{variables_json}

Return clear, user-friendly questions."""
        
        try:
            response = self.model.generate_content(
                [system_prompt, user_prompt],
                generation_config={
                    "temperature": 0.4,
                    "max_output_tokens": 4096,
                }
            )
            
            result_text = response.text.strip()
            
            # Extract JSON
            json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            
            questions = json.loads(result_text)
            return questions
            
        except Exception as e:
            print(f"Error generating questions: {e}")
            # Fallback to simple questions
            return [
                {
                    "variable_key": var["key"],
                    "question": f"Please provide: {var['label']}",
                    "hint": var.get("example", ""),
                    "required": var.get("required", False)
                }
                for var in variables
            ]
    
    def pre_fill_variables(
        self,
        user_query: str,
        variables: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Attempt to pre-fill variables from user query.
        
        Args:
            user_query: User's original request
            variables: Template variables
            
        Returns:
            Dict of variable_key: value for filled variables
        """
        
        system_prompt = """You are extracting information from a user's request to pre-fill template variables.

RULES:
1. Only extract information explicitly stated in the user query
2. Do NOT make assumptions or generate placeholder data
3. Match data types and formats specified in variable definitions
4. For dates, use ISO 8601 format (YYYY-MM-DD)
5. Return empty object {} if nothing can be extracted

OUTPUT FORMAT (strict JSON):
{
  "variable_key": "extracted_value",
  "another_key": "another_value"
}
"""
        
        variables_json = json.dumps(variables, indent=2)
        user_prompt = f"""User query: "{user_query}"

Variables to fill:
{variables_json}

Extract any values mentioned in the query that match these variables."""
        
        try:
            response = self.model.generate_content(
                [system_prompt, user_prompt],
                generation_config={
                    "temperature": 0.1,
                    "max_output_tokens": 2048,
                }
            )
            
            result_text = response.text.strip()
            
            # Extract JSON
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            
            filled = json.loads(result_text)
            return filled
            
        except Exception as e:
            print(f"Error pre-filling variables: {e}")
            return {}
    
    def generate_embedding(self, text: str) -> Optional[np.ndarray]:
        """
        Generate embedding vector for text.
        
        Args:
            text: Input text
            
        Returns:
            Numpy array of embedding vector
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return np.array(result['embedding'])
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def calculate_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
        except:
            return 0.0


# Global instance - UOIONHHC
gemini_service = GeminiService()
