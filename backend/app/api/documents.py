"""
Documents API endpoints for uploading and processing documents.
Handles file upload, validation, and template extraction.
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import os
from pathlib import Path

from app.db.database import get_db
from app.db import models
from app.schemas import schemas
from app.services.document_processor import document_processor
from app.services.template_service import template_service
from app.core.config import settings

router = APIRouter()


@router.post("/upload", response_model=schemas.DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a legal document (DOCX/PDF) for processing.
    Extracts text and stores in database.
    Created by UOIONHHC
    """
    # Validate file
    document_processor.validate_file(file, settings.MAX_UPLOAD_SIZE)
    
    # Extract text
    try:
        text, temp_path = await document_processor.extract_text(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    
    # Save document to database
    document_id = f"doc_{uuid.uuid4().hex[:12]}"
    
    # Generate embedding
    from app.services.gemini_service import gemini_service
    embedding = gemini_service.generate_embedding(text[:1000])  # Use first 1000 chars
    embedding_bytes = embedding.tobytes() if embedding is not None else None
    
    db_document = models.Document(
        id=document_id,
        filename=file.filename,
        mime_type=file.content_type,
        raw_text=text,
        embedding=embedding_bytes
    )
    
    db.add(db_document)
    db.commit()
    
    # Clean up temp file
    if os.path.exists(temp_path):
        os.unlink(temp_path)
    
    return schemas.DocumentUploadResponse(
        document_id=document_id,
        filename=file.filename,
        status="success",
        message=f"Document uploaded successfully. Extracted {len(text)} characters."
    )


@router.post("/extract-template/{document_id}", response_model=schemas.ExtractionResult)
async def extract_template(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Extract template from uploaded document.
    Uses Gemini AI to identify variables and create reusable template.
    """
    # Get document
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not document.raw_text:
        raise HTTPException(status_code=400, detail="Document has no extracted text")
    
    # Extract template
    try:
        result = await template_service.extract_template_from_document(
            document.raw_text,
            document.filename
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting template: {str(e)}")


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Get document by ID"""
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {
        "id": document.id,
        "filename": document.filename,
        "mime_type": document.mime_type,
        "text_length": len(document.raw_text) if document.raw_text else 0,
        "created_at": document.created_at
    }
