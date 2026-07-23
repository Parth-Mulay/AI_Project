# AI Meeting Notes Manager

An intelligent, full-stack meeting notes management system powered by rule-based NLP. Captures meetings, extracts action items and decisions, detects risks, generates summaries, and exports professional documentation — all with **zero external API cost**.

---

## Project Overview

The AI Meeting Notes Manager helps teams efficiently capture, organize, and extract insights from meeting recordings and documents. Built over 14 days as a capstone project, it demonstrates professional software architecture, resilient backend engineering, multi-layer quality testing, and a zero-cost cloud deployment strategy.

**Status**: ✅ Complete (Day 14 of 14)

---

## Features

- **Meeting Capture**: Live note-taking with speaker attribution
- **Document Upload**: Process .txt, .docx, .pdf, .mp3, .wav files
- **AI-Powered Analysis**: Rule-based NLP extracts action items, decisions, risks, and summaries
- **Action Item Tracking**: Auto-detected tasks with owner, deadline, and priority
- **Decision Logging**: Key decisions captured with context
- **Risk Detection**: Identifies risks, blockers, and concerns
- **Export**: Professional Markdown exports
- **Full-Text Search**: Search across meeting titles and transcripts
- **Web Dashboard**: Professional SPA dashboard (React + Vite + static HTML)
- **REST API**: FastAPI backend with CORS configuration
- **CI/CD**: GitHub Actions automated testing and build verification
- **Zero-Cost Deployment**: Vercel (frontend) + Render (backend) + UptimeRobot (monitoring)

---

## Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React 18, Vite, HTML5, CSS3, JavaScript (ES6+) |
| **Backend** | Python 3.12, FastAPI, Uvicorn |
| **AI/NLP** | spaCy, NLTK, dateparser, rule-based keyword detection |
| **Database** | SQLAlchemy ORM, SQLite |
| **Testing** | pytest (unit, integration, E2E) |
| **CI/CD** | GitHub Actions |
| **Deployment** | Vercel (frontend), Render (backend) |
| **Monitoring** | UptimeRobot, structured logging |
| **AI Cost** | $0.00/month (rule-based, no external APIs) |

---

## Architecture

```
┌──────────────────────────────────────────────┐
│          Application Layer (main.py)          │
│         MeetingNotesManager (app.py)          │
├──────────────────────────────────────────────┤
│              Services Layer                   │
│  ┌──────────────┐  ┌──────────────────────┐  │
│  │ MeetingService│  │    DetectionService   │  │
│  │ ExportService │  │  SummarizationService │  │
│  └──────────────┘  └──────────────────────┘  │
├──────────────────────────────────────────────┤
│               AI / NLP Layer                  │
│  ┌──────────┐ ┌───────────┐ ┌───────────┐   │
│  │Keyword   │ │ NLP       │ │LLM Service│    │
│  │Detector  │ │ Pipeline  │ │(Fallback) │    │
│  └──────────┘ └───────────┘ └───────────┘   │
├──────────────────────────────────────────────┤
│              Multi-Agent Pipeline             │
│  Agent 1 → Agent 2 → Agent 3 → Agent 4       │
│  (Ingestion → Processing → Refinement → Output)│
├──────────────────────────────────────────────┤
│              Data Layer                       │
│  ┌────────────────────────────────────────┐  │
│  │  SQLAlchemy ORM → SQLite Database      │  │
│  └────────────────────────────────────────┘  │
├──────────────────────────────────────────────┤
│              Utility Layer                    │
│  ┌──────────┐ ┌──────────┐ ┌────────────┐   │
│  │ Logger   │ │Formatter │ │File Handler│   │
│  └──────────┘ └──────────┘ └────────────┘   │
└──────────────────────────────────────────────┘
```

### Deployment Architecture

```
Users ──▶ Vercel CDN (React SPA) ──▶ Render (FastAPI) ──▶ SQLite
              │                            │
         GitHub Actions              UptimeRobot
         (CI/CD)                     (Monitoring)
```

---

## Folder Structure

```
AI-Meeting-Notes-Manager/
├── src/
│   ├── main.py                    # Entry point
│   ├── app.py                     # Core MeetingNotesManager class
│   ├── server.py                  # FastAPI REST API server
│   ├── config.py                  # Project configuration
│   ├── persistence.py             # SQLAlchemy ↔ domain model bridge
│   ├── document_extraction.py     # File text extraction helpers
│   ├── ai/                        # AI/LLM abstraction layer
│   ├── agents/                    # Multi-agent pipeline (4 agents)
│   ├── audio/                     # Audio transcription
│   ├── database/                  # SQLAlchemy ORM (models, session, schema)
│   ├── models/                    # Domain models (Meeting, ActionItem, etc.)
│   ├── nlp/                       # NLP pipeline (spaCy, regex)
│   ├── services/                  # Business logic services
│   ├── utils/                     # Logger, formatter, keyword detector
│   └── web/                       # Static HTML/CSS/JS dashboard
├── backend/
│   ├── ai/                        # LLM providers, guardrails, RAG, cost estimator
│   └── core/                      # Structured logging configuration
├── frontend/
│   ├── src/                       # React components and pages
│   ├── components/                # Reusable UI components
│   ├── pages/                     # Page-level components
│   └── styles/                    # CSS design system
├── tests/
│   ├── unit/                      # Unit tests (12 files)
│   ├── integration/               # Integration tests (5 files)
│   └── e2e/                       # End-to-end tests (1 file)
├── .github/workflows/ci.yml       # GitHub Actions CI/CD
├── render.yaml                    # Render Blueprint deployment config
├── frontend/vercel.json           # Vercel SPA deployment config
├── .env.example                   # Backend environment template
├── frontend/.env.example          # Frontend environment template
├── Day1_Docs/..Day14_Docs/        # 14-day capstone documentation
└── tests/                         # 218+ automated tests
```

---

## Installation

### Prerequisites

- Python 3.8+
- Node.js 20+
- pip (Python package manager)
- npm or yarn

### Setup

```bash
# Clone the repository
git clone https://github.com/Parth-Mulay/AI_Project.git
cd AI-Meeting-Notes-Manager

# Create and activate virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Environment Variables

```bash
# Backend
cp .env.example .env

# Frontend
cp frontend/.env.example frontend/.env
```

See [Day13_Docs/02_Environment_Variables.md](Day13_Docs/02_Environment_Variables.md) for the complete reference.

---

## Running Locally

### CLI Application

```bash
python src/main.py
```

### FastAPI Server

```bash
uvicorn src.server:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` for the API, or `http://localhost:8000/static/` for the web dashboard.

### Frontend Development Server

```bash
cd frontend
npm run dev
```

Open `http://localhost:3000` for the React app.

### Demo Script

```bash
python demo.py
```

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test suites
pytest tests/unit/ -v           # Unit tests
pytest tests/integration/ -v    # Integration tests
pytest tests/e2e/ -v            # End-to-end tests

# Run with coverage
pytest tests/ -v --cov=src
```

Total: **218+ tests** across unit, integration, and E2E layers.

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/meetings` | List all meetings |
| `GET` | `/api/v1/meetings/{id}` | Get meeting details |
| `DELETE` | `/api/v1/meetings/{id}` | Delete a meeting |
| `POST` | `/api/v1/upload` | Upload a document |
| `GET` | `/api/v1/meetings/{id}/export` | Export meeting as Markdown |

---

## Deployment

### Frontend (Vercel)

```bash
cd frontend
npm run build
# Deploy dist/ to Vercel
```

### Backend (Render)

Push to `main` branch — `render.yaml` auto-deploys the FastAPI server.

### CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request:
1. Backend tests (pytest)
2. Frontend build verification (Vite)

For detailed deployment instructions, see [Day13_Docs/06_Deployment_Runbook.md](Day13_Docs/06_Deployment_Runbook.md).

---

## Cost

| Component | Provider | Monthly Cost |
| :--- | :--- | :--- |
| Frontend Hosting | Vercel Free | $0.00 |
| Backend Hosting | Render Free | $0.00 |
| Database | SQLite (embedded) | $0.00 |
| CI/CD | GitHub Actions Free | $0.00 |
| Monitoring | UptimeRobot Free | $0.00 |
| AI Inference | Rule-based NLP | $0.00 |
| **Total** | | **$0.00/month** |

---

## Screenshots

### CLI Dashboard
```
┌──────────────────────────────────────────────────────────────┐
│              AI MEETING NOTES MANAGER                        │
│           Workspace Dashboard | Role: MEMBER                 │
├──────────────────────────────────────────────────────────────┤
│  STATS: [⏱ Saved: 7.5 hrs]  [📝 Meetings: 3]  [🎯 Pending: 3]│
├──────────────────────────────────────────────────────────────┤
│  [1] 📝 Start Live Meeting Capture                           │
│  [2] 📤 Upload Meeting Audio / Documents                     │
│  [3] 📂 View Meeting History & Archive                       │
│  [4] 🔍 Search Past Meetings                                 │
│  [5] 👥 Team Workspace & RBAC Settings                      │
│  [6] ⚙ System Settings & Integrations                      │
│  [7] 📖 Onboarding Guide / UI-UX Tour                       │
│  [8] ❌ Exit Application                                     │
│  [9] 🌐 Open Professional Web Dashboard                     │
├──────────────────────────────────────────────────────────────┤
│  Alert Log: [🔔] AI Summary generated for '...'              │
└──────────────────────────────────────────────────────────────┘
```

### Web Dashboard
The professional web dashboard (React SPA + static HTML) features:
- Dashboard hub with metrics cards and recent meetings
- Drag-and-drop file upload with processing pipeline
- Searchable archive with tabbed detail views
- Team workspace with RBAC controls

---

## Future Scope

- **External LLM Integration**: Enable OpenAI/Anthropic/Gemini providers for enhanced summaries
- **PostgreSQL**: Replace SQLite for production persistence
- **Authentication**: JWT/OAuth user login
- **Real-Time Transcription**: WebSocket support for live meetings
- **Cloud Storage**: S3/R2 for uploaded files
- **Mobile App**: React Native companion
- **Calendar Integration**: Google Calendar, Outlook
- **Slack Integration**: Automated meeting notifications
- **Analytics Dashboard**: Meeting trends, participation metrics

---

## Project Timeline

| Day | Phase | Deliverables |
| :--- | :--- | :--- |
| 1-2 | Discovery & AI Fundamentals | User research, Python basics, prompt engineering |
| 3 | Product Thinking | MVP decisions, competitor research |
| 4 | Requirements & PRD | User stories, acceptance criteria, MoSCoW |
| 5 | UI/UX Prototyping | Design system, wireframes, Figma |
| 6 | Client Proposal | Proposal, effort estimation, sign-off |
| 7 | React Frontend | Components, pages, styling |
| 8 | Integration | Frontend-backend wiring, API connectivity |
| 9 | Database Design | SQLAlchemy schema, persistence |
| 10 | AI Architecture | LLM abstraction, guardrails, RAG |
| 11 | Debugging & Resilience | Logging, error handling, fixes |
| 12 | QA & Testing | 218+ tests, security audit, UAT |
| 13 | Deployment & DevOps | CI/CD, Vercel, Render, monitoring |
| 14 | Capstone Completion | Cost audit, verification, handover |

---

## Author

**Parth Mulay**
- AI Software Engineering Internship Capstone Project
- GitHub: [Parth-Mulay/AI_Project](https://github.com/Parth-Mulay/AI_Project)

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Documentation Index

| Phase | Documentation |
| :--- | :--- |
| Day 1 | [Discovery & Planning](Day1_Docs/) |
| Day 2 | [AI-Assisted Development](Day2_Docs/) |
| Day 3 | [Product Thinking & MVP](Day3_Docs/) |
| Day 4 | [Requirements & PRD](Day4_Docs/) |
| Day 5 | [UI/UX Prototyping](Day5_Docs/) |
| Day 6 | [Client Proposal & Sign-off](Day6_Docs/) |
| Day 7 | [React Frontend](Day7_Docs/) |
| Day 8 | [Integration](Day8_Docs/) |
| Day 9 | [Database Design](Day9_Docs/) |
| Day 10 | [AI Architecture](Day10_Docs/) |
| Day 11 | [Debugging & Resilience](Day11_Docs/) |
| Day 12 | [QA & Testing](Day12_Docs/) |
| Day 13 | [Deployment & DevOps](Day13_Docs/) |
| Day 14 | [Capstone Completion](Day14_Docs/) |
