# AI Meeting Notes Manager – Working Prototype

**Day 3 of a 14-Day AI Software Engineering Internship Capstone Project**

A professional, rule-based meeting assistant that demonstrates intelligent meeting note-taking without requiring expensive APIs.

## 🎯 Overview

This is a **working prototype** that simulates an AI meeting notes manager. It demonstrates the core workflow of a real meeting assistant while using simple rule-based keyword detection instead of LLMs.

**Perfect for**: Product demonstrations, capstone evaluations, and showcase presentations.

**Key Benefit**: Fully functional without API costs – uses only Python standard library.

---

## ✨ Features

### 1. **Smart Meeting Management**
- Create meetings with title and participants
- Real-time conversation input
- Continuous message tracking with timestamps

### 2. **Live AI Insight Detection** 🤖
Automatically detects and displays:
- **Action Items** – "will", "need to", "should", "complete by Friday"
- **Decisions** – "approved", "decided", "agreed", "finalized"
- **Important Notes** – "risk", "issue", "blocker", "reminder"

Each detection displays: `🤖 AI Insight: ✓ Action Item Detected`

### 3. **Intelligent Summarization**
- Extracts key points from meetings
- Prioritizes important sentences
- Avoids duplicates
- Creates readable summaries

### 4. **Meeting Transcript**
- Full transcript of all messages
- Speaker attribution
- Timestamp tracking

### 5. **Action Items Tracking**
- Extracted with ownership detection
- Due date recognition (Friday, Tomorrow, ASAP, etc.)
- Checkbox-style markdown export

### 6. **Decision Logging**
- All decisions captured and timestamped
- Context awareness
- Organized in meeting export

### 7. **Important Notes**
- Risk warnings
- Blockers identified
- Reminders captured
- Category-based organization

### 8. **Meeting Statistics**
- Total messages processed
- Insights detected (counts)
- Meeting duration
- Participant count
- Professional formatting with Unicode icons

### 9. **Professional Export**
- Automatic Markdown file generation
- Organized folder structure (`meeting_notes/`)
- Professional formatting
- All insights included

### 10. **Beautiful Console UI**
- Unicode icons (✓, •, 🤖, 📝, 📊, etc.)
- Professional separators
- Color-coded output
- Clear section headers

---

## 🏗️ Architecture

Clean, modular design with clear separation of concerns:

```
src/
├── main.py                          # Entry point
├── app.py                           # Main application class
├── models/
│   └── meeting_model.py             # Data structures
├── services/
│   ├── detection_service.py         # Insight detection & summarization
│   └── export_service.py            # Markdown export
└── utils/
    ├── formatter.py                 # Console formatting
    └── keyword_detector.py          # Rule-based keyword matching
```

### Key Classes

**`Meeting`** – Core data model
- Title, participants, messages
- Action items, decisions, important notes
- Duration tracking

**`DetectionService`** – Intelligent processing
- Rule-based detection of insights
- Duplicate avoidance
- Owner extraction

**`SummarizationService`** – Summary generation
- Key sentence extraction
- Smart prioritization

**`ExportService`** – Professional export
- Markdown generation
- File management

**`ConsoleFormatter`** – Professional UI
- Unicode icons
- Color support
- Consistent formatting

---

## 🚀 Quick Start

### Installation

No special setup needed! Uses only Python standard library.

```bash
# Clone the repository
git clone https://github.com/Parth-Mulay/AI_Project.git
cd AI_Project

# Run the prototype
python src/main.py
```

### Running the Demo

See all features in action with pre-filled demo data:

```bash
python demo.py
```

This demonstrates:
- ✓ Meeting creation
- ✓ Real-time insight detection
- ✓ Summary generation
- ✓ Statistics display
- ✓ Markdown export

---

## 📝 Usage Example

### Interactive Mode

```bash
$ python src/main.py

==================================================
             AI Meeting Notes Manager             
==================================================

Enter Meeting Title: Sprint Planning
Enter Participants (comma separated): Alice, Bob, Charlie

Meeting Started Successfully

==================================================
Live Meeting Notes
==================================================

Enter meeting conversations (type 'end' to finish):

Alice: We need to finish the dashboard by Friday.
🤖 AI Insight: ✓ Action Item Detected

Bob: Approved the new payment gateway.
🤖 AI Insight: ✓ Decision Detected

Charlie: Risk identified with server deployment.
🤖 AI Insight: ✓ Important Note Detected

end
```

### Automatic Processing

After ending the meeting, the app automatically:
1. ✓ Generates summary
2. ✓ Displays action items
3. ✓ Shows decisions made
4. ✓ Lists important notes
5. ✓ Displays statistics
6. ✓ Exports to Markdown file

---

## 🧠 How Intelligence Works

### Rule-Based Detection (No APIs)

**Action Item Keywords:**
```
will, need to, should, must, assign, complete, build, 
review, approve, by Friday, tomorrow, next week, ASAP
```

**Decision Keywords:**
```
decided, approved, agreed, finalized, confirmed, 
accepted, resolved, implemented, adopted, selected
```

**Important Note Keywords:**
```
risk, issue, blocker, problem, concern, reminder, 
note, important, critical, urgent
```

### Smart Parsing

- Extracts speaker names from "Speaker: Message" format
- Detects assigned owners: "Alice will review API"
- Extracts due dates: "by Friday", "tomorrow", "ASAP"
- Avoids duplicate entries
- Prioritizes important sentences for summaries

---

## 📊 Example Output

### Console Display
```
==================================================
Meeting Summary
==================================================

Key points discussed:

• We need to finish dashboard by Friday
• Authentication approved
• Risk: server deployment issues

==================================================
Action Items
==================================================

✓ We need to finish dashboard by Friday (Friday)
✓ Should review API (Tomorrow)

==================================================
Decisions Made
==================================================

• Authentication approach approved

==================================================
Important Notes
==================================================

• [RISK] Deployment server has limited resources
• [REMINDER] Backup data before launch
```

### Exported Markdown

```markdown
# Sprint Planning - Week 15

**Date:** 2026-07-10 12:55:07
**Participants:** Rahul, Priya, Amit, Brian

## Summary
- 6 action items identified
- 1 key decision made
- 2 important notes captured

## Action Items
- [ ] We need to finish dashboard (Due: Friday)
- [ ] Rahul to review API (Due: Tomorrow)

## Decisions
- JWT authentication approved

## Important Notes
- [RISK] Server deployment risk
- [REMINDER] Backup data before launch
```

---

## 🎓 Technical Highlights

### Code Quality
- ✓ PEP 8 compliant
- ✓ Comprehensive docstrings
- ✓ Type hints throughout
- ✓ Clean class design
- ✓ No code duplication

### Production-Ready Features
- ✓ Error handling
- ✓ Input validation
- ✓ Professional logging
- ✓ Graceful degradation
- ✓ Consistent formatting

### Design Patterns
- ✓ Service layer pattern
- ✓ Data model separation
- ✓ Utility modules
- ✓ Formatter abstraction

---

## 📁 Output Structure

Meeting notes are exported to:

```
project_root/
├── meeting_notes/
│   ├── Sprint_Planning_Week_15_20260710_125507.md
│   ├── Team_Standup_20260710_120000.md
│   └── ... (more meeting files)
```

Each file is named: `{MeetingTitle}_{Timestamp}.md`

---

## 🎬 Demo Features

Run `python demo.py` to see:

1. **Live meeting processing** with 9 sample messages
2. **Real-time detection** of 6 action items, 1 decision, 2 notes
3. **Automatic summary** generation
4. **Professional statistics** display
5. **Markdown file creation** with complete meeting details
6. **Console output** with Unicode formatting

---

## 🔧 Customization

### Add Detection Keywords

Edit `src/utils/keyword_detector.py`:

```python
ACTION_KEYWORDS = {
    "your_keyword": [],
    "another_keyword": [],
}
```

### Change Export Location

Edit `src/services/export_service.py`:

```python
DEFAULT_EXPORT_DIR = "your_folder"
```

### Customize Output Format

Edit `src/utils/formatter.py` for UI changes.

---

## ✅ Testing

Verify all components work:

```bash
python -c "
import sys; sys.path.insert(0, 'src')
from models.meeting_model import Meeting
from services.detection_service import DetectionService
print('✓ All imports successful')
"
```

---

## 📚 Project Status

| Component | Status |
|-----------|--------|
| Meeting creation | ✅ Complete |
| Live note-taking | ✅ Complete |
| Insight detection | ✅ Complete |
| Summary generation | ✅ Complete |
| Statistics | ✅ Complete |
| Markdown export | ✅ Complete |
| Console UI | ✅ Complete |

---

## 🎯 Use Cases

### 1. Product Demonstration
Show stakeholders a working meeting assistant without APIs.

### 2. Capstone Evaluation
Demonstrate software engineering skills:
- Clean architecture
- Professional code
- Modular design
- Production readiness

### 3. Starting Point for Full Implementation
- Replace keyword detection with LLMs
- Add database storage
- Build web interface
- Integrate with calendar APIs

### 4. Learning Resource
Study how to:
- Build rule-based intelligence
- Create professional CLIs
- Design scalable architecture
- Export structured data

---

## 🚀 Future Enhancements

### Phase 2: Full AI Integration
- Replace keyword detection with GPT-4 API
- Real audio transcription (Whisper)
- Advanced NLP processing

### Phase 3: Web Interface
- FastAPI backend
- React frontend
- Database storage (PostgreSQL)
- User authentication

### Phase 4: Enterprise Features
- Meeting calendar integration
- Team collaboration
- Advanced analytics
- Multi-language support

---

## 👨‍💻 Author

**Parth Mulay**
- AI Software Engineering Internship Capstone Project
- GitHub: [Parth-Mulay/AI_Project](https://github.com/Parth-Mulay/AI_Project)

---

## 📄 License

MIT License – See LICENSE file for details.

---

## 📞 Support

For questions or issues:
- Check [Day1_Docs/](Day1_Docs/) for product requirements
- Check [Day2_Docs/](Day2_Docs/) for AI fundamentals
- Check [Day3_Docs/](Day3_Docs/) for architecture documentation

---

## 🎉 Summary

This prototype demonstrates:
- ✓ **Intelligent meeting assistance** without expensive APIs
- ✓ **Professional software architecture** ready for scale
- ✓ **Production-quality code** suitable for enterprise use
- ✓ **Complete feature set** for demonstration purposes
- ✓ **Clean, maintainable design** for future development

**Status**: Ready for presentation and evaluation ✅

---

*Last Updated: 2026-07-10*  
*Version: 0.2.0 - Working Prototype*
