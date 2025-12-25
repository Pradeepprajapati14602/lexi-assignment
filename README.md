Lexi – Legal Document Templating System

Lexi is an AI-powered full-stack application designed to simplify legal document drafting by converting existing legal documents into reusable templates and generating new drafts through natural language interaction.

The goal of the system is to eliminate repetitive manual drafting work for legal teams by introducing a structured, template-based and AI-assisted workflow.

Problem Lexi Solves

Legal documents usually:

Follow a fixed structure

Contain repetitive clauses

Differ only in variable details (names, dates, amounts, policy numbers, etc.)

Lexi solves this by:

Converting legal documents into reusable templates

Automatically extracting meaningful variables using AI

Allowing users to generate drafts through a chat-based interface

How the System Works

The user uploads a legal document (PDF or DOCX)

The system analyzes the document and extracts reusable variables

A template is created and stored in the database

The user requests a new draft using natural language

The system selects the best matching template

Missing information is collected through guided questions

A production-ready legal draft is generated

Architecture Overview

Lexi follows a clean and scalable architecture:

Frontend: Next.js (Port 3000)

Backend: FastAPI (Port 8000)

LLM: Google Gemini

Database: SQLite (development)

Web Search (Optional): exa.ai

The frontend communicates with the backend via REST APIs.
The backend handles document processing, AI interactions, template management, and draft generation.

Core Features
1. Document Upload & Templatization

Users can upload PDF or DOCX legal documents

Documents are processed in chunks for reliability

AI intelligently extracts reusable variables

Duplicate or logically identical fields are merged automatically

2. Template Management

Templates are stored with metadata such as document type and jurisdiction

Templates can be searched and reused across multiple drafts

Ensures consistency in legal language

3. Intelligent Template Matching

User requests are matched with existing templates

Vector similarity and classification are used

Confidence scores help determine the best match

4. Conversational Drafting

Users can request drafts in plain English

“Draft a notice to an insurer in India”

The system asks clear, human-friendly questions

Variables are filled step by step

5. Draft Generation

Drafts are generated once all required fields are filled

Output formats include:

Markdown

DOCX

Bonus Feature – Web Template Bootstrap

If no suitable local template is found:

The system automatically searches the web using exa.ai

Relevant legal documents are fetched and previewed

A new template is created from the web source

Drafting continues without interruption

This ensures the system works even with zero pre-existing templates.

AI Prompting Strategy (High Level)

The prompting system is designed for reliability and consistency:

Variables use snake_case naming

Required and optional fields are clearly identified

Data types, examples, and validation rules are included

AI outputs are strictly structured (JSON-based)

This minimizes hallucinations and improves extraction accuracy.

Template Design Concept

Each template contains:

Metadata (title, document type, jurisdiction)

A list of variables with labels and descriptions

A Markdown body with placeholder variables

During generation, only the placeholders are replaced.
The original legal wording remains unchanged.

Database Design

The system uses four primary tables:

Templates – reusable legal templates

Template Variables – structured fields for each template

Instances – generated drafts with user inputs

Documents – raw uploaded documents

The schema is intentionally simple to allow easy migration to PostgreSQL in production.

Security & Validation

Only PDF and DOCX uploads are allowed

File size limits are enforced

All user inputs are sanitized

Date and structured fields are validated using regex

Rate limiting is supported for production environments

Production Readiness

Planned production improvements include:

PostgreSQL database migration

JWT or OAuth-based authentication

Redis caching

Error tracking and monitoring (Sentry)

Cloud deployment (Railway, Render, Vercel)

Technology Stack

Frontend: Next.js 14 (React, TypeScript)

Backend: FastAPI (Python)

LLM: Google Gemini 1.5 Flash

Database: SQLite (development)

Document Processing: PyPDF2, python-docx

Web Search: exa.ai (optional)
