"""
Templates API endpoints for managing document templates.
Handles template creation, retrieval, search, and matching.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db import models
from app.schemas import schemas
from app.services.template_service import template_service
from app.services.document_processor import document_processor

router = APIRouter()


@router.post("/", response_model=schemas.TemplateResponse)
async def create_template(
    template: schemas.TemplateCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new template.
    Saves template with variables to database.
    Created by UOIONHHC
    """
    try:
        db_template = template_service.save_template(db, template)
        return db_template
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating template: {str(e)}")


@router.get("/", response_model=List[schemas.TemplateResponse])
async def list_templates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of all templates"""
    templates = db.query(models.Template).offset(skip).limit(limit).all()
    return templates


@router.get("/{template_id}", response_model=schemas.TemplateResponse)
async def get_template(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Get template by ID with all variables"""
    template = template_service.get_template_by_id(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.post("/match", response_model=schemas.TemplateMatchResponse)
async def match_template(
    query: str,
    db: Session = Depends(get_db)
):
    """
    Match user query to best template.
    Uses Gemini AI for intelligent template selection.
    """
    try:
        result = await template_service.match_template(db, query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching template: {str(e)}")


@router.delete("/{template_id}")
async def delete_template(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Delete template by ID"""
    template = template_service.get_template_by_id(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    db.delete(template)
    db.commit()
    
    return {"status": "success", "message": f"Template {template_id} deleted"}


@router.get("/{template_id}/variables", response_model=List[schemas.VariableResponse])
async def get_template_variables(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Get all variables for a template"""
    template = template_service.get_template_by_id(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return template.variables


@router.get("/{template_id}/export")
async def export_template(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Export template as Markdown with YAML front-matter"""
    template = template_service.get_template_by_id(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Build variables list
    variables = []
    for var in template.variables:
        var_dict = {
            "key": var.key,
            "label": var.label,
            "description": var.description,
            "example": var.example,
            "required": var.required,
            "dtype": var.dtype
        }
        if var.regex:
            var_dict["regex"] = var.regex
        if var.enum_values:
            var_dict["enum_values"] = var.enum_values
        variables.append(var_dict)
    
    # Build metadata
    metadata = {
        "template_id": template.id,
        "title": template.title,
        "file_description": template.file_description,
        "jurisdiction": template.jurisdiction,
        "doc_type": template.doc_type,
        "similarity_tags": template.similarity_tags
    }
    
    # Create markdown
    markdown = document_processor.create_markdown_template(
        template.body_md,
        variables,
        metadata
    )
    
    return {
        "template_id": template_id,
        "markdown": markdown
    }
