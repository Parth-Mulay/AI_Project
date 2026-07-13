# AI Meeting Notes Manager

**Architecture Setup – Day 3 of a 14-Day AI Software Engineering Internship Capstone Project**

## Project Overview

The AI Meeting Notes Manager is an intelligent solution designed to help teams efficiently capture, organize, and extract insights from meeting recordings. This project demonstrates professional software architecture and clean coding practices with a focus on scalability and maintainability.

**Current Phase:** Frontend component development (Day 7)
**Status:** ✅ Complete - Day 7 React Frontend Components & Learning Docs Done


---

## Planned Features

The following features are planned for implementation in future phases:

- **Audio Transcription**: Convert meeting recordings to text transcripts
- **Intelligent Summarization**: AI-powered meeting summary generation
- **Action Item Extraction**: Automatically identify and extract action items
- **Export Capabilities**: Export meeting notes to PDF, Markdown, and DOCX formats
- **Participant Tracking**: Track meeting participants and their contributions
- **Search & Retrieval**: Full-text search across meeting archives
- **Integration Support**: API integrations with calendar and productivity tools

---

## Project Architecture

The project follows clean architecture principles with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│        Application Layer (main.py)      │
├─────────────────────────────────────────┤
│      MeetingNotesManager (app.py)       │
├─────────────────────────────────────────┤
│         Business Logic Layer            │
│  ┌──────────────────────────────────┐   │
│  │    Services                      │   │
│  │  • MeetingService               │   │
│  │  • ExportService                │   │
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│         Core Modules                    │
│  ┌──────────────────────────────────┐   │
│  │    AI Module                     │   │
│  │  • Summarizer                   │   │
│  │  • ActionItemExtractor          │   │
│  │  • Prompts                      │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │    Audio Module                 │   │
│  │  • Transcriber                  │   │
│  │  • AudioUtils                   │   │
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│         Data Layer                      │
│  ┌──────────────────────────────────┐   │
│  │    Models                        │   │
│  │  • Meeting                       │   │
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│         Utility Layer                   │
│  ┌──────────────────────────────────┐   │
│  │  • Logger                        │   │
│  │  • FileHandler                   │   │
│  │  • Config                        │   │
│  └──────────────────────────────────┘   │
```

---

## Folder Structure

```
AI-Meeting-Notes-Manager/
│
├── src/
│   ├── main.py                    # Application entry point
│   ├── app.py                     # Core MeetingNotesManager class
│   ├── config.py                  # Project configuration
│   │
│   ├── ai/                        # AI/ML modules
│   │   ├── summarizer.py          # Meeting summarization
│   │   ├── action_items.py        # Action item extraction
│   │   └── prompts.py             # AI prompts and templates
│   │
│   ├── audio/                     # Audio processing modules
│   │   ├── transcriber.py         # Audio to text transcription
│   │   └── audio_utils.py         # Audio utility functions
│   │
│   ├── models/                    # Data models
│   │   └── meeting.py             # Meeting class definition
│   │
│   ├── services/                  # Business logic services
│   │   ├── meeting_service.py     # Meeting management service
│   │   └── export_service.py      # Export functionality
│   │
│   └── utils/                     # Utility modules
│       ├── logger.py              # Logging configuration
│       └── file_handler.py        # File operations
│
├── tests/                         # Test suite
│   └── test_structure.py          # Architecture tests
│
├── Day3_Docs/                     # Day 3 documentation
├── Day1_Docs/                     # Day 1 artifacts
├── Day2_Docs/                     # Day 2 artifacts
│
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
├── LICENSE                        # MIT License
└── .env.example                   # Environment variables template
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Parth-Mulay/AI_Project.git
   cd AI-Meeting-Notes-Manager
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

---

## Running the Project

### Start the Application
```bash
python src/main.py
```

**Expected Output:**
```
==================================================

        AI MEETING NOTES MANAGER

Architecture Initialized Successfully

Day 3 Product Thinking Completed

==================================================

Initialized Modules:

✓ Audio Processing (Transcriber)
✓ AI Summarization (MeetingSummarizer)
✓ Action Item Extraction (ActionItemExtractor)
✓ Meeting Management (MeetingService)
✓ Export Services (PDF, Markdown, DOCX)
✓ Logging & Utilities

==================================================

Status: Ready for Development

Version: 0.1.0
Author: Parth Mulay

Project: An intelligent meeting notes management system powered by AI

==================================================
```

### Run Tests
```bash
pytest tests/ -v
```

Or run specific test:
```bash
pytest tests/test_structure.py -v
```

---

## Current Status

### ✅ Day 3 – Architecture Setup (Complete)

**Completed:**
- ✓ Professional project structure created
- ✓ Clean architecture design implemented
- ✓ All core modules initialized with placeholder implementations
- ✓ Service layer established
- ✓ Logging system configured
- ✓ Test suite created
- ✓ Documentation generated
- ✓ Project runs successfully without errors

**Modules Implemented:**
- ✓ Configuration management
- ✓ Audio processing (Transcriber, AudioUtils)
- ✓ AI services (Summarizer, ActionItemExtractor)
- ✓ Meeting management service
- ✓ Export service (Markdown, PDF, DOCX)
- ✓ Logging and file handling utilities
- ✓ Data models (Meeting)

---

## Day 1 – Product Discovery & Planning

The first phase focused on understanding the problem domain, identifying target users, defining project requirements, and establishing the product vision.

### Documentation

- [Project Overview](Day1_Docs/PROJECT_OVERVIEW.md)
- [Problem Statement](Day1_Docs/PROBLEM_STATEMENT.md)
- [Target Users](Day1_Docs/TARGET_USERS.md)
- [User Personas](Day1_Docs/USER_PERSONAS.md)
- [User Journey](Day1_Docs/USER_JOURNEY.md)
- [Market Research](Day1_Docs/MARKET_RESEARCH.md)
- [Competitor Analysis](Day1_Docs/COMPETITOR_ANALYSIS.md)
- [Functional Requirements](Day1_Docs/FUNCTIONAL_REQUIREMENTS.md)
- [Non-Functional Requirements](Day1_Docs/NON_FUNCTIONAL_REQUIREMENTS.md)
- [Project Scope](Day1_Docs/PROJECT_SCOPE.md)
- [Success Metrics](Day1_Docs/SUCCESS_METRICS.md)
- [Day 1 Summary](Day1_Docs/DAY1_SUMMARY.md)

---

## Day 2 – AI-Assisted Development Fundamentals

The second phase focused on AI-assisted software development practices, prompt engineering techniques, Python fundamentals, and practical implementation exercises.

### Documentation

- [Python Fundamentals](Day2_Docs/PYTHON_FUNDAMENTALS.md)
- [Prompt Engineering](Day2_Docs/PROMPT_ENGINEERING.md)
- [Project Context Experiment](Day2_Docs/PROJECT_CONTEXT_EXPERIMENT.md)
- [Code Review](Day2_Docs/CODE_REVIEW.md)
- [Explain Then Generate](Day2_Docs/EXPLAIN_THEN_GENERATE.md)
- [Token & Cost Optimization](Day2_Docs/TOKEN_COST.md)
- [Day 2 Summary](Day2_Docs/DAY2_SUMMARY.md)

### Practice Files

- [python_basics.py](Day2_Docs/python_basics.py)
- [prompt_examples.py](Day2_Docs/prompt_examples.py)
- [meeting_notes_demo.py](Day2_Docs/meeting_notes_demo.py)
- [word_counter.py](Day2_Docs/word_counter.py)
- [my_version.py](Day2_Docs/my_version.py)

---

## Day 3 – Product Thinking & MVP Design Decisions

The third phase focused on product ideation, user research, competitor evaluation, and defining MVP design choices for rule-based analysis.

### Documentation

- [Product Ideation Research](Day3_Docs/01_Product_Ideation_Research.md)
- [User Research & Persona Study](Day3_Docs/02_User_Research_and_Persona_Study.md)
- [Competitor Research](Day3_Docs/03_Competitor_Research.md)
- [MVP Design Decisions](Day3_Docs/04_MVP_Design_Decisions.md)
- [Product Thinking Learnings](Day3_Docs/05_Product_Thinking_Learnings.md)
- [Research References](Day3_Docs/06_Research_References.md)
- [Day 3 Readme](Day3_Docs/README.md)

---

## Day 4 – Requirements Analysis & Product Requirements

The fourth phase focused on creating high-fidelity product requirements, user stories, acceptance criteria, priority modeling, gap analysis, and trace mapping.

### Documentation

- [01 User Stories](Day4_Docs/01_User_Stories.md)
- [02 Acceptance Criteria](Day4_Docs/02_Acceptance_Criteria.md)
- [03 MoSCoW Prioritization](Day4_Docs/03_MoSCoW_Prioritization.md)
- [04 Requirement Gap Analysis](Day4_Docs/04_Requirement_Gap_Analysis.md)
- [05 Product Requirements Document (PRD)](Day4_Docs/05_Product_Requirements_Document.md)
- [06 Requirement Traceability Matrix](Day4_Docs/06_Requirement_Traceability_Matrix.md)
- [07 Verification Checklist](Day4_Docs/07_Verification_Checklist.md)

### Technical Metadata

System-parsable requirements schemas are saved in the `docs/requirements/` directory:
- [Requirements Index JSON](docs/requirements/requirements_index.json)
- [User Stories JSON](docs/requirements/user_stories.json)
- [Acceptance Criteria JSON](docs/requirements/acceptance_criteria.json)
- [Feature Priority JSON](docs/requirements/feature_priority.json)
- [Traceability JSON](docs/requirements/traceability.json)

---

## Day 5 – UI/UX Prototyping & Design System

The fifth phase focused on translating requirements into a modern SaaS user interface design, outlining the style system, mapping screen flows, and upgrading the CLI prototype to an interactive multi-screen console dashboard.

### Documentation

- [01 Design System](Day5_Docs/01_Design_System.md)
- [02 User Flow & Wireframe Notes](Day5_Docs/02_User_Flow_and_Wireframe_Notes.md)
- [03 Figma AI Prompts & Prototype Notes](Day5_Docs/03_Figma_AI_Prompts_and_Prototype_Notes.md)
- [04 Screen Traceability Matrix](Day5_Docs/04_Screen_Traceability.md)
- [05 Design Decisions Rationale](Day5_Docs/05_Design_Decisions.md)

### Prototype & Analysis Upgrades

- **Dynamic Analysis Pipeline:** Fully replaced hardcoded meeting outcomes with a dynamic standard-library content processing engine supporting `.docx`, `.pdf`, `.txt`, `.mp3`, and `.wav` formats.
- **Granular Insight Extraction:** Added rule-based parsers that extract participants, chronologically indexed dialogue messages, decisions (e.g. `agreed`, `approved`), action checklists (capturing owner and due dates), next steps, risks, and executive summaries.
- **Robust File Validation:** Enforces max file limits (10MB for documents, 100MB for audio), detects empty documents, catches corruption exceptions, and identifies password-protected files.
- **Verification Tests:** Added a dedicated test suite [test_document_analysis.py](tests/test_document_analysis.py) asserting schema safety, extraction reliability, and proper validation handling.

### Professional Web Dashboard Prototype

We have implemented a responsive, high-fidelity web user interface matching the Figma mockup layout specifications inside [src/web/](src/web/):
- **Separate View Templates:** Refactored the dashboard layout into isolated HTML5 state-synchronized screens:
  - [dashboard.html](src/web/dashboard.html): Dashboard hub displaying metrics cards, recent meetings list, and priority checklist filter tabs. Contains responsive native SVG graphs (Time Trend splines with hover tooltips, Meetings by Category segmented donuts, and Actions Completion dials).
  - [live.html](src/web/live.html): In-browser recording cockpit with live typing note analyzers and real-time AI outcome checklists.
  - [upload.html](src/web/upload.html): File uploader drag-and-drop zone featuring multi-stage analysis pipeline loader timelines.
  - [archive.html](src/web/archive.html): Grid database search and filter indexing with tab-panel views (Summary, Action Items, Timeline Transcripts) and Markdown download export helpers.
  - [directory.html](src/web/directory.html): Workspace user lists and password-overlay gated Security Audit Logs.
  - [settings.html](src/web/settings.html): Gated Compliance retention rules sliders and Slack webhook integrations.
  - [onboarding.html](src/web/onboarding.html): Design tour explainability cards.
  - [index.html](src/web/index.html): Redirect page forwarding browser requests to `dashboard.html`.
- **Styling Design System ([style.css](src/web/style.css)):** Implements the matte glassmorphic panels, dark gradients, geometric scales, pulsed record indicators, and custom `@keyframes spin` loading animations.
- **Stateful Storage Sync ([app.js](src/web/app.js)):** Coordinates SPA routing, dynamic file reading, live note extraction, and browser-wide `localStorage` sync that matches role and notifications across views.
- **Google Material Symbols:** Replaced primitive system emojis with professional Outlined vector icons for sidebars, cards, and pipelines.

To run, simply open [index.html](src/web/index.html) inside any standard web browser.

---

## Day 6 – Client Proposal & Project Sign-Off

The sixth phase focused on preparing all corporate communication, project proposal, effort estimation, and approval materials to secure client sign-off prior to launching full-scale implementation.

### Documentation

- [01 Client Proposal](Day6_Docs/01_Client_Proposal.md): Detailed consulting proposal containing executive summary, scope boundaries, timeline milestones, and risk assessment.
- [02 Client-Friendly PRD](Day6_Docs/02_Client_Friendly_PRD.md): Simplified requirements detailing business ROI, team productivity gains, and Continuous Offline Service Protection.
- [03 Effort Estimation](Day6_Docs/03_Effort_Estimation.md): Multi-phase development breakdown (Discovery, Design, AI, DB, QA, Buffer) with explicit resource assumptions.
- [04 Demo Script](Day6_Docs/04_Demo_Script.md): Speaking guide and click-by-click presenter workflow for live client system demonstrations.
- [05 Client FAQ & Objection Handling](Day6_Docs/05_Client_FAQ_and_Objections.md): Reassuring answers resolving security, scale, accuracy, offline capability, and integration objections.
- [06 Project Sign-Off Checklist](Day6_Docs/06_Project_Signoff_Checklist.md): Official document mapping requirements approval and stakeholder signature blocks.
- [07 Follow-Up Email Template](Day6_Docs/07_Followup_Email.md): Email draft summarizing walkthrough outcomes, client decisions, and immediate next steps.

---

## Day 7 – React Frontend Component Development

The seventh phase focused on converting the approved Figma design and Design System into stateful, reusable React frontend components, while documentation of web and React development fundamentals was created.

### Documentation

- [01 Frontend Fundamentals](Day7_Docs/01_Frontend_Fundamentals.md): Principles of HTML5 semantic structure, CSS box models, Flexbox, Grid layouts, responsive breakpoints, media queries, CSS variables, and WCAG AA accessibility.
- [02 React Fundamentals](Day7_Docs/02_React_Fundamentals.md): Details on functional components, JSX syntax, props data flow, state, controlled forms, hook cycles (`useState`, `useEffect`), communication models, and folder architectures.
- [03 Code Review and Refactoring](Day7_Docs/03_Code_Review_and_Refactoring.md): Design decisions explaining code formatting, variable/hook structures, and reusability.
- [04 AI Code Review](Day7_Docs/04_AI_Code_Review.md): Catalog of three major security and layout pitfalls made by naive AI engines (XSS vectors, insecure state RBAC, and accessibility gaps) and their correct fixes.

### Frontend Application

We have implemented a fully functional React workspace inside the [frontend/](frontend/) folder:
- **Build System:** Vite-based build setup with fast hot-reloading configurations.
- **Styling Tokens:** Separated into `variables.css` (Approved color system, margins, font sizing) and `global.css` (layout structures, responsive mobile menus, custom charts).
- **Reusable Presentation Components:**
  - `Button`: Encapsulates CTA, outline, and AI action gradients with micro-animations.
  - `Input`: Integrates form labeling, error alert spans, and ARIA state labels.
  - `Sidebar`: Nav block containing storage counters and user roles matching the Figma draft.
  - `Navbar` & `SearchBar`: Controlled query box with notifications bell panel dropdowns.
  - `StatCard`: Telemetry cards showing trend wave SVGs.
  - `MeetingCard`: Expandable rows displaying participant stacks and details drawers.
  - `ActionItem`: Active task checklist boxes with priority categories.
- **Interactive SPA Pages:**
  - `Dashboard`: Orchestrates charts, search, and dynamic priority checklist filters.
  - `UploadMeeting`: Controlled upload form incorporating size validation, drag-and-drop triggers, AI analysis pipeline loader simulations, and success output cards.

To install dependencies and start the React app locally:
```bash
cd frontend
npm install
npm run dev
```

---


## Future Roadmap

### Phase 2: Core Implementation
- Implement audio transcription with Whisper API
- Integrate AI summarization with GPT-4
- Develop action item extraction logic
- Build export functionality for all formats

### Phase 3: Web Interface
- Create REST API with FastAPI
- Build frontend with React
- Implement user authentication
- Add database integration (PostgreSQL/MongoDB)

### Phase 4: Advanced Features
- Real-time transcription
- Multi-language support
- Meeting analytics dashboard
- Integration with productivity tools

### Phase 5: Deployment & Optimization
- Docker containerization
- Cloud deployment (AWS/GCP/Azure)
- Performance optimization
- Security hardening

---

## Development Standards

This project adheres to the following standards:

- **Code Style**: PEP 8 compliant
- **Documentation**: Comprehensive docstrings and comments
- **Architecture**: Clean Architecture with separation of concerns
- **Testing**: Unit tests with pytest
- **Logging**: Structured logging throughout
- **Version Control**: Git with meaningful commit messages

---

## Project Management

**Project Type**: AI Software Engineering Capstone
**Duration**: 14 Days
**Phase**: 5/14 (UI/UX Prototyping)
**Timeline**: Days 1-5 Complete, Days 6-14 Upcoming

---

## Technology Stack

- **Language**: Python 3.8+
- **Testing**: pytest
- **Logging**: Python logging
- **Configuration**: python-dotenv
- **Validation**: pydantic
- **Future**: FastAPI, SQLAlchemy, PostgreSQL, React

---

## Author

**Parth Mulay**
- AI Software Engineering Internship Capstone Project
- GitHub: [Parth-Mulay/AI_Project](https://github.com/Parth-Mulay/AI_Project)

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## Contributing

This is a capstone project. Contributions and feedback are welcome!

---

## Support

For questions or issues, please refer to:
- Project Documentation: [Day3_Docs/](Day3_Docs/)
- Previous Phases: [Day1_Docs/](Day1_Docs/) and [Day2_Docs/](Day2_Docs/)

---

**Last Updated**: 2026
**Status**: UI/UX Prototyping Phase Complete ✅
