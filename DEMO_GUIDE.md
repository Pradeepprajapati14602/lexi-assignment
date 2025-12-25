# Lexi Demo Guide

**Complete walkthrough for evaluators - UOIONHHC**

## 🎯 Quick Start (5 minutes)

### Prerequisites Check
- ✅ Python 3.10+ installed
- ✅ Node.js 18+ installed
- ✅ Git installed (to clone repo)
- ✅ Gemini API key from Google AI Studio
- ✅ (Optional) Exa.ai API key for bonus features

### Step 1: Get API Keys (2 minutes)

#### Gemini API Key (Required)
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

#### Exa API Key (Bonus Feature)
1. Visit: https://dashboard.exa.ai/
2. Sign up (free $5 credit)
3. Copy your API key

### Step 2: Backend Setup (2 minutes)

```powershell
# Navigate to backend
cd lexi\backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
Copy-Item .env.example .env

# Edit .env and add your keys:
# GEMINI_API_KEY=your_actual_key_here
# EXA_API_KEY=your_exa_key_here (optional)

# Initialize database
python -m app.db.init_db

# Start backend
uvicorn app.main:app --reload --port 8000
```

Backend will run at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Step 3: Frontend Setup (2 minutes)

Open a NEW terminal:

```powershell
# Navigate to frontend
cd lexi\frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

Frontend will run at: http://localhost:3000

## 📹 Demo Script (6 minutes)

### Demo 1: Upload & Template Creation (2 min)

**Goal:** Show AI-powered template extraction

1. **Open app**: Navigate to http://localhost:3000
2. **Click "Upload Document"** button (top right)
3. **Upload sample**: Use `backend\samples\insurance_notice_sample.md`
   - System extracts text
   - Gemini AI identifies 10+ variables
   - Shows variable preview
4. **Review variables**:
   - Scroll through detected fields
   - Note: label, description, examples, required status
5. **Click "Save Template"**
   - Toast notification shows template ID
   - Template added to library

**Key Points to Highlight:**
- ✅ Automatic variable extraction
- ✅ Smart field detection (names, dates, amounts, policy numbers)
- ✅ Clear labels and descriptions
- ✅ Required vs optional fields
- ✅ Data type inference

### Demo 2: Chat-Based Drafting (2 min)

**Goal:** Show natural language document generation

1. **In Chat tab**, type: `"Draft a notice to insurer in India"`
2. **Template Match Card appears**:
   - Shows best match with confidence score
   - Provides justification
   - Lists alternatives
3. **Type "yes"** to proceed
4. **Q&A Flow**:
   - System asks human-friendly questions
   - Example: "What is the insurance policy number exactly as it appears on your policy schedule?"
   - Answer: `POL-302786965`
   - System shows progress: "Q2/10"
5. **Continue answering** a few more questions:
   - Claimant name: `Rajesh Kumar`
   - Incident date: `2025-07-12`
   - Claim amount: `450000`
6. **Draft Generated**:
   - Complete document with all variables filled
   - Professional formatting
   - Copy/Download options

**Key Points to Highlight:**
- ✅ Natural language understanding
- ✅ Smart template matching
- ✅ Context-aware questions (no "policy_number?")
- ✅ Progress tracking
- ✅ Clean, ready-to-use output

### Demo 3: Web Bootstrap - Bonus Feature (2 min)

**Goal:** Show automatic template discovery via exa.ai

1. **Request uncommon template**: `"Draft a lease agreement for Victoria, Australia"`
2. **No Local Match**:
   - System: "No matching template found locally"
   - Automatically triggers web search
3. **Web Results Shown**:
   - 3-5 similar documents from web
   - Shows titles, URLs, previews
4. **Select result**: Type `1` to choose first result
5. **Template Created**:
   - System extracts variables from web document
   - Saves as new template
   - Proceeds to Q&A flow
6. **Complete drafting** as normal

**Key Points to Highlight:**
- ✅ Seamless fallback to web search
- ✅ Real-time template creation
- ✅ No manual intervention needed
- ✅ Expands template library automatically

## 🎬 Alternative Demo Scenarios

### Scenario A: Employment Letter
```
User: "Draft an employment termination letter"
System: [Matches employment_termination template]
User: "yes"
System: [Asks for employee name, designation, termination date, etc.]
User: [Provides answers]
System: [Generates professional termination letter]
```

### Scenario B: Using Slash Commands
```
User: "/draft insurance claim notice"
System: [Matches template, starts Q&A]

User: "/vars"
System: [Shows filled vs missing variables]
```

### Scenario C: Template Management
1. Click "Templates" tab
2. View all templates in gallery
3. Click "View" to see variables
4. Export template as Markdown
5. Delete unwanted templates

## 🔍 Feature Checklist for Evaluation

### Core Features
- [x] **Document Upload**: DOCX/PDF validation and processing
- [x] **Variable Extraction**: AI-powered with Gemini
- [x] **Template Storage**: Database with embeddings
- [x] **Template Matching**: Classification + similarity
- [x] **Smart Questions**: Human-friendly prompts
- [x] **Draft Generation**: Variable substitution
- [x] **Multiple Formats**: Markdown, DOCX download

### Bonus Features
- [x] **Exa.ai Integration**: Web template discovery
- [x] **Chunked Processing**: Handle large documents
- [x] **Variable Deduplication**: Across chunks
- [x] **Pre-filling**: Extract from user query
- [x] **Progress Tracking**: Q&A status
- [x] **Conversation State**: Multi-turn dialogue

### Smart Prompting
- [x] **Extraction Prompt**: Structured JSON output
- [x] **Classification Prompt**: Template matching
- [x] **Question Generation**: Context-aware
- [x] **Pre-fill Prompt**: Value extraction
- [x] **Guardrails**: Validation and safety

### UI/UX
- [x] **Modern Interface**: Tailwind CSS
- [x] **Real-time Updates**: Progress indicators
- [x] **Error Handling**: Clear messages
- [x] **Responsive Design**: Works on all screens
- [x] **Markdown Rendering**: Beautiful display

## 🐛 Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'app'"**
```powershell
# Make sure you're in backend directory and venv is activated
cd backend
.\venv\Scripts\activate
```

**"Database not found"**
```powershell
python -m app.db.init_db
```

**"GEMINI_API_KEY not configured"**
- Check `.env` file exists in `backend/` directory
- Verify API key is valid (test at https://makersuite.google.com/)

**"CORS error"**
- Backend must run on port 8000
- Frontend must run on port 3000
- Check CORS_ORIGINS in `.env`

### Frontend Issues

**"Cannot connect to API"**
- Verify backend is running: http://localhost:8000/health
- Check `.env.local` has correct API URL

**"npm install fails"**
```powershell
# Clear cache and retry
npm cache clean --force
npm install
```

**"Port 3000 already in use"**
```powershell
# Use different port
npm run dev -- -p 3001
# Update .env.local: NEXT_PUBLIC_API_URL=http://localhost:3001
```

## 📊 Testing Checklist

### Functional Tests
- [ ] Upload valid DOCX file → Success
- [ ] Upload valid PDF file → Success
- [ ] Upload invalid file type → Error
- [ ] Upload file > 10MB → Error
- [ ] Extract variables from simple doc → 3+ variables
- [ ] Extract variables from complex doc → 10+ variables
- [ ] Match exact query → Confidence > 0.8
- [ ] Match fuzzy query → Confidence 0.6-0.8
- [ ] No match query → Web search triggered (if exa enabled)
- [ ] Answer all questions → Draft generated
- [ ] Skip optional field → Draft still generates
- [ ] Copy draft → Clipboard populated
- [ ] Download draft → File saved

### Prompt Quality Tests
- [ ] Variable labels are clear (no technical jargon)
- [ ] Questions include context and format hints
- [ ] No raw variable names exposed to user
- [ ] Consistent formatting across questions
- [ ] Regex validation for structured fields
- [ ] Date format hints (YYYY-MM-DD)

### Edge Cases
- [ ] Document with no variables → Graceful handling
- [ ] Very long document (>10 pages) → Chunked processing
- [ ] Document with tables → Text extracted
- [ ] Multiple similar templates → Top 3 shown
- [ ] Conversation interrupted → State preserved
- [ ] Browser refresh → Can continue (check localStorage)

## 📈 Performance Metrics

Expected timings on standard hardware:

| Operation | Time |
|-----------|------|
| Upload 2MB PDF | < 3 seconds |
| Extract variables (5 pages) | 5-10 seconds |
| Template matching | < 2 seconds |
| Question generation | < 3 seconds |
| Draft generation | < 2 seconds |
| Web search (exa) | 3-5 seconds |

## 🎯 Evaluation Criteria Mapping

### Technical Implementation (40%)
- ✅ FastAPI backend with proper structure
- ✅ Next.js 14 with TypeScript
- ✅ SQLAlchemy ORM with migrations
- ✅ Gemini AI integration
- ✅ Exa.ai integration (bonus)
- ✅ Error handling and validation
- ✅ API documentation (FastAPI /docs)

### Prompt Engineering (30%)
- ✅ Structured extraction prompt
- ✅ Classification for matching
- ✅ Human-friendly question generation
- ✅ Pre-filling logic
- ✅ Chunked processing strategy
- ✅ Variable deduplication

### User Experience (20%)
- ✅ Intuitive upload flow
- ✅ Clear variable review
- ✅ Natural chat interface
- ✅ Progress indicators
- ✅ Error messages
- ✅ Download options

### Bonus Features (10%)
- ✅ Exa.ai web bootstrap
- ✅ Advanced prompting
- ✅ Template management UI
- ✅ Slash commands
- ✅ Markdown export

## 📝 Sample Output Files

After demo, you should have:

1. **Database**: `backend/lexi.db` with templates and variables
2. **Generated Drafts**: Available in chat history
3. **Exported Templates**: Markdown files with front-matter
4. **API Logs**: Console output showing AI interactions

## 🚀 Production Readiness Checklist

Before deploying:
- [ ] Switch to PostgreSQL
- [ ] Add user authentication
- [ ] Implement rate limiting
- [ ] Set up monitoring (Sentry)
- [ ] Add caching layer (Redis)
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up CI/CD
- [ ] Add automated tests
- [ ] Document API endpoints

## 📧 Support & Questions

This is a take-home project for hiring evaluation.

**Tracking ID**: UOIONHHC

---

**Good luck with the demo! 🎉**

Show off the AI-powered magic and the seamless user experience.
