"""
SQLAlchemy database models for the legal templating system.
Defines templates, variables, instances, and documents tables.
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, Float, JSON, BLOB, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Template(Base):
    """Template model - stores reusable document templates"""
    __tablename__ = "templates"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    file_description = Column(Text)
    doc_type = Column(String)
    jurisdiction = Column(String)
    similarity_tags = Column(JSON)  # List of tags for matching
    body_md = Column(Text, nullable=False)  # Markdown template body
    embedding = Column(BLOB)  # Vector embedding for similarity search
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    variables = relationship("TemplateVariable", back_populates="template", cascade="all, delete-orphan")
    instances = relationship("Instance", back_populates="template")


class TemplateVariable(Base):
    """Template variables - stores variable definitions for templates"""
    __tablename__ = "template_variables"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    template_id = Column(String, ForeignKey("templates.id"), nullable=False)
    key = Column(String, nullable=False)  # snake_case variable key
    label = Column(String, nullable=False)  # Human-readable label
    description = Column(Text)  # Detailed description
    example = Column(String)  # Example value
    required = Column(Boolean, default=False)
    dtype = Column(String, default="string")  # Data type: string, number, date, enum
    regex = Column(String)  # Validation regex
    enum_values = Column(JSON)  # For enum types
    
    # Relationships
    template = relationship("Template", back_populates="variables")


class Instance(Base):
    """Instance model - stores draft instances with filled variables"""
    __tablename__ = "instances"
    
    id = Column(String, primary_key=True, index=True)
    template_id = Column(String, ForeignKey("templates.id"), nullable=False)
    user_query = Column(Text, nullable=False)  # Original user request
    answers_json = Column(JSON)  # Dict of variable_key: answer
    draft_md = Column(Text)  # Generated draft markdown
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    template = relationship("Template", back_populates="instances")


class Document(Base):
    """Document model - stores uploaded raw documents"""
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    raw_text = Column(Text)  # Extracted text content
    embedding = Column(BLOB)  # Vector embedding
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# UOIONHHC - Database models
