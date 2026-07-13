# Client FAQs & Objection Handling Guide

This guide compiles common questions, security concerns, and functional inquiries raised by client stakeholders during project walkthroughs.

---

## 1. Security & Compliance

### Q1: How secure is our meeting data? Where is the audio hosted?
> **Answer:** Data security is a core pillar of our design architecture. 
> * **Zero Permanent Audio Retention:** The application processes audio transiently to extract transcripts and summary payloads, then deletes the temporary buffers. No raw audio recordings are stored on our servers.
> * **Local Sandbox Processing:** All user sessions, local logs, and cache indexes are retained directly in your browser's secure client-side storage, ensuring that third-party script runs cannot leak files.
> * **Access Controls (RBAC):** Gated screens restrict compliance policies and audit records to authorized Admin roles.

### Q2: Is the system GDPR and SOC2 compliant?
> **Answer:** Yes. Because the platform allows administrators to set custom data retention cycles (e.g. automatic deletion of logs after 30, 90, or 365 days) and restricts audit log visibility to Admin roles, it aligns perfectly with GDPR's data minimization guidelines. A complete audit log trails every login, config change, and file download.

---

## 2. Artificial Intelligence & Accuracy

### Q3: Why should we use AI instead of hiring administrative note-takers?
> **Answer:** Speed, standardization, and cost. While a human note-taker takes hours to draft summaries, the AI Meeting Notes Manager extracts structured action items and meeting insights instantly. Furthermore, AI eliminates subjectivity, ensuring every task is captured with identical metadata templates (Owner, Due Date, Priority).

### Q4: How accurate is the transcription and AI summary engine?
> **Answer:** The system leverages state-of-the-art Natural Language Processing (NLP) models with a baseline accuracy of over 95% for standard business audio. For accents or technical industry jargon, we include a **Human-in-the-Loop review step** inside the Meetings Archive page where users can manually edit and correct summaries or task assignments before final distribution.

---

## 3. Integrations & Scalability

### Q5: Can this platform integrate with Zoom, Microsoft Teams, or Google Meet?
> **Answer:** Yes. The Phase 2 roadmap includes native webhook integrations. These webhooks allow the platform to receive calendar invites, listen to API streams from Teams/Zoom, and push extracted action items directly into collaboration tools like Slack or JIRA automatically.

### Q6: Can multiple departments or distinct teams use this simultaneously?
> **Answer:** Absolutely. The system architecture supports workspace directory isolation. Different teams can manage their own meeting archives, set custom retention schedules, and track separate action item lists under localized tenant profiles.

### Q7: Will the application scale if our meeting volume increases by 10x?
> **Answer:** Yes. The frontend is built on lightweight, single-page frameworks, offloading heavy rendering work to client browsers. The backend uses scalable, serverless API functions designed to scale horizontally to support thousands of parallel transcription streams.

---

## 4. Customization & Offline Capability

### Q8: Can the application branding and layouts be customized?
> **Answer:** Yes. The styling system is built on a clean Vanilla CSS custom design system utilizing variables (e.g. `--color-accent-blue`, `--font-primary`). We can easily apply your brand's color palette, logo, and typography standards with minor changes to the style definitions.

### Q9: What happens if our internet connection is lost during a live meeting?
> **Answer:** The platform features **Continuous Offline Service Protection**. If cloud connection drops, the app switches to local mode. It continues tracking the live session locally, allowing notes to be typed and historic summaries to be searched. Once the connection is re-established, it syncs the database transparently.

### Q10: Can we export reports to other formats?
> **Answer:** Yes. The system includes a built-in markdown download utility. A single click compiles summaries, checklists, and timelines into a formatted document ready to be loaded into Notion, Confluence, or internal wiki directories.
