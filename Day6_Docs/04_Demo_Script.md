# Live Presentation Walkthrough Demo Script

**Project Title:** AI Meeting Notes Manager  
**Presentation Audience:** Enterprise Client Stakeholders  
**Presenter:** Project Lead / Account Director  

---

## 1. Introduction & Context (Slide-to-Screen)
* **Goal:** Set the stage, introduce the team, and align on the meeting objectives.
* **Presenter Dialogue:**
  > "Good morning/afternoon, everyone. Thank you for joining us today. Over the past few weeks, we've collaborated closely with your operations team to design a platform that solves a major efficiency leak: administrative overhead. 
  > 
  > Every day, your leaders spend hours summarizing meetings and chasing status updates. Today, I am excited to give you a live tour of the **AI Meeting Notes Manager**—a tailored workspace built to automate notes transcription, extract decisions, track ownership, and keep your teams completely aligned."

---

## 2. Dashboard View & Live Telemetry
* **Action:** Open browser tab to `dashboard.html`. Hover over metrics and charts.
* **Presenter Dialogue:**
  > "We are starting here on the main Workspace Dashboard. We wanted your leaders to immediately see the value this application generates.
  > 
  > At the top, you can see our live efficiency meters. The first card shows **Time Saved This Week**—presently 12.5 hours—accompanied by a trend sparkline. To the right, you can see the count of meetings analyzed and our AI processing success rate.
  > 
  > Below, we have built native charts representing your meeting telemetry. Our **Time Saved Trend** line graph tracks efficiency improvements day by day. Hovering over any coordinate displays the exact hours saved. Beside it, the **Meetings by Category** donut segments track meeting distribution across departments like Engineering, Marketing, and Operations. This visual telemetry gives your operations managers total transparency into team focus."

---

## 3. Live Capture & Real-Time AI Extraction
* **Action:** Click "Live Capture" in the sidebar navigation. Input meeting title "Sprint Core Sync". Click "Start Session". Speak or type a message like `Rahul: Priya will deploy the database backup by Friday.`
* **Presenter Dialogue:**
  > "Now, let's look at active meeting capture. Imagine you are starting a stand-up. I'll navigate to 'Live Capture' in our sidebar. Notice how the default underlines are gone and the interface uses clean Google Material Icons.
  > 
  > We'll label this session 'Sprint Core Sync' and click 'Start Session'. The recording indicator begins pulsing, and the live timer starts. 
  > 
  > As the team speaks, the transcript timeline builds below. Even more impressive is the **AI Insights Feed** on the right. When I say: *'Priya will deploy the database backup by Friday'*, the system immediately flags this as an Action Item, assigns it to Priya, establishes a deadline, and prints an AI confidence chip. This happens live, meaning notes write themselves while the meeting is happening."

---

## 4. Multi-Format Upload & Processing Animation
* **Action:** Click "Upload File" in the sidebar. Hover over the drag-and-drop zone. Trigger a mock upload of `Operations_Report.docx`.
* **Presenter Dialogue:**
  > "What about meetings recorded on external devices or summarized in text templates? We've designed a Smart File Uploader. 
  > 
  > By navigating to 'Upload File', I can drag and drop text logs, Word docs, PDFs, or audio recordings up to 100MB. Let's upload this Word document.
  > 
  > Watch the progress pipeline. It transitions from reading to text extraction, analysis, and summary generation. Each stage is marked by a clean Material Symbol, featuring a spinning sync indicator during active analysis. The moment it completes, the upload status badge turns green, and the user is redirected to the meeting summaries archive."

---

## 5. Meetings Archive & Global Search
* **Action:** Click "Meetings Archive". Type "Government" in the search box. Click on the "Government Planning Sync" card. Switch between the "Summary", "Action Items", and "Transcript" tabs.
* **Presenter Dialogue:**
  > "Here we are in the Meetings Archive. Instead of scrolling through endless folders, I can filter meetings by categories or search keywords. Let's type 'Government' in the search bar. 
  > 
  > The grid immediately filters to match. Clicking the card slides us into the detail layout. The **Executive Summary** tab displays a professional, formatted overview of discussion points and risks. 
  > 
  > Toggling the **Action Items** tab shows checkboxes for tasks. If I complete a task here, it updates the dashboard telemetry automatically. Toggling **Transcript** shows the original chronological dialogue. If we need to distribute this, the 'Export Markdown' button instantly downloads a formatted file ready for email or corporate wiki upload."

---

## 6. Team Workspace & Role Gating (RBAC)
* **Action:** Click "Workspace Directory" in the sidebar. Point out Priya (Member badge) and the lock overlay on the Security Audit Logs. Click the "Active Role" toggle in the top-right header, changing the role to "Admin". Show the overlay disappear and the logs display.
* **Presenter Dialogue:**
  > "Security is a top priority. In the Workspace Directory, you can see all registered team members. Look at the Security Audit Logs card on the right: it displays a lock icon restricting access to Administrators.
  > 
  > Watch what happens when I simulate a role change. I will toggle our Active Role from 'Member' to 'Admin' in the top bar. The lock screen disappears instantly, revealing the audit records. This role-based access control is also active on the 'System Settings' page, protecting your retention configurations from standard users."

---

## 7. Business Value, Roadmap, & Closing
* **Presenter Dialogue:**
  > "As we conclude our tour, I want to emphasize the core business benefits:
  > - **Time Reclaimed:** 2.5 hours saved per meeting.
  > - **Risk Minimization:** System settings lock down auditing and compliance rules.
  > - **Offline Protection:** If the internet fails, local keyword lookups remain active.
  > 
  > Looking ahead, our Phase 2 roadmap includes direct integrations with Slack, Google Drive, and Zoom APIs to synchronize action items automatically.
  > 
  > Thank you for your time. I'd love to open the floor to any questions and finalize our sign-off checklist so we can proceed to core construction."
