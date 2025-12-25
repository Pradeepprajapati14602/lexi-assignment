# Lexi Project Structure - Complete File Tree

```
lexi/
│
├── 📄 README.md                          # Main documentation (comprehensive)
├── 📄 QUICKSTART.md                      # 5-minute setup guide
├── 📄 DEMO_GUIDE.md                      # Complete demo walkthrough
├── 📄 SUBMISSION.md                      # Submission summary
├── 📄 .gitignore                         # Git ignore rules
├── 📄 setup.ps1                          # Automated setup script
│
├── 📁 backend/                           # FastAPI Backend (Python)
│   │
│   ├── 📄 requirements.txt               # Python dependencies
│   ├── 📄 .env.example                   # Environment template
│   ├── 📄 .env                           # Your API keys (create this)
│   ├── 📄 lexi.db                        # SQLite database (auto-created)
│   │
│   ├── 📁 app/                           # Main application
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py                    # FastAPI app entry point
│   │   │
│   │   ├── 📁 api/                       # API endpoints
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 documents.py           # Upload & extraction
│   │   │   ├── 📄 templates.py           # Template CRUD
│   │   │   └── 📄 chat.py                # Conversation & drafting
│   │   │
│   │   ├── 📁 core/                      # Core configuration
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 config.py              # Settings & environment
│   │   │
│   │   ├── 📁 db/                        # Database layer
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 database.py            # SQLAlchemy setup
│   │   │   ├── 📄 models.py              # Database models
│   │   │   └── 📄 init_db.py             # DB initialization
│   │   │
│   │   ├── 📁 schemas/                   # Pydantic schemas
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 schemas.py             # Request/response models
│   │   │
│   │   └── 📁 services/                  # Business logic
│   │       ├── 📄 __init__.py
│   │       ├── 📄 gemini_service.py      # Gemini AI integration ⭐
│   │       ├── 📄 document_processor.py  # DOCX/PDF processing
│   │       ├── 📄 template_service.py    # Template operations
│   │       └── 📄 exa_service.py         # Web search (bonus) 🎁
│   │
│   └── 📁 samples/                       # Sample templates
│       ├── 📄 README.md
│       ├── 📄 insurance_notice_sample.md
│       └── 📄 employment_termination_sample.md
│
└── 📁 frontend/                          # Next.js Frontend (TypeScript)
    │
    ├── 📄 package.json                   # Node dependencies
    ├── 📄 tsconfig.json                  # TypeScript config
    ├── 📄 tailwind.config.js             # Tailwind CSS
    ├── 📄 postcss.config.js              # PostCSS config
    ├── 📄 next.config.js                 # Next.js config
    ├── 📄 .env.local                     # API URL (create this)
    │
    └── 📁 src/
        │
        ├── 📁 app/                       # Next.js 14 App Router
        │   ├── 📄 layout.tsx             # Root layout
        │   ├── 📄 page.tsx               # Main page
        │   └── 📄 globals.css            # Global styles
        │
        └── 📁 components/                # React components
            ├── 📄 ChatInterface.tsx      # Chat & drafting UI ⭐
            ├── 📄 UploadDialog.tsx       # Document upload modal
            └── 📄 TemplateList.tsx       # Template management

```

## 📊 File Statistics

| Category | Count | Lines of Code (approx) |
|----------|-------|------------------------|
| Python Backend | 12 files | ~1,800 LOC |
| TypeScript Frontend | 8 files | ~1,500 LOC |
| Documentation | 5 files | ~2,000 lines |
| Configuration | 8 files | ~200 LOC |
| **Total** | **33 files** | **~5,500 LOC** |

## 🎯 Key Files by Function

### 🔥 Core Intelligence (AI/ML)
- `backend/app/services/gemini_service.py` - 400+ LOC
  - Variable extraction with chunking
  - Template matching
  - Question generation
  - Pre-filling logic
  - Embedding generation

### 🚀 API Endpoints
- `backend/app/api/chat.py` - 450+ LOC
  - Conversation management
  - State handling
  - Q&A flow
  - Draft generation
  - Web bootstrap integration

### 💎 Frontend Components
- `frontend/src/components/ChatInterface.tsx` - 200+ LOC
  - Message display
  - User input
  - Real-time updates
  - Draft actions

- `frontend/src/components/UploadDialog.tsx` - 250+ LOC
  - File upload
  - Variable preview
  - Template creation

### 🎁 Bonus Features
- `backend/app/services/exa_service.py` - 150+ LOC
  - Web search integration
  - Content extraction
  - Template discovery

## 🔒 Security & Configuration

### Must Create (Not in Git)
1. `backend/.env` - Your API keys
2. `frontend/.env.local` - API URL
3. `backend/lexi.db` - Auto-created on first run
4. `backend/venv/` - Python virtual environment
5. `frontend/node_modules/` - Node packages

### Already Included
- ✅ `.env.example` - Environment template
- ✅ `.gitignore` - Ignores sensitive files
- ✅ Sample documents
- ✅ Complete documentation

## 📦 Dependencies

### Backend (Python)
- **Web**: FastAPI, Uvicorn
- **Database**: SQLAlchemy
- **AI**: google-generativeai, exa-py
- **Documents**: python-docx, PyPDF2
- **Utilities**: pydantic, python-dotenv

### Frontend (TypeScript)
- **Framework**: Next.js 14, React 18
- **Styling**: Tailwind CSS
- **HTTP**: Axios
- **Markdown**: react-markdown
- **UI**: lucide-react (icons)
- **Upload**: react-dropzone

## 🎯 Quick Navigation

**To setup**: Start with `setup.ps1` or `QUICKSTART.md`

**To demo**: Follow `DEMO_GUIDE.md`

**To understand**: Read `README.md`

**To submit**: Review `SUBMISSION.md`

**To extend**:
- Add API routes: `backend/app/api/`
- Add services: `backend/app/services/`
- Add components: `frontend/src/components/`
- Add templates: `backend/samples/`

---

**All files are in place and ready to run!** ✅

**Tracking: UOIONHHC**
