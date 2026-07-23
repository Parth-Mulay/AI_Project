# Demo Guide

## Overview

This demo guide walks through the complete workflow of the **AI Meeting Notes Manager**. It is designed for prospective users, evaluators, and stakeholders to understand the application's capabilities.

---

## 1. Application Workflow

```
User Input ──> Text Extraction ──> NLP Pipeline ──> Analysis Results ──> Export
                                                 │
                           ┌─────────────────────┼─────────────────────┐
                           ▼                     ▼                     ▼
                      Action Items          Decisions             Summary
                      + Owners              + Context             + Key Points
                      + Deadlines
```

---

## 2. Features to Demonstrate

### 2.1 Meeting Creation & Live Capture

Start a new meeting, add participants, and record messages in real time. AI detects insights as you type.

**To demonstrate**:
1. Launch the application
2. Select option **[1] Start Live Meeting Capture**
3. Enter title: "Sprint Planning - Week 16"
4. Enter participants: "Alice, Bob, Charlie"
5. Type messages one by one

### 2.2 Real-Time AI Insight Detection

As each message is entered, the system detects:
- **Action Items**: Messages containing "will", "need to", "must", "assign"
- **Decisions**: Messages containing "decided", "agreed", "approved"
- **Important Notes**: Messages containing "risk", "blocker", "concern"

**Expected output**: Each message shows detected insight type with AI badge indicator.

### 2.3 Document Upload & Analysis

Upload meeting transcripts in .txt, .docx, .pdf, .mp3, or .wav format for automatic processing.

**To demonstrate**:
1. Select option **[2] Upload Meeting Audio / Documents**
2. Enter path to a sample .txt file
3. Watch the AI processing stages
4. Review extracted summary, action items, decisions, and risks

### 2.4 Meeting History & Archive

View all processed meetings with details.

**To demonstrate**:
1. Select option **[3] View Meeting History & Archive**
2. Select a meeting
3. Browse tabs: Summary, Action Items, Decisions, Transcript
4. Export to Markdown

### 2.5 Search

Search across meeting titles and transcripts.

**To demonstrate**:
1. Select option **[4] Search Past Meetings**
2. Enter keyword: "security"
3. Review matching results

### 2.6 Team Workspace & RBAC

Toggle between Member and Admin roles to test access controls.

**To demonstrate**:
1. Select option **[5] Team Workspace & RBAC Settings**
2. Toggle role to Admin
3. Access Security Audit Logs
4. Toggle back to Member and verify access is denied

### 2.7 System Settings

Configure data retention, Slack integration, and API fallback simulation.

**To demonstrate**:
1. Select option **[6] System Settings & Integrations**
2. Toggle API Fallback Mode
3. Start a meeting and observe fallback behavior

### 2.8 Web Dashboard

Open the professional web-based dashboard.

**To demonstrate**:
1. Select option **[9] Open Professional Web Dashboard**
2. Browser opens with full SPA dashboard
3. Navigate through dashboard, upload, archive, and settings views

---

## 3. Demo Script (15 minutes)

### Setup (2 minutes)

```bash
# From project root
python src/main.py
```

### Walkthrough (10 minutes)

| Step | Action | Expected Result | Time |
| :--- | :--- | :--- | :--- |
| 1 | App starts | Dashboard menu displays | 30s |
| 2 | Option [3] - View History | 3 demo meetings listed | 1 min |
| 3 | Select meeting 1 - View Summary | AI-generated summary shown | 1 min |
| 4 | View Action Items tab | 2+ action items with owners | 1 min |
| 5 | View Decisions tab | Decisions with context | 1 min |
| 6 | Export to Markdown | File created successfully | 1 min |
| 7 | Option [4] - Search "deployment" | Matching meetings found | 1 min |
| 8 | Option [1] - Start new meeting | Create and capture messages | 2 mins |
| 9 | Type messages with insights | AI badges appear | 2 mins |
| 10 | End meeting | Summary and export generated | 1 min |
| 11 | Option [9] - Web Dashboard | Browser opens SPA | 1 min |

### Conclusion (3 minutes)

- Summarize key features demonstrated
- Review architecture
- Discuss deployment and DevOps pipeline
- Answer questions

---

## 4. Sample Input Messages

Use these messages during the live demo for reliable AI insight detection:

```
Alice: We need to complete the authentication module by Friday.
Bob: I agreed to adopt the new design system.
Charlie: Risk identified - the deployment server has limited resources.
Alice: I will write the migration scripts before launch.
Bob: We decided to use JWT for token management.
Charlie: We must finish the API documentation by Monday.
```

**Expected detected insights**:
- Action Item: "complete the authentication module by Friday" (Owner: Alice)
- Decision: "agreed to adopt the new design system"
- Risk: "deployment server has limited resources"
- Action Item: "write the migration scripts" (Owner: Alice)
- Decision: "use JWT for token management"
- Action Item: "finish the API documentation by Monday" (Owner: Charlie)

---

## 5. Expected Outputs

### Console Output (CLI)

After processing the sample messages:

```
Summary:
Key points discussed:
• We need to complete the authentication module by Friday.
• I agreed to adopt the new design system.
• Risk identified - the deployment server has limited resources.

Action Items:
  🎯 Complete the authentication module by Friday. (Friday) - Alice
  🎯 I will write the migration scripts before launch. - Alice
  🎯 We must finish the API documentation by Monday. (Monday) - Charlie

Decisions:
  ✓ I agreed to adopt the new design system.
  ✓ We decided to use JWT for token management.

Important Notes:
  ⚠️ Risk identified - the deployment server has limited resources. [RISK]
```

### Exported Markdown File

A professionally formatted Markdown file is created in the `meeting_notes/` directory with full meeting content, metadata, transcript, action items, decisions, and statistics.

---

## 6. Web Dashboard Screenshots

The web-based SPA dashboard includes:
- **Dashboard**: Metrics cards, recent meetings, priority checklist
- **Upload**: Drag-and-drop file upload with processing pipeline
- **Archive**: Searchable meeting history with tabbed detail views
- **Settings**: Retention controls, Slack integration toggles

(Refer to `src/web/` for the full static dashboard implementation.)
