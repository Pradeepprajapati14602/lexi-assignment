"""
Template service for managing template operations.
Handles template extraction, storage, retrieval, and matching.
"""

import uuid
import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import schemas
from app.services.gemini_service import gemini_service
from app.services.document_processor import document_processor
from app.core.config import settings


class TemplateService:
    """Service for template operations - UOIONHHC"""
    
    @staticmethod
    async def extract_template_from_document(
        text: str,
        filename: str
    ) -> schemas.ExtractionResult:
        """
        Extract template from document text using chunked processing.
        
        Args:
            text: Document text
            filename: Original filename
            
        Returns:
            ExtractionResult with template data
        """
        import re
        
        # Pre-detect existing placeholders in format {{variable_name}}
        placeholder_pattern = r'\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}'
        existing_placeholders = re.findall(placeholder_pattern, text)
        
        chunks = []  # Initialize chunks for stats
        
        # If document already has placeholders, extract them directly
        if existing_placeholders:
            all_variables = []
            for placeholder in set(existing_placeholders):
                # Convert snake_case to human readable
                label = placeholder.replace('_', ' ').title()
                all_variables.append({
                    "key": placeholder,
                    "label": label,
                    "description": f"Variable for {label.lower()}",
                    "example": "",
                    "required": True,
                    "dtype": "string",
                    "regex": None,
                    "enum_values": None
                })
            all_tags = []
            template_text = text  # Keep the text as-is with placeholders
            chunks = [text]  # Single chunk for stats
        else:
            # Chunk the document for AI extraction
            chunks = document_processor.chunk_text(text, settings.CHUNK_SIZE)
            
            all_variables = []
            all_tags = set()
            
            # Process first chunk to establish initial variables
            first_chunk_result = gemini_service.extract_variables_from_chunk(
                chunks[0],
                existing_variables=None
            )
            
            all_variables.extend(first_chunk_result.get("variables", []))
            all_tags.update(first_chunk_result.get("similarity_tags", []))
        
            # Process remaining chunks with existing variables
            for chunk in chunks[1:]:
                chunk_result = gemini_service.extract_variables_from_chunk(
                    chunk,
                    existing_variables=all_variables
                )
                
                # Add new variables only
                new_vars = chunk_result.get("variables", [])
                existing_keys = {v["key"] for v in all_variables}
                
                for var in new_vars:
                    if var["key"] not in existing_keys:
                        all_variables.append(var)
                
                all_tags.update(chunk_result.get("similarity_tags", []))
            
            # Replace variable occurrences with {{variable_key}}
            template_text = text
            for var in all_variables:
                # Look for the example value or label in text
                example = var.get("example", "")
                if example and example in template_text:
                    # Replace first few occurrences
                    template_text = template_text.replace(
                        example,
                        f"{{{{{var['key']}}}}}",
                        3  # Replace up to 3 occurrences
                    )
        
        # Generate template ID
        template_id = f"tpl_{uuid.uuid4().hex[:12]}"
        
        # Extract title from filename or first line
        title = filename.replace('.pdf', '').replace('.docx', '').replace('_', ' ').title()
        
        # Create template schema
        template_data = schemas.TemplateCreate(
            title=title,
            file_description=f"Template extracted from {filename}",
            doc_type="legal_document",
            jurisdiction="",
            similarity_tags=list(all_tags) if isinstance(all_tags, set) else all_tags,
            body_md=template_text,
            variables=[schemas.VariableSchema(**var) for var in all_variables]
        )
        
        stats = {
            "total_chunks": len(chunks),
            "variables_found": len(all_variables),
            "tags_found": len(all_tags),
            "template_length": len(template_text)
        }
        
        return schemas.ExtractionResult(
            template=template_data,
            extraction_stats=stats
        )
    
    @staticmethod
    def save_template(
        db: Session,
        template: schemas.TemplateCreate
    ) -> models.Template:
        """
        Save template to database.
        
        Args:
            db: Database session
            template: Template data
            
        Returns:
            Saved template model
        """
        # Generate ID if not provided
        template_id = f"tpl_{uuid.uuid4().hex[:12]}"
        
        # Generate embedding for template (temporarily disabled due to quota)
        # embedding_text = f"{template.title} {template.file_description} {' '.join(template.similarity_tags or [])}"
        # embedding = gemini_service.generate_embedding(embedding_text)
        embedding = None
        embedding_bytes = None  # embedding.tobytes() if embedding is not None else None
        
        # Create template
        db_template = models.Template(
            id=template_id,
            title=template.title,
            file_description=template.file_description,
            doc_type=template.doc_type,
            jurisdiction=template.jurisdiction,
            similarity_tags=template.similarity_tags,
            body_md=template.body_md,
            embedding=embedding_bytes
        )
        
        db.add(db_template)
        db.flush()
        
        # Create variables
        for var in template.variables:
            db_var = models.TemplateVariable(
                template_id=template_id,
                key=var.key,
                label=var.label,
                description=var.description,
                example=var.example,
                required=var.required,
                dtype=var.dtype,
                regex=var.regex,
                enum_values=var.enum_values
            )
            db.add(db_var)
        
        db.commit()
        db.refresh(db_template)
        
        return db_template
    
    @staticmethod
    def get_all_templates(db: Session) -> List[models.Template]:
        """Get all templates"""
        return db.query(models.Template).all()
    
    @staticmethod
    def get_template_by_id(db: Session, template_id: str) -> Optional[models.Template]:
        """Get template by ID"""
        return db.query(models.Template).filter(models.Template.id == template_id).first()
    
    @staticmethod
    async def match_template(
        db: Session,
        user_query: str
    ) -> schemas.TemplateMatchResponse:
        """
        Match user query to best template.
        
        Args:
            db: Database session
            user_query: User's drafting request
            
        Returns:
            TemplateMatchResponse with best match and alternatives
        """
        templates = TemplateService.get_all_templates(db)
        
        if not templates:
            return schemas.TemplateMatchResponse(
                best_match=None,
                alternatives=[],
                has_match=False
            )
        
        # Prepare template data for matching
        template_data = []
        for tmpl in templates:
            template_data.append({
                "id": tmpl.id,
                "title": tmpl.title,
                "file_description": tmpl.file_description,
                "doc_type": tmpl.doc_type,
                "jurisdiction": tmpl.jurisdiction,
                "similarity_tags": tmpl.similarity_tags or []
            })
        
        # Use Gemini to match
        match_result = gemini_service.match_template(user_query, template_data)
        
        # Build response
        best_match = None
        if match_result.get("best_match"):
            bm = match_result["best_match"]
            template = TemplateService.get_template_by_id(db, bm["template_id"])
            if template:
                best_match = schemas.TemplateMatchResult(
                    template_id=template.id,
                    title=template.title,
                    confidence=bm["confidence"],
                    justification=bm["justification"],
                    file_description=template.file_description
                )
        
        alternatives = []
        for alt in match_result.get("alternatives", []):
            template = TemplateService.get_template_by_id(db, alt["template_id"])
            if template:
                alternatives.append(schemas.TemplateMatchResult(
                    template_id=template.id,
                    title=template.title,
                    confidence=alt["confidence"],
                    justification=alt["justification"],
                    file_description=template.file_description
                ))
        
        return schemas.TemplateMatchResponse(
            best_match=best_match,
            alternatives=alternatives,
            has_match=match_result.get("has_match", False)
        )


# Global instance
template_service = TemplateService()
