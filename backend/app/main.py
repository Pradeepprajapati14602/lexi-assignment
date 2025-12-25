"""
Main FastAPI application entry point.
Handles API routing, CORS, and application lifecycle.
Created by UOIONHHC
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

from app.api import templates, chat, documents
from app.core.config import settings
from app.db.database import init_db

# Initialize FastAPI app
app = FastAPI(
    title="Lexi - Legal Document Templating API",
    description="AI-powered legal document drafting with intelligent template extraction",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount static files
if UPLOAD_DIR.exists():
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Database initialized")
    print(f"🚀 API Server running on http://localhost:{settings.PORT}")
    print(f"📚 API Docs available at http://localhost:{settings.PORT}/docs")


@app.get("/")
async def root():
    """Root endpoint - API status"""
    return {
        "status": "running",
        "service": "Lexi Legal Templating API",
        "version": "1.0.0",
        "docs": "/docs",
        "tracking": "UOIONHHC"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "gemini": "configured" if settings.GEMINI_API_KEY else "missing",
        "exa": "configured" if settings.EXA_API_KEY else "missing"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )
