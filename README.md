# Lexi - Legal Document Templating System

**AI-powered legal document drafting with intelligent template extraction and generation.**

<!-- UOIONHHC -->

## 🎯 Overview

Lexi is a full-stack application that:
- Ingests legal documents (DOCX/PDF) and converts them to reusable templates
- Extracts variables intelligently using Gemini AI
- Enables natural language drafting through a chat interface
- Automatically searches the web for templates when none exist locally (via exa.ai)
- Generates production-ready legal drafts with smart variable substitution

## 🏗️ Architecture

```
┌─────────────────┐
│   Next.js UI    │
│  (Port 3000)    │
└────────┬────────┘
         │
    HTTP/REST
         │
┌────────▼────────┐      ┌──────────────┐
│  FastAPI        │─────▶│  Gemini API  │
│  Backend        │      │  (LLM)       │
│  (Port 8000)    │      └──────────────┘
└────────┬────────┘
         │                ┌──────────────┐
         ├───────────────▶│  exa.ai      │
         │                │  (Web Search)│
         │                └──────────────┘
         │
┌────────▼────────┐
│   SQLite DB     │
│  - Templates    │
│  - Variables    │
│  - Instances    │
└─────────────────┘
```

## ✨ Features

### Core Features
- ✅ **Document Ingestion**: Upload DOCX/PDF files
- ✅ **Smart Templatization**: AI-powered variable extraction with Gemini
- ✅ **Template Management**: Store, search, and manage templates
- ✅ **Intelligent Matching**: Vector similarity + classification for template selection
- ✅ **Conversational Drafting**: Natural language Q&A for variable filling
- ✅ **Draft Generation**: Multiple output formats (Markdown, DOCX)

### Bonus Features
- ✅ **Web Bootstrap**: Automatic template discovery via exa.ai when no local match
- ✅ **Smart Prompts**: Robust, context-aware LLM prompting
- ✅ **Chunked Processing**: Handle large documents efficiently
- ✅ **Variable Deduplication**: Intelligent field merging across chunks

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- API Keys:
  - **Gemini API Key** (Google AI Studio - free tier)
  - **exa.ai API Key** (optional, $5 free credit for bonus features)

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
Create `backend/.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
EXA_API_KEY=your_exa_api_key_here  # Optional for bonus features
DATABASE_URL=sqlite:///./lexi.db
CORS_ORIGINS=http://localhost:3000
```

5. **Initialize database**:
```bash
python -m app.db.init_db
```

6. **Run backend**:
```bash
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Configure environment**:
Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. **Run frontend**:
```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 📖 Usage Guide

### 1. Upload a Template

1. Click **"Upload Document"** button
2. Select a DOCX or PDF legal document
3. Wait for AI to extract variables (progress shown)
4. Review detected variables in the preview
5. Edit variable details if needed
6. Click **"Save Template"** - you'll get a template ID

### 2. Draft a Document

#### Using Chat Interface:
```
You: "Draft a notice to insurer in India"
```

Assistant will:
- Find the closest matching template
- Show you match confidence and alternatives
- Ask questions for missing variables
- Generate the draft

#### Using Slash Command:
```
/draft "employment termination letter"
```

#### Check Progress:
```
/vars
```
Shows which variables are filled/missing.

### 3. No Template Found (Bonus Feature)

If no local template matches:
1. System automatically searches web via exa.ai
2. Shows found documents with previews
3. Click **"Create Template & Continue"**
4. System templatizes the web document
5. Proceeds with normal Q&A flow

### 4. Generate Draft

After answering questions:
1. Click **"Generate Draft"**
2. Choose generation mode:
   - **Strict Replace**: Only variable substitution
   - **Enhanced**: Minor improvements (optional)
3. Download as Markdown or DOCX
4. Copy to clipboard
5. Edit variables and regenerate if needed

## 🧠 Smart Prompting Design

### Variable Extraction Prompt
```python
system_prompt = """You are a legal document templating expert. 
Extract reusable variables from legal documents.

Rules:
1. Use snake_case keys
2. Deduplicate logically identical fields
3. Provide clear labels and descriptions
4. Include realistic examples
5. Mark required vs optional fields
6. Suggest data types and validation rules

Output strict JSON only."""

user_prompt = """
Document text: {text}

Previously discovered variables: {existing_vars}

Extract NEW variables from this text chunk.
Reuse existing variable keys where the meaning matches.
Only propose new variables for genuinely new fields.
"""
```

### Template Selection Prompt
```python
system_prompt = """You are a template matching assistant.
Given a user request, find the best matching template.

Return:
1. Best match template_id
2. Confidence score (0-1)
3. Brief justification
4. Top 2-3 alternatives

If confidence < 0.6, return no match."""
```

### Question Generation
Transforms variables into human-friendly questions:
- ❌ Bad: "policy_number?"
- ✅ Good: "What is the insurance policy number exactly as it appears on the policy schedule?"

## 📊 Template Format Example

```markdown
---
template_id: tpl_insurance_notice_v1
title: Incident Notice to Insurer
file_description: Notice to insurance company about a claimable incident
jurisdiction: IN
doc_type: legal_notice
variables:
  - key: claimant_full_name
    label: Claimant's full name
    description: Person or entity raising the claim
    example: "Rajesh Kumar"
    required: true
    dtype: string
  - key: incident_date
    label: Date of incident
    description: The date the insured event occurred (ISO 8601)
    example: "2025-07-12"
    required: true
    dtype: date
    regex: "^\d{4}-\d{2}-\d{2}$"
  - key: policy_number
    label: Policy number
    description: Insurance policy reference as printed on schedule
    example: "POL-302786965"
    required: true
    dtype: string
  - key: demand_amount_inr
    label: Demand amount (INR)
    description: Total principal claim excluding interest/fees
    example: "450000"
    required: false
    dtype: number
similarity_tags: ["insurance", "notice", "india", "motor", "health"]
---

Dear Sir/Madam,

Re: Notice of Claim under Policy {{policy_number}}

On {{incident_date}}, {{claimant_full_name}} hereby notifies you...

We demand payment of INR {{demand_amount_inr}} within 15 days...

Yours faithfully,
{{claimant_full_name}}
```

## 🗄️ Database Schema

```sql
-- Templates table
CREATE TABLE templates (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    file_description TEXT,
    doc_type TEXT,
    jurisdiction TEXT,
    similarity_tags JSON,
    body_md TEXT NOT NULL,
    embedding BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Template variables
CREATE TABLE template_variables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_id TEXT NOT NULL,
    key TEXT NOT NULL,
    label TEXT NOT NULL,
    description TEXT,
    example TEXT,
    required BOOLEAN DEFAULT false,
    dtype TEXT DEFAULT 'string',
    regex TEXT,
    enum_values JSON,
    FOREIGN KEY (template_id) REFERENCES templates(id)
);

-- Draft instances
CREATE TABLE instances (
    id TEXT PRIMARY KEY,
    template_id TEXT NOT NULL,
    user_query TEXT NOT NULL,
    answers_json JSON,
    draft_md TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (template_id) REFERENCES templates(id)
);

-- Documents (raw uploads)
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    raw_text TEXT,
    embedding BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎥 Demo Video Points

1. **Upload & Templatization** (2 min)
   - Upload sample insurance notice PDF
   - Show variable extraction in real-time
   - Review and save template

2. **Drafting Flow** (2 min)
   - Chat: "Draft a notice to insurer"
   - Template match card shown
   - Answer Q&A questions
   - Generate draft

3. **Web Bootstrap** (2 min - Bonus)
   - Request: "Draft a lease deed for Victoria"
   - No local template found
   - exa.ai searches web
   - Create template from web doc
   - Complete drafting

## 📁 Sample Documents

See `backend/samples/` directory:
- `insurance_notice_sample.pdf`
- `employment_termination.docx`
- `lease_agreement.pdf`

## 🔒 Security & Validation

- File type validation (DOCX/PDF only)
- File size limits (configurable, default 10MB)
- Input sanitization for all user inputs
- ISO date format validation
- Regex constraints on structured fields
- API rate limiting

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📦 Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **Frontend**: Next.js 14 (React, TypeScript)
- **LLM**: Google Gemini 1.5 Flash
- **Database**: SQLite (dev) / PostgreSQL (prod ready)
- **Search**: exa.ai for web retrieval
- **Document Processing**: python-docx, PyPDF2
- **Embeddings**: Gemini embedding-001

## 🎯 Production Considerations

- Switch to PostgreSQL for production
- Add user authentication (JWT/OAuth)
- Implement rate limiting
- Add caching layer (Redis)
- Set up monitoring (Sentry)
- Deploy backend on Railway/Render
- Deploy frontend on Vercel
- Use managed embedding service

## 🤝 Contributing

This is a take-home project for hiring evaluation.

## 📄 License

Proprietary - Created for hiring assessment

## 👤 Author

**Tracking ID**: UOIONHHC

---

Built with ❤️ for practical legal tech automation
