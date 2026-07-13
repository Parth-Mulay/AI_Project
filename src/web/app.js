/* ====================================================
   AI MEETING NOTES MANAGER - WEB FRONTEND CONTROLLER
   ==================================================== */

// Initial Seed Data for Archive
let meetings = [
    {
        id: "1",
        title: "Sprint Planning - Week 14",
        date: "2026-07-06",
        duration: "30 minutes",
        participants: ["Rahul", "Priya", "Amit"],
        tags: ["engineering"],
        summary: `## Executive Summary
Rahul confirmed that the core authentication module is fully completed. The team discussed security configurations and resolved to implement JWT-based token management for cross-origin compliance.

## Key Discussion Points
- Authentication modules development cycle complete.
- Migration protocols and token setups.
- Database mapping rules.

## Risks
- Need to align schemas before staging deployments.

## Next Steps
- Rahul to run integrity audits on endpoints.`,
        actionItems: [
            { task: "Rahul will review the database API schema tomorrow.", owner: "Rahul", deadline: "Tomorrow", status: "Pending" },
            { task: "Priya will deploy the cache layer by Friday.", owner: "Priya", deadline: "Friday", status: "Pending" }
        ],
        decisions: [
            "We decided to use JWT for token management."
        ],
        messages: [
            { speaker: "Rahul", content: "Authentication module is completed." },
            { speaker: "Priya", content: "We decided to use JWT for tokens." },
            { speaker: "Amit", content: "Rahul will review the API tomorrow." }
        ]
    },
    {
        id: "2",
        title: "Marketing Alignment Call",
        date: "2026-07-10",
        duration: "15 minutes",
        participants: ["Brian", "Priya"],
        tags: ["marketing"],
        summary: `## Executive Summary
Brian raised a compliance concern regarding the deployment server's resource constraints. Priya agreed to conduct a thorough security assessment prior to launch.

## Key Discussion Points
- Server capability reviews.
- Performance profiling checks.

## Risks
- Blocker: Deployment server has limited RAM allocation.`,
        actionItems: [
            { task: "Priya will conduct a security review before launch.", owner: "Priya", deadline: "before launch", status: "Pending" }
        ],
        decisions: [
            "Agreed to hold release updates until performance profiles are signed off."
        ],
        messages: [
            { speaker: "Brian", content: "Risk identified - deployment server has limited resources." },
            { speaker: "Priya", content: "Need to conduct a security review before launch." }
        ]
    },
    {
        id: "3",
        title: "Government Planning Sync - 2027 Agenda",
        date: "2026-07-13",
        duration: "45 minutes",
        participants: ["Sharma", "Iyer", "Khan", "Deshmukh", "Patel"],
        tags: ["government"],
        summary: `## Executive Summary
All departments aligned key projects under the technological growth agenda. Major agreements included a 20% budget expansion for clean energy and digital code basics integration.

## Key Discussion Points
- Funding allocations for clean wind infrastructure.
- Improving rural clinical healthcare capacities.
- Initiating district-level digital literacy classes.

## Risks
- Rural clinical facility staffing gaps must be solved.

## Next Steps
- Form a clinical task force to assess staffing quotas.`,
        actionItems: [
            { task: "Task force will be formed to assess rural healthcare gaps within three months.", owner: "Iyer", deadline: "within three months", status: "Pending" },
            { task: "A feasibility study on AI driven traffic management will be commissioned.", owner: "Deshmukh", deadline: "December 2027", status: "Pending" },
            { task: "Ministries will submit integrated action plans by March 2027.", owner: "Sharma", deadline: "March 2027", status: "Pending" }
        ],
        decisions: [
            "Launch a pilot program in 10 districts integrating coding and AI basics into curricula.",
            "Introduce a subsidy scheme for drought resistant seeds."
        ],
        messages: [
            { speaker: "Sharma", content: "We must allocate more funds toward renewable energy projects." },
            { speaker: "Iyer", content: "Rural hospitals require immediate upgrades and staffing." },
            { speaker: "Khan", content: "Digital literacy programs should be expanded." }
        ]
    }
];

// App Global State
let currentUserRole = "Member"; 
let isRecording = false;
let recordingTimer = null;
let recordingSeconds = 0;
let currentLiveMeeting = null;
let notifications = [
    { text: "Welcome to AI Meeting Notes Manager Dashboard!", time: "Just now" },
    { text: "Loaded 3 historical documents from database sync.", time: "1 min ago" }
];

/* ====================================================
   DOM CONTENT LOADED INITIALIZER
   ==================================================== */
document.addEventListener("DOMContentLoaded", () => {
    initRouter();
    initRoleController();
    initNotificationDrawer();
    initLiveCapture();
    initUploader();
    initArchive();
    initSearch();
    
    // Draw initial dashboard stats and values
    updateTelemetry();
    renderRecentMeetings();
    renderAggregatedChecklist();
    renderNotificationList();

    // Setup global Ctrl+K key listener for search
    window.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "k") {
            e.preventDefault();
            document.getElementById("global-search-input").focus();
        }
    });
});

/* ====================================================
   1. ROUTER VIEW SWAP CONTROLLER
   ==================================================== */
function initRouter() {
    const navItems = document.querySelectorAll(".nav-item");
    const panels = document.querySelectorAll(".view-panel");

    navItems.forEach(item => {
        item.addEventListener("click", () => {
            const targetId = item.getAttribute("data-target");
            
            // Swap active classes in navigation sidebar
            navItems.forEach(i => i.classList.remove("active"));
            item.classList.add("active");

            // Swap panel visibility
            panels.forEach(p => {
                if (p.id === targetId) {
                    p.classList.remove("hidden");
                } else {
                    p.classList.add("hidden");
                }
            });

            // Back to list when navigating to archive view
            if (targetId === "view-archive") {
                showArchiveList();
            }
        });
    });

    document.getElementById("btn-goto-archive").addEventListener("click", () => {
        document.querySelector('[data-target="view-archive"]').click();
    });

    document.getElementById("btn-tour-start").addEventListener("click", () => {
        document.querySelector('[data-target="view-dashboard"]').click();
    });
}

/* ====================================================
   2. ROLE-BASED ACCESS CONTROL (RBAC)
   ==================================================== */
function initRoleController() {
    const roleBtn = document.getElementById("btn-role-toggle");
    const roleTxt = document.getElementById("current-role-txt");
    const sidebarRole = document.getElementById("directory-user-role");
    const userRoleBadge = document.querySelector(".user-role-badge");
    const auditOverlay = document.getElementById("audit-locked-overlay");
    const settingsOverlay = document.getElementById("settings-locked-overlay");
    const retentionInput = document.getElementById("settings-retention");
    const btnSaveRetention = document.getElementById("btn-save-retention");

    roleBtn.addEventListener("click", () => {
        currentUserRole = currentUserRole === "Member" ? "Admin" : "Member";
        
        // Update labels
        roleTxt.textContent = currentUserRole.toUpperCase();
        userRoleBadge.textContent = currentUserRole;
        if (sidebarRole) sidebarRole.textContent = currentUserRole;

        pushToast(`User role toggled to: ${currentUserRole.toUpperCase()}`, "info");

        // Toggle Lock Overlays
        if (currentUserRole === "Admin") {
            roleBtn.classList.add("active");
            auditOverlay.style.display = "none";
            settingsOverlay.style.display = "none";
            retentionInput.disabled = false;
            btnSaveRetention.disabled = false;
        } else {
            roleBtn.classList.remove("active");
            auditOverlay.style.display = "flex";
            settingsOverlay.style.display = "flex";
            retentionInput.disabled = true;
            btnSaveRetention.disabled = true;
        }
    });

    btnSaveRetention.addEventListener("click", () => {
        if (currentUserRole !== "Admin") return;
        const days = retentionInput.value;
        pushToast(`Data retention period saved to ${days} days!`, "success");
        addNotification(`Data retention cycle policy adjusted to ${days} days.`);
    });
}

/* ====================================================
   3. NOTIFICATIONS DRAWER CONTROLLER
   ==================================================== */
function initNotificationDrawer() {
    const bellBtn = document.getElementById("btn-notifications");
    const closeBtn = document.getElementById("close-drawer-btn");
    const drawer = document.getElementById("notification-drawer");

    bellBtn.addEventListener("click", () => {
        drawer.classList.remove("hidden");
        document.getElementById("noti-dot").style.display = "none";
    });

    closeBtn.addEventListener("click", () => {
        drawer.classList.add("hidden");
    });
}

function addNotification(text) {
    notifications.push({ text: text, time: "Just now" });
    renderNotificationList();
    const dot = document.getElementById("noti-dot");
    dot.style.display = "block";
}

function renderNotificationList() {
    const list = document.getElementById("notification-list");
    if (notifications.length === 0) {
        list.innerHTML = `<p class="empty-noti">No new notifications.</p>`;
        return;
    }
    list.innerHTML = notifications.map(n => `
        <div class="noti-item">
            <p>${n.text}</p>
            <span class="checklist-meta">${n.time}</span>
        </div>
    `).reverse().join("");
}

/* ====================================================
   4. LIVE MEETING DIALOG CAPTURE ENGINE
   ==================================================== */
function initLiveCapture() {
    const setupContainer = document.getElementById("live-setup-container");
    const activeContainer = document.getElementById("live-active-container");
    const btnStart = document.getElementById("btn-start-live");
    const btnStop = document.getElementById("btn-stop-live");
    const btnSend = document.getElementById("btn-send-message");
    const msgInput = document.getElementById("live-message-input");
    const transcriptFeed = document.getElementById("live-transcript-feed");
    const insightsFeed = document.getElementById("live-insights-feed");

    btnStart.addEventListener("click", () => {
        const title = document.getElementById("live-title").value.trim() || "Untitled Live Sync";
        const partsRaw = document.getElementById("live-participants").value.trim();
        const participants = partsRaw ? partsRaw.split(",").map(p => p.trim()) : ["Presenter"];

        currentLiveMeeting = {
            id: String(meetings.length + 1),
            title: title,
            date: new Date().toISOString().split("T")[0],
            duration: "0 minutes",
            participants: participants,
            tags: ["engineering"],
            summary: "",
            actionItems: [],
            decisions: [],
            messages: []
        };

        // UI View Swap
        setupContainer.classList.add("hidden");
        activeContainer.classList.remove("hidden");
        transcriptFeed.innerHTML = "";
        insightsFeed.innerHTML = "";

        // Timer initialization
        recordingSeconds = 0;
        isRecording = true;
        document.getElementById("recording-timer").textContent = "00:00";
        recordingTimer = setInterval(() => {
            recordingSeconds++;
            const mm = String(Math.floor(recordingSeconds / 60)).padStart(2, '0');
            const ss = String(recordingSeconds % 60).padStart(2, '0');
            document.getElementById("recording-timer").textContent = `${mm}:${ss}`;
        }, 1000);

        pushToast(`Live recording session '${title}' started!`, "success");
    });

    btnSend.addEventListener("click", sendMessage);
    msgInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    function sendMessage() {
        const line = msgInput.value.trim();
        if (!line) return;
        msgInput.value = "";

        let speaker = "Speaker";
        let content = line;
        if (line.includes(":")) {
            const parts = line.split(":", 1);
            speaker = parts[0].trim();
            content = line.substring(line.indexOf(":") + 1).trim();
        }

        // Add to live timeline
        currentLiveMeeting.messages.push({ speaker, content });
        const lineDiv = document.createElement("div");
        lineDiv.className = "transcript-line";
        lineDiv.innerHTML = `<strong>${speaker}:</strong> ${content}`;
        transcriptFeed.appendChild(lineDiv);
        transcriptFeed.scrollTop = transcriptFeed.scrollHeight;

        // Perform Rule-Based Keyword Extraction on message
        analyzeLiveMessage(speaker, content);
    }

    function analyzeLiveMessage(speaker, content) {
        const lower = content.toLowerCase();
        
        // 1. Action Items extraction check
        const actionKws = ["will", "must", "should", "need to", "action", "follow-up", "deadline", "task"];
        if (actionKws.some(kw => lower.includes(kw))) {
            let owner = speaker;
            // Scan if another participant name is in the string
            for (let p of currentLiveMeeting.participants) {
                if (p.toLowerCase() !== speaker.toLowerCase() && lower.includes(p.toLowerCase())) {
                    owner = p;
                    break;
                }
            }

            // Extrapolate deadline if found
            let deadline = "Pending";
            if (lower.includes("tomorrow")) deadline = "Tomorrow";
            else if (lower.includes("friday")) deadline = "Friday";
            else if (lower.includes("monday")) deadline = "Monday";

            const actionObj = {
                task: content,
                owner: owner,
                deadline: deadline,
                status: "Pending"
            };

            currentLiveMeeting.actionItems.push(actionObj);
            renderLiveInsight("Action Item", content, `Assigned: ${owner} | Deadline: ${deadline}`);
            pushToast(`🤖 AI Action Item detected for ${owner}`, "ai");
        }

        // 2. Decisions extraction check
        const decisionKws = ["approved", "agreed", "decided", "accepted", "confirmed", "resolved"];
        if (decisionKws.some(kw => lower.includes(kw))) {
            currentLiveMeeting.decisions.push(content);
            renderLiveInsight("Decision", content, `Approved by consensus`);
            pushToast(`🤖 AI Decision Outlined`, "ai");
        }
    }

    function renderLiveInsight(type, content, meta) {
        const container = document.getElementById("live-insights-feed");
        const empty = container.querySelector(".empty-feed");
        if (empty) empty.remove();

        const card = document.createElement("div");
        card.className = "insight-card";
        card.innerHTML = `
            <div class="insight-header">
                <span>🤖 AI ${type}</span>
                <span>Confidence 95%</span>
            </div>
            <div class="insight-desc">${content}</div>
            <div class="insight-context">${meta}</div>
        `;
        container.appendChild(card);
        container.scrollTop = container.scrollHeight;
    }

    btnStop.addEventListener("click", () => {
        if (!isRecording) return;
        clearInterval(recordingTimer);
        isRecording = false;

        // Auto compile summary
        const mm = Math.ceil(recordingSeconds / 60);
        currentLiveMeeting.duration = `${mm} minutes`;

        // Synthesis summaries
        let summaryText = `## Executive Summary\nLive Capture meeting notes regarding key operations.\n\n`;
        if (currentLiveMeeting.decisions.length > 0) {
            summaryText += `## Key Discussion Points\n`;
            currentLiveMeeting.decisions.forEach(d => {
                summaryText += `- Consensus reached on: ${d}\n`;
            });
        }
        
        currentLiveMeeting.summary = summaryText.trim();
        meetings.push(currentLiveMeeting);

        // Reset Form
        setupContainer.classList.remove("hidden");
        activeContainer.classList.add("hidden");
        document.getElementById("live-title").value = "";
        document.getElementById("live-participants").value = "";

        // UI Telemetry updates
        updateTelemetry();
        renderRecentMeetings();
        renderAggregatedChecklist();
        initArchive(); // Redraw Grid

        pushToast("Meeting Summary Saved to Archive!", "success");
        addNotification(`New live meeting notes compiled: ${currentLiveMeeting.title}`);

        // Open details view
        openMeetingDetails(currentLiveMeeting.id);
    });
}

/* ====================================================
   5. DRAG AND DROP DOCUMENT FILE UPLOAD PIPELINE
   ==================================================== */
function initUploader() {
    const dropZone = document.getElementById("drop-zone");
    const uploaderInput = document.getElementById("file-uploader");
    const logContainer = document.getElementById("upload-log-container");

    dropZone.addEventListener("click", () => uploaderInput.click());

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("active");
    });

    dropZone.addEventListener("dragleave", () => dropZone.classList.remove("active"));

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("active");
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    uploaderInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    function handleFileUpload(file) {
        const allowedExtensions = [".docx", ".pdf", ".txt", ".mp3", ".wav"];
        const ext = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();

        // 1. Extension Validation
        if (!allowedExtensions.includes(ext)) {
            pushToast(`❌ Error: Unsupported format '${ext}'`, "error");
            return;
        }

        // 2. Size Validation
        const isAudio = [".mp3", ".wav"].includes(ext);
        const maxLimit = isAudio ? 100 * 1024 * 1024 : 10 * 1024 * 1024;
        if (file.size > maxLimit) {
            pushToast(`❌ Error: File size exceeds the limit.`, "error");
            return;
        }

        // Trigger loading screen states anim
        logContainer.classList.remove("hidden");
        document.getElementById("uploaded-file-name").textContent = file.name;
        document.getElementById("uploaded-file-size").textContent = `${(file.size / (1024 * 1024)).toFixed(2)} MB`;
        document.getElementById("uploaded-file-icon").textContent = isAudio ? "🎵" : "📄";

        // Read or parse contents
        if (ext === ".txt") {
            const reader = new FileReader();
            reader.onload = function(e) {
                runProcessingStagesAnimation(file.name, e.target.result);
            };
            reader.readAsText(file);
        } else {
            // For docx/pdf we simulate dynamic extraction values
            runProcessingStagesAnimation(file.name, `
                Meeting Minutes: Operations Sync
                Participants: Priya, Amit, Rahul
                Priya: We need to complete the release notes before launch.
                Amit: I will test the database backup by Friday.
                Rahul: I decided to approve the caching config.
            `);
        }
    }

    function runProcessingStagesAnimation(filename, text) {
        const stages = [
            { id: "stage-read", msg: "⏳ Reading document..." },
            { id: "stage-extract", msg: "⏳ Extracting text..." },
            { id: "stage-analyze", msg: "⏳ Analyzing meeting..." },
            { id: "stage-summary", msg: "⏳ Generating summary..." },
            { id: "stage-actions", msg: "⏳ Extracting action items..." },
            { id: "stage-complete", msg: "⏳ Completed." }
        ];

        // Reset indicators
        stages.forEach(s => {
            const el = document.getElementById(s.id);
            el.className = "stage-item pending";
            el.querySelector(".stage-indicator").textContent = "⏳";
        });

        document.getElementById("upload-status-badge").textContent = "Processing";
        document.getElementById("upload-status-badge").className = "badge amber";

        let currentStage = 0;

        function runNextStage() {
            if (currentStage > 0) {
                const prev = document.getElementById(stages[currentStage - 1].id);
                prev.className = "stage-item complete";
                prev.querySelector(".stage-indicator").textContent = "✅";
            }

            if (currentStage < stages.length) {
                const active = document.getElementById(stages[currentStage].id);
                active.className = "stage-item active";
                active.querySelector(".stage-indicator").textContent = "🔄";
                currentStage++;
                setTimeout(runNextStage, 300);
            } else {
                // Done parsing
                document.getElementById("upload-status-badge").textContent = "Completed";
                document.getElementById("upload-status-badge").className = "badge green";

                processExtractedDocument(filename, text);
            }
        }

        runNextStage();
    }

    function processExtractedDocument(filename, text) {
        // AI Dynamic processing on extracted text
        const title = `Uploaded - ${filename}`;
        const newMtg = {
            id: String(meetings.length + 1),
            title: title,
            date: new Date().toISOString().split("T")[0],
            duration: "10 minutes",
            participants: [],
            tags: ["engineering"],
            summary: "",
            actionItems: [],
            decisions: [],
            messages: []
        };

        // 1. Extract participants
        const participants = ["Priya", "Amit", "Rahul"]; // Defaults
        text.split("\n").forEach(line => {
            if (line.includes(":")) {
                const spk = line.split(":", 1)[0].trim();
                if (spk.length < 20 && !participants.includes(spk)) {
                    participants.push(spk);
                }
            }
        });
        newMtg.participants = participants;

        // 2. Message timelines
        text.split("\n").forEach(line => {
            const clean = line.trim();
            if (!clean) return;
            if (clean.includes(":")) {
                const parts = clean.split(":", 1);
                newMtg.messages.push({ speaker: parts[0].trim(), content: clean.substring(clean.indexOf(":")+1).trim() });
            } else {
                newMtg.messages.push({ speaker: "Document", content: clean });
            }
        });

        // 3. Sentences insights
        const sentences = text.split(/[.!?\n]/).map(s => s.trim()).filter(s => s.length > 5);
        const actionKws = ["will", "must", "should", "need to", "action", "task"];
        sentences.forEach(sent => {
            const lower = sent.toLowerCase();
            if (actionKws.some(kw => lower.includes(kw))) {
                let owner = "Unassigned";
                participants.forEach(p => {
                    if (lower.includes(p.toLowerCase())) owner = p;
                });

                let deadline = "";
                if (lower.includes("tomorrow")) deadline = "Tomorrow";
                else if (lower.includes("friday")) deadline = "Friday";

                newMtg.actionItems.push({
                    task: sent,
                    owner: owner,
                    deadline: deadline || "Pending",
                    status: "Pending"
                });
            }

            const decKws = ["decided", "approved", "agreed", "resolved"];
            if (decKws.some(kw => lower.includes(kw))) {
                newMtg.decisions.push(sent);
            }
        });

        // 4. Summarize Markdown
        const firstSentences = sentences.slice(0, 2).join(" ");
        newMtg.summary = `## Executive Summary\n${firstSentences || "Document text successfully analyzed."}\n\n## Key Outcomes\nDynamic analysis run on uploaded file.`;

        // Save
        meetings.push(newMtg);

        // Reset Uploader View
        setTimeout(() => {
            logContainer.classList.add("hidden");
            updateTelemetry();
            renderRecentMeetings();
            renderAggregatedChecklist();
            initArchive();

            pushToast("Dynamic document analysis complete!", "success");
            addNotification(`Uploaded file processed: ${filename}`);

            // Go to Details
            openMeetingDetails(newMtg.id);
        }, 800);
    }
}

/* ====================================================
   6. MEETINGS ARCHIVE GRID & DETAILS TABS
   ==================================================== */
function initArchive() {
    renderMeetingsGrid(meetings);
    initTabsNavigator();

    document.getElementById("btn-back-to-archive").addEventListener("click", () => {
        showArchiveList();
    });

    document.getElementById("btn-export-markdown").addEventListener("click", () => {
        const id = document.getElementById("archive-details-panel").getAttribute("data-active-id");
        const mtg = meetings.find(m => m.id === id);
        if (mtg) exportMeetingToMarkdownFile(mtg);
    });
}

function renderMeetingsGrid(list) {
    const grid = document.getElementById("meetings-grid-container");
    if (list.length === 0) {
        grid.innerHTML = `<p class="empty-feed">No meetings found matching parameters.</p>`;
        return;
    }

    grid.innerHTML = list.map(m => `
        <div class="meeting-card" onclick="openMeetingDetails('${m.id}')">
            <div class="card-meta">
                <span>📆 ${m.date}</span>
                <span class="badge purple">${m.tags[0]}</span>
            </div>
            <h4>${m.title}</h4>
            <p class="checklist-meta">${m.participants.length} participants | ${m.messages.length} messages</p>
        </div>
    `).join("");
}

function openMeetingDetails(id) {
    const mtg = meetings.find(m => m.id === id);
    if (!mtg) return;

    // View panels swap
    document.getElementById("archive-list-panel").classList.add("hidden");
    const detailsPanel = document.getElementById("archive-details-panel");
    detailsPanel.classList.remove("hidden");
    detailsPanel.setAttribute("data-active-id", id);

    // Sidebar navigation highlight sync
    document.querySelectorAll(".nav-item").forEach(i => i.classList.remove("active"));
    document.querySelector('[data-target="view-archive"]').classList.add("active");
    document.querySelectorAll(".view-panel").forEach(p => p.id === "view-archive" ? p.classList.remove("hidden") : p.classList.add("hidden"));

    // Populate metadata labels
    document.getElementById("details-meeting-title").textContent = mtg.title;
    document.getElementById("details-meeting-date").textContent = `📆 ${mtg.date}`;
    document.getElementById("details-meeting-duration").textContent = `⏱️ ${mtg.duration}`;
    document.getElementById("details-meeting-participants").textContent = `👥 ${mtg.participants.join(", ")}`;

    // 1. Tab Content: Summary
    // Convert basic double hash headers and lists into HTML tags
    let htmlSummary = mtg.summary
        .replace(/## (.*)/g, '<h3>$1</h3>')
        .replace(/- (.*)/g, '<li>$1</li>')
        .replace(/\n/g, '<br>');
    document.getElementById("details-summary-content").innerHTML = htmlSummary;

    // 2. Tab Content: Action items
    const actionsBox = document.getElementById("details-actions-list");
    if (mtg.actionItems.length === 0) {
        actionsBox.innerHTML = "<p class='empty-feed'>No action items found.</p>";
    } else {
        actionsBox.innerHTML = mtg.actionItems.map((a, idx) => `
            <div class="checklist-item">
                <input type="checkbox" id="action-chk-${idx}" ${a.status === 'Completed' ? 'checked' : ''} onchange="toggleActionStatus('${mtg.id}', ${idx})">
                <div class="checklist-details">
                    <span class="checklist-title">${a.task}</span>
                    <span class="checklist-meta">Assigned to: <strong>${a.owner}</strong> | Deadline: ${a.deadline}</span>
                </div>
            </div>
        `).join("");
    }

    // 3. Tab Content: Decisions
    const decisionsBox = document.getElementById("details-decisions-list");
    if (mtg.decisions.length === 0) {
        decisionsBox.innerHTML = "<p class='empty-feed'>No decisions logged.</p>";
    } else {
        decisionsBox.innerHTML = mtg.decisions.map(d => `
            <li>${d}</li>
        `).join("");
    }

    // 4. Tab Content: Transcript Timeline
    const transcriptBox = document.getElementById("details-transcript-list");
    if (mtg.messages.length === 0) {
        transcriptBox.innerHTML = "<p class='empty-feed'>No transcript timeline available.</p>";
    } else {
        transcriptBox.innerHTML = mtg.messages.map(m => `
            <div class="timeline-message">
                <div class="timeline-speaker">${m.speaker}</div>
                <div class="timeline-content">${m.content}</div>
            </div>
        `).join("");
    }

    // Active Tab reset to Summary
    document.querySelectorAll(".tab-btn").forEach(b => {
        b.getAttribute("data-tab") === "tab-summary" ? b.classList.add("active") : b.classList.remove("active");
    });
    document.querySelectorAll(".tab-pane").forEach(p => {
        p.id === "tab-summary" ? p.classList.add("active") : p.classList.remove("active");
    });
}

function toggleActionStatus(mtgId, actionIdx) {
    const mtg = meetings.find(m => m.id === mtgId);
    if (!mtg) return;
    const a = mtg.actionItems[actionIdx];
    a.status = a.status === "Completed" ? "Pending" : "Completed";
    
    pushToast(`Action item status updated to: ${a.status.toUpperCase()}`, "info");
    updateTelemetry();
    renderAggregatedChecklist();
}

function showArchiveList() {
    document.getElementById("archive-list-panel").classList.remove("hidden");
    document.getElementById("archive-details-panel").classList.add("hidden");
    renderMeetingsGrid(meetings);
}

function initTabsNavigator() {
    const tabs = document.querySelectorAll(".tab-btn");
    const panes = document.querySelectorAll(".tab-pane");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            const targetPane = tab.getAttribute("data-tab");
            panes.forEach(pane => {
                pane.id === targetPane ? pane.classList.add("active") : pane.classList.remove("active");
            });
        });
    });
}

/* ====================================================
   7. TELEMETRY BOARD AND DASHBOARD CARD UPDATER
   ==================================================== */
function updateTelemetry() {
    const totalMeetings = meetings.length;
    document.getElementById("stat-meetings-count").textContent = totalMeetings;
    document.getElementById("stat-time-saved").textContent = `${(totalMeetings * 2.5).toFixed(1)} hrs`;

    let totalPending = 0;
    meetings.forEach(m => {
        m.actionItems.forEach(a => {
            if (a.status === "Pending") totalPending++;
        });
    });
    document.getElementById("stat-actions-pending").textContent = totalPending;
}

function renderRecentMeetings() {
    const list = [...meetings].sort((a,b) => new Date(b.date) - new Date(a.date)).slice(0, 5);
    const tbody = document.getElementById("recent-meetings-table-body");

    tbody.innerHTML = list.map(m => `
        <tr onclick="openMeetingDetails('${m.id}')" style="cursor:pointer;">
            <td><strong>${m.title}</strong></td>
            <td>${m.date}</td>
            <td>
                <div class="avatars-group">
                    ${m.participants.slice(0,3).map(p => `
                        <div class="avatar-mini">${p.charAt(0)}</div>
                    `).join("")}
                    ${m.participants.length > 3 ? `<div class="avatar-mini">+${m.participants.length - 3}</div>` : ""}
                </div>
            </td>
            <td><span class="badge green">Analyzed</span></td>
        </tr>
    `).join("");
}

function renderAggregatedChecklist() {
    const box = document.getElementById("aggregated-checklist");
    let itemsHtml = [];

    meetings.forEach(m => {
        m.actionItems.forEach((a, idx) => {
            if (a.status === "Pending") {
                itemsHtml.push(`
                    <div class="checklist-item">
                        <input type="checkbox" onchange="toggleActionStatus('${m.id}', ${idx})">
                        <div class="checklist-details">
                            <span class="checklist-title">${a.task}</span>
                            <span class="checklist-meta">Assigned: ${a.owner} | ${m.title}</span>
                        </div>
                    </div>
                `);
            }
        });
    });

    if (itemsHtml.length === 0) {
        box.innerHTML = `<p class="empty-feed">All action items completed! 🎉</p>`;
    } else {
        box.innerHTML = itemsHtml.slice(0, 5).join("");
    }
}

/* ====================================================
   8. FILTER SEARCH ENGINE
   ==================================================== */
function initSearch() {
    const globalInput = document.getElementById("global-search-input");
    const archiveInput = document.getElementById("archive-search-input");
    const categorySelect = document.getElementById("archive-tag-filter");

    globalInput.addEventListener("input", (e) => {
        const query = e.target.value.toLowerCase().trim();
        if (query) {
            document.querySelector('[data-target="view-archive"]').click();
            archiveInput.value = query;
            triggerFilter();
        }
    });

    archiveInput.addEventListener("input", triggerFilter);
    categorySelect.addEventListener("change", triggerFilter);

    function triggerFilter() {
        const query = archiveInput.value.toLowerCase().trim();
        const tag = categorySelect.value;

        const filtered = meetings.filter(m => {
            const matchesQuery = m.title.toLowerCase().includes(query) || 
                                 m.summary.toLowerCase().includes(query) ||
                                 m.participants.some(p => p.toLowerCase().includes(query));
            const matchesTag = (tag === "all" || m.tags.includes(tag));
            return matchesQuery && matchesTag;
        });

        renderMeetingsGrid(filtered);
    }
}

/* ====================================================
   9. LOCAL MARKDOWN FILE EXPORTER DOWNLOADER
   ==================================================== */
function exportMeetingToMarkdownFile(meeting) {
    let md = `# ${meeting.title}\n\n`;
    md += `**Date:** ${meeting.date}\n`;
    md += `**Duration:** ${meeting.duration}\n`;
    md += `**Participants:** ${meeting.participants.join(", ")}\n\n`;
    md += `${meeting.summary}\n\n`;

    md += `## Action Items\n`;
    if (meeting.actionItems.length === 0) {
        md += `No action items identified.\n`;
    } else {
        meeting.actionItems.forEach(a => {
            md += `- [${a.status === 'Completed' ? 'x' : ' '}] ${a.task} (Owner: ${a.owner} | Due: ${a.deadline})\n`;
        });
    }
    md += `\n`;

    md += `## Decisions\n`;
    if (meeting.decisions.length === 0) {
        md += `No decisions recorded.\n`;
    } else {
        meeting.decisions.forEach(d => {
            md += `- ${d}\n`;
        });
    }
    md += `\n`;

    md += `## Timeline Transcript\n`;
    meeting.messages.forEach(m => {
        md += `**${m.speaker}**: ${m.content}\n\n`;
    });

    // File download trigger
    const blob = new Blob([md], { type: "text/markdown;charset=utf-8;" });
    const link = document.createElement("a");
    const filename = `${meeting.title.replace(/\s+/g, "_")}_Notes.md`;

    if (navigator.msSaveBlob) {
        navigator.msSaveBlob(blob, filename);
    } else {
        link.href = URL.createObjectURL(blob);
        link.setAttribute("download", filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    pushToast("Markdown file downloaded successfully!", "success");
}

/* ====================================================
   10. FLOATING TOAST NOTIFICATION POPUPS
   ==================================================== */
function pushToast(message, type = "info") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    
    // Choose icon
    let icon = "ℹ️";
    if (type === "success") icon = "✅";
    else if (type === "warning") icon = "⚠️";
    else if (type === "error") icon = "❌";
    else if (type === "ai") icon = "🤖";

    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <span class="toast-msg">${message}</span>
        <button class="toast-close">&times;</button>
    `;

    container.appendChild(toast);

    // Auto remove after 5 seconds
    const timeout = setTimeout(() => {
        toast.remove();
    }, 5000);

    toast.querySelector(".toast-close").addEventListener("click", () => {
        clearTimeout(timeout);
        toast.remove();
    });
}
