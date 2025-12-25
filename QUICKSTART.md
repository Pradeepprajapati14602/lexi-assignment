# ⚡ Lexi - Quick Start Guide

**Get running in 5 minutes!**

---

## 🎯 Prerequisites (2 min)

1. **Install Python 3.10+**: https://www.python.org/downloads/
2. **Install Node.js 18+**: https://nodejs.org/
3. **Get Gemini API Key**: https://makersuite.google.com/app/apikey
4. **(Optional) Get Exa API Key**: https://dashboard.exa.ai/

---

## 🚀 Automated Setup

### Windows (PowerShell)

```powershell
cd lexi
.\setup.ps1
```

Follow the prompts to add your API keys!

---

## 🔧 Manual Setup (if script fails)

### Backend (Terminal 1)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Copy and edit .env
Copy-Item .env.example .env
notepad .env  # Add your GEMINI_API_KEY

python -m app.db.init_db
uvicorn app.main:app --reload --port 8000
```

### Frontend (Terminal 2)

```powershell
cd frontend
npm install
npm run dev
```

---

## ✅ Verify Setup

1. **Backend Running**: http://localhost:8000/health
   - Should return: `{"status": "healthy"}`

2. **Frontend Running**: http://localhost:3000
   - Should show Lexi interface

3. **API Docs**: http://localhost:8000/docs
   - Interactive API documentation

---

## 🎮 Quick Demo (3 min)

### Test 1: Upload Template

1. Click **"Upload Document"** (top right)
2. Use `backend/samples/insurance_notice_sample.md`
3. Wait for AI extraction (~10 seconds)
4. Review variables
5. Click **"Save Template"**

### Test 2: Draft Document

1. In Chat tab, type: `Draft a notice to insurer`
2. Click or type `yes` when template matches
3. Answer questions:
   - Policy number: `POL-123456`
   - Claimant name: `John Doe`
   - Date: `2025-12-25`
   - Amount: `100000`
4. Get complete draft!

---

## 🐛 Common Issues

### "Module not found"
```powershell
# Make sure venv is activated:
cd backend
.\venv\Scripts\Activate.ps1
```

### "Port already in use"
```powershell
# Backend: Change port
uvicorn app.main:app --reload --port 8001

# Frontend: Change port
npm run dev -- -p 3001
```

### "GEMINI_API_KEY not configured"
```powershell
# Check .env file exists and has valid key:
cd backend
cat .env
```

### "Cannot connect to API"
- Verify backend is running on port 8000
- Check `frontend/.env.local` has: `NEXT_PUBLIC_API_URL=http://localhost:8000`

---

## 📚 Next Steps

- Read **DEMO_GUIDE.md** for complete demo walkthrough
- Read **README.md** for detailed documentation
- Check **SUBMISSION.md** for technical details
- Explore API docs at http://localhost:8000/docs

---

## 🎯 Key Features to Try

- ✅ Upload DOCX/PDF documents
- ✅ AI variable extraction
- ✅ Natural language drafting
- ✅ Template matching
- ✅ Smart Q&A flow
- ✅ Web search (bonus - needs EXA_API_KEY)
- ✅ Slash commands: `/draft`, `/vars`
- ✅ Export templates as Markdown

---

## 📧 Need Help?

Check these in order:
1. DEMO_GUIDE.md - Troubleshooting section
2. README.md - Detailed setup
3. API Docs - http://localhost:8000/docs

---

**Built by UOIONHHC** 🚀

*Happy drafting!*
