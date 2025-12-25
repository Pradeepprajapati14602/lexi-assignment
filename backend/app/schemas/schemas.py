"""
Pydantic schemas for API request/response validation.
Defines data structures for templates, variables, and instances.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class VariableSchema(BaseModel):
    """Variable definition schema - UOIONHHC"""
    key: str = Field(..., description="snake_case variable key")
    label: str = Field(..., description="Human-readable label")
    description: Optional[str] = Field(None, description="Detailed description")
    example: Optional[str] = Field(None, description="Example value")
    required: bool = Field(False, description="Whether variable is required")
    dtype: str = Field("string", description="Data type: string, number, date, enum")
    regex: Optional[str] = Field(None, description="Validation regex pattern")
    enum_values: Optional[List[str]] = Field(None, description="For enum types")


class VariableResponse(VariableSchema):
    """Variable response with ID"""
    id: int
    template_id: str
    
    class Config:
        from_attributes = True


class TemplateCreate(BaseModel):
    """Schema for creating a new template"""
    title: str
    file_description: Optional[str] = None
    doc_type: Optional[str] = None
    jurisdiction: Optional[str] = None
    similarity_tags: Optional[List[str]] = []
    body_md: str
    variables: List[VariableSchema]


class TemplateResponse(BaseModel):
    """Template response schema"""
    id: str
    title: str
    file_description: Optional[str]
    doc_type: Optional[str]
    jurisdiction: Optional[str]
    similarity_tags: Optional[List[str]]
    body_md: str
    created_at: datetime
    variables: List[VariableResponse] = []
    
    class Config:
        from_attributes = True


class TemplateMatchResult(BaseModel):
    """Template match result for selection"""
    template_id: str
    title: str
    confidence: float
    justification: str
    file_description: Optional[str] = None


class TemplateMatchResponse(BaseModel):
    """Response for template matching"""
    best_match: Optional[TemplateMatchResult]
    alternatives: List[TemplateMatchResult]
    has_match: bool


class InstanceCreate(BaseModel):
    """Schema for creating a draft instance"""
    template_id: str
    user_query: str
    answers: Dict[str, Any]


class InstanceResponse(BaseModel):
    """Draft instance response"""
    id: str
    template_id: str
    user_query: str
    answers_json: Dict[str, Any]
    draft_md: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class DocumentUploadResponse(BaseModel):
    """Response after document upload"""
    document_id: str
    filename: str
    status: str
    message: str


class ExtractionResult(BaseModel):
    """Result of template extraction from document"""
    template: TemplateCreate
    extraction_stats: Dict[str, Any]


class ChatMessage(BaseModel):
    """Chat message schema"""
    role: str  # "user" or "assistant"
    content: str
    metadata: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    """Chat request with message history"""
    message: str
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = {}


class ChatResponse(BaseModel):
    """Chat response"""
    conversation_id: str
    message: str
    message_type: str  # "text", "template_match", "question", "draft"
    data: Optional[Dict[str, Any]] = None


class QuestionResponse(BaseModel):
    """Response containing questions for variables"""
    questions: List[Dict[str, Any]]
    template_id: str
    filled_count: int
    total_count: int


class DraftGenerateRequest(BaseModel):
    """Request to generate a draft"""
    instance_id: str
    mode: str = "strict"  # "strict" or "enhanced"


class DraftResponse(BaseModel):
    """Generated draft response"""
    instance_id: str
    draft_md: str
    draft_docx_url: Optional[str] = None
    template_title: str
