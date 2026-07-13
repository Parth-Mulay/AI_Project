/* ====================================================
   AI MEETING NOTES MANAGER - WEB FRONTEND CONTROLLER
   ==================================================== */

// Default Seed Data matching the Figma Mockup
const defaultMeetings = [
    {
        id: "1",
        title: "Government Planning Sync - 2027 Agenda",
        date: "2026-07-13",
        time: "10:00 AM",
        duration: "45 minutes",
        participants: ["Sharma", "Iyer", "Khan", "Deshmukh", "Patel"],
        tags: ["government"],
        status: "Analyzed",
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
            { task: "Task force will be formed to assess rural healthcare gaps within three months.", owner: "Iyer", deadline: "Oct 13", priority: "medium", status: "Pending" },
            { task: "A feasibility study on AI driven traffic management will be commissioned.", owner: "Deshmukh", deadline: "Dec 20", priority: "low", status: "Pending" },
            { task: "Ministries will submit integrated action plans by March 2027.", owner: "Sharma", deadline: "Mar 30", priority: "low", status: "Pending" }
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
    },
    {
        id: "2",
        title: "Marketing Alignment Call",
        date: "2026-07-10",
        time: "02:30 PM",
        duration: "20 minutes",
        participants: ["Brian", "Priya"],
        tags: ["marketing"],
        status: "Analyzed",
        summary: `## Executive Summary
Brian raised a compliance concern regarding the deployment server's resource constraints. Priya agreed to conduct a thorough security assessment prior to launch.

## Key Discussion Points
- Server capability reviews.
- Performance profiling checks.

## Risks
- Blocker: Deployment server has limited RAM allocation.`,
        actionItems: [
            { task: "Priya will conduct a security review before launch.", owner: "Priya", deadline: "Jul 22", priority: "medium", status: "Pending" }
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
        title: "Sprint Planning - Week 14",
        date: "2026-07-06",
        time: "11:00 AM",
        duration: "30 minutes",
        participants: ["Rahul", "Priya", "Amit"],
        tags: ["engineering"],
        status: "Analyzed",
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
            { task: "Rahul will review the database API schema tomorrow.", owner: "Rahul", deadline: "Jul 20", priority: "high", status: "Pending" },
            { task: "Priya will deploy the cache layer by Friday.", owner: "Priya", deadline: "Jul 18", priority: "high", status: "Pending" }
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
        id: "4",
        title: "Client Onboarding Discussion",
        date: "2026-07-05",
        time: "04:00 PM",
        duration: "45 minutes",
        participants: ["Client", "Partner"],
        tags: ["engineering"],
        status: "Processing",
        summary: `## Executive Summary\nClient review onboarding requirements.\n\n## Key Outcomes\nDynamic analysis processing.`,
        actionItems: [
            { task: "Approve the new onboarding flow wireframes.", owner: "Designer", deadline: "Jul 21", priority: "low", status: "Pending" }
        ],
        decisions: [],
        messages: [
            { speaker: "Client", content: "We should start the deployment draft." }
        ]
    },
    {
        id: "5",
        title: "Product Roadmap Review",
        date: "2026-07-04",
        time: "09:30 AM",
        duration: "60 minutes",
        participants: ["Priya", "Brian", "Amit"],
        tags: ["engineering"],
        status: "Analyzed",
        summary: `## Executive Summary\nReviewed roadmap items for Q3/Q4.`,
        actionItems: [],
        decisions: [],
        messages: []
    }
];

// Load State from LocalStorage or seed defaults
let meetings = JSON.parse(localStorage.getItem("meetings")) || defaultMeetings;
let currentUserRole = localStorage.getItem("currentUserRole") || "Member";
let notifications = JSON.parse(localStorage.getItem("notifications")) || [
    { text: "Welcome to AI Meeting Notes Manager Dashboard!", time: "Just now" },
    { text: "Loaded 5 historical documents from database sync.", time: "1 min ago" }
];

let isRecording = false;
let recordingTimer = null;
let recordingSeconds = 0;
let currentLiveMeeting = null;
let selectedPriority = "all";

// Save variables helper
function saveStateToLocalStorage() {
    localStorage.setItem("meetings", JSON.stringify(meetings));
    localStorage.setItem("currentUserRole", currentUserRole);
    localStorage.setItem("notifications", JSON.stringify(notifications));
}

/* ====================================================
   DOM CONTENT LOADED INITIALIZER
   ==================================================== */
document.addEventListener("DOMContentLoaded", () => {
    // Save defaults back to storage if empty
    if (!localStorage.getItem("meetings")) {
        saveStateToLocalStorage();
    }

    initGlobalHeader();
    initRoleController();
    initNotificationDrawer();
    
    // Page-specific initializers based on present DOM elements
    if (document.getElementById("view-dashboard")) {
        initDashboardView();
    }
    if (document.getElementById("btn-start-live")) {
        initLiveCapture();
    }
    if (document.getElementById("drop-zone")) {
        initUploader();
    }
    if (document.getElementById("meetings-grid-container")) {
        initArchiveView();
    }
    if (document.getElementById("directory-user-role")) {
        // Workspace directory page
        syncRoleUI();
    }
    if (document.getElementById("settings-retention")) {
        initSettingsView();
    }

    // Global elements event binding
    document.getElementById("btn-assistant-quick").addEventListener("click", () => {
        pushToast("🤖 AI assistant loaded! Ask any query about your meeting workspace.", "ai");
    });

    const assistantSidebar = document.getElementById("btn-sidebar-assistant");
    if (assistantSidebar) {
        assistantSidebar.addEventListener("click", (e) => {
            e.preventDefault();
            pushToast("🤖 Interactive AI Assistant Drawer opening.", "ai");
        });
    }

    document.getElementById("btn-upgrade-plan").addEventListener("click", () => {
        pushToast("🚀 Connecting to payment gateway... Upgrade popup opened.", "info");
    });
});

/* ====================================================
   GLOBAL HEADER BAR & ROUTING
   ==================================================== */
function initGlobalHeader() {
    const globalInput = document.getElementById("global-search-input");
    
    // Global search redirection on Enter press
    globalInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            const val = globalInput.value.trim();
            if (val) {
                window.location.href = `archive.html?q=${encodeURIComponent(val)}`;
            }
        }
    });

    // global Ctrl+K key binding
    window.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "k") {
            e.preventDefault();
            globalInput.focus();
        }
    });
}

/* ====================================================
   ROLE-BASED ACCESS CONTROL (RBAC)
   ==================================================== */
function initRoleController() {
    const roleBtn = document.getElementById("btn-role-toggle");
    
    syncRoleUI();

    roleBtn.addEventListener("click", () => {
        currentUserRole = currentUserRole === "Member" ? "Admin" : "Member";
        saveStateToLocalStorage();
        syncRoleUI();
        pushToast(`User role toggled to: ${currentUserRole.toUpperCase()}`, "info");
    });
}

function syncRoleUI() {
    const roleTxt = document.getElementById("current-role-txt");
    const userRoleBadge = document.querySelector(".user-role-badge");
    const directoryUserRole = document.getElementById("directory-user-role");
    
    const auditOverlay = document.getElementById("audit-locked-overlay");
    const settingsOverlay = document.getElementById("settings-locked-overlay");
    const retentionInput = document.getElementById("settings-retention");
    const btnSaveRetention = document.getElementById("btn-save-retention");

    if (roleTxt) roleTxt.textContent = currentUserRole.toUpperCase();
    if (userRoleBadge) userRoleBadge.textContent = currentUserRole;
    if (directoryUserRole) directoryUserRole.textContent = currentUserRole;

    const roleBtn = document.getElementById("btn-role-toggle");
    if (!roleBtn) return;

    if (currentUserRole === "Admin") {
        roleBtn.classList.add("active");
        if (auditOverlay) auditOverlay.style.display = "none";
        if (settingsOverlay) settingsOverlay.style.display = "none";
        if (retentionInput) retentionInput.disabled = false;
        if (btnSaveRetention) btnSaveRetention.disabled = false;
    } else {
        roleBtn.classList.remove("active");
        if (auditOverlay) auditOverlay.style.display = "flex";
        if (settingsOverlay) settingsOverlay.style.display = "flex";
        if (retentionInput) retentionInput.disabled = true;
        if (btnSaveRetention) btnSaveRetention.disabled = true;
    }
}

/* ====================================================
   NOTIFICATIONS SYSTEM
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
    
    renderNotificationList();
}

function addNotification(text) {
    notifications.push({ text: text, time: "Just now" });
    saveStateToLocalStorage();
    renderNotificationList();
    const dot = document.getElementById("noti-dot");
    if (dot) dot.style.display = "block";
}

function renderNotificationList() {
    const list = document.getElementById("notification-list");
    if (!list) return;
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
   DASHBOARD INITIALIZER & RENDERERS
   ==================================================== */
function initDashboardView() {
    updateTelemetry();
    renderRecentMeetings();
    renderAggregatedChecklist();
    initPriorityTabs();
}

function updateTelemetry() {
    const totalMeetings = meetings.length;
    
    const countEl = document.getElementById("stat-meetings-count");
    const timeEl = document.getElementById("stat-time-saved");
    const actionsEl = document.getElementById("stat-actions-pending");

    if (countEl) countEl.textContent = totalMeetings;
    if (timeEl) timeEl.textContent = `${(totalMeetings * 2.5).toFixed(1)} hrs`;

    let totalPending = 0;
    meetings.forEach(m => {
        m.actionItems.forEach(a => {
            if (a.status === "Pending") totalPending++;
        });
    });
    if (actionsEl) actionsEl.textContent = totalPending;
}

function renderRecentMeetings() {
    const list = [...meetings].sort((a,b) => new Date(b.date) - new Date(a.date)).slice(0, 5);
    const tbody = document.getElementById("recent-meetings-table-body");
    if (!tbody) return;

    tbody.innerHTML = list.map(m => `
        <tr onclick="window.location.href='archive.html?id=${m.id}'" style="cursor:pointer;">
            <td><strong><span class="material-symbols-outlined" style="font-size: 16px; color: var(--color-accent-purple); vertical-align: -2px; margin-right: 4px;">folder</span> ${m.title}</strong></td>
            <td>${m.date} • ${m.time || '10:00 AM'}</td>
            <td>
                <div class="avatars-group">
                    ${m.participants.slice(0,3).map(p => `
                        <div class="avatar-mini">${p.charAt(0)}</div>
                    `).join("")}
                    ${m.participants.length > 3 ? `<div class="avatar-mini">+${m.participants.length - 3}</div>` : ""}
                </div>
            </td>
            <td><span class="badge ${m.status === 'Processing' ? 'amber' : 'green'}">${m.status || 'Analyzed'}</span></td>
        </tr>
    `).join("");
}

function initPriorityTabs() {
    const pTabs = document.querySelectorAll(".p-tab");
    pTabs.forEach(tab => {
        tab.addEventListener("click", () => {
            pTabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            selectedPriority = tab.getAttribute("data-priority");
            renderAggregatedChecklist();
        });
    });

    const shortcutBtn = document.getElementById("btn-add-action-item-shortcut");
    if (shortcutBtn) {
        shortcutBtn.addEventListener("click", () => {
            pushToast("Adding new action item... Feature loading.", "info");
        });
    }
}

function renderAggregatedChecklist() {
    const box = document.getElementById("aggregated-checklist");
    if (!box) return;
    let itemsHtml = [];

    meetings.forEach(m => {
        m.actionItems.forEach((a, idx) => {
            if (a.status === "Pending") {
                const matchesPriority = (selectedPriority === "all" || a.priority === selectedPriority);
                if (matchesPriority) {
                    itemsHtml.push(`
                        <div class="checklist-item">
                            <input type="checkbox" onchange="toggleActionStatus('${m.id}', ${idx})">
                            <div class="checklist-details">
                                <span class="checklist-title">${a.task}</span>
                                <span class="checklist-meta">Owner: <strong>${a.owner}</strong> | Due: ${a.deadline} | <span class="badge ${a.priority === 'high' ? 'red' : a.priority === 'medium' ? 'amber' : 'green'}">${a.priority}</span></span>
                            </div>
                        </div>
                    `);
                }
            }
        });
    });

    if (itemsHtml.length === 0) {
        box.innerHTML = `<p class="empty-feed">No pending action items for this filter.</p>`;
    } else {
        box.innerHTML = itemsHtml.slice(0, 6).join("");
    }
}

function toggleActionStatus(mtgId, actionIdx) {
    const mtg = meetings.find(m => m.id === mtgId);
    if (!mtg) return;
    const a = mtg.actionItems[actionIdx];
    a.status = a.status === "Completed" ? "Pending" : "Completed";
    
    saveStateToLocalStorage();
    pushToast(`Action item status updated to: ${a.status.toUpperCase()}`, "info");
    updateTelemetry();
    renderAggregatedChecklist();
}

/* ====================================================
   LIVE CAPTURE PAGE CONTROLLERS
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
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            duration: "0 minutes",
            participants: participants,
            tags: ["engineering"],
            status: "Analyzed",
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

        analyzeLiveMessage(speaker, content);
    }

    function analyzeLiveMessage(speaker, content) {
        const lower = content.toLowerCase();
        
        // 1. Action Items extraction check
        const actionKws = ["will", "must", "should", "need to", "action", "follow-up", "deadline", "task"];
        if (actionKws.some(kw => lower.includes(kw))) {
            let owner = speaker;
            for (let p of currentLiveMeeting.participants) {
                if (p.toLowerCase() !== speaker.toLowerCase() && lower.includes(p.toLowerCase())) {
                    owner = p;
                    break;
                }
            }

            let deadline = "Pending";
            if (lower.includes("tomorrow")) deadline = "Tomorrow";
            else if (lower.includes("friday")) deadline = "Friday";
            else if (lower.includes("monday")) deadline = "Monday";

            const actionObj = {
                task: content,
                owner: owner,
                deadline: deadline,
                priority: lower.includes("urgent") || lower.includes("immediate") ? "high" : "medium",
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

        const mm = Math.ceil(recordingSeconds / 60);
        currentLiveMeeting.duration = `${mm} minutes`;

        let summaryText = `## Executive Summary\nLive Capture meeting notes regarding key operations.\n\n`;
        if (currentLiveMeeting.decisions.length > 0) {
            summaryText += `## Key Discussion Points\n`;
            currentLiveMeeting.decisions.forEach(d => {
                summaryText += `- Consensus reached on: ${d}\n`;
            });
        }
        
        currentLiveMeeting.summary = summaryText.trim();
        meetings.push(currentLiveMeeting);
        saveStateToLocalStorage();

        setupContainer.classList.remove("hidden");
        activeContainer.classList.add("hidden");
        document.getElementById("live-title").value = "";
        document.getElementById("live-participants").value = "";

        pushToast("Meeting Summary Saved to Archive!", "success");
        addNotification(`New live meeting notes compiled: ${currentLiveMeeting.title}`);

        // Redirect directly to the details pane on archive page
        window.location.href = `archive.html?id=${currentLiveMeeting.id}`;
    });
}

/* ====================================================
   DOCUMENT UPLOAD CONTROLLERS
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

        if (!allowedExtensions.includes(ext)) {
            pushToast(`❌ Error: Unsupported format '${ext}'`, "error");
            return;
        }

        const isAudio = [".mp3", ".wav"].includes(ext);
        const maxLimit = isAudio ? 100 * 1024 * 1024 : 10 * 1024 * 1024;
        if (file.size > maxLimit) {
            pushToast(`❌ Error: File size exceeds the limit.`, "error");
            return;
        }

        logContainer.classList.remove("hidden");
        document.getElementById("uploaded-file-name").textContent = file.name;
        document.getElementById("uploaded-file-size").textContent = `${(file.size / (1024 * 1024)).toFixed(2)} MB`;
        document.getElementById("uploaded-file-icon").textContent = isAudio ? "🎵" : "📄";

        if (ext === ".txt") {
            const reader = new FileReader();
            reader.onload = function(e) {
                runProcessingStagesAnimation(file.name, e.target.result);
            };
            reader.readAsText(file);
        } else {
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
            { id: "stage-read", msg: "Reading document..." },
            { id: "stage-extract", msg: "Extracting text..." },
            { id: "stage-analyze", msg: "Analyzing meeting..." },
            { id: "stage-summary", msg: "Generating summary..." },
            { id: "stage-actions", msg: "Extracting action items..." },
            { id: "stage-complete", msg: "Completed." }
        ];

        stages.forEach(s => {
            const el = document.getElementById(s.id);
            if (el) {
                el.className = "stage-item pending";
                el.querySelector(".stage-indicator").innerHTML = `<span class="material-symbols-outlined">hourglass_empty</span>`;
            }
        });

        document.getElementById("upload-status-badge").textContent = "Processing";
        document.getElementById("upload-status-badge").className = "badge amber";

        let currentStage = 0;

        function runNextStage() {
            if (currentStage > 0) {
                const prev = document.getElementById(stages[currentStage - 1].id);
                if (prev) {
                    prev.className = "stage-item complete";
                    prev.querySelector(".stage-indicator").innerHTML = `<span class="material-symbols-outlined" style="color: var(--color-accent-green);">check_circle</span>`;
                }
            }

            if (currentStage < stages.length) {
                const active = document.getElementById(stages[currentStage].id);
                if (active) {
                    active.className = "stage-item active";
                    active.querySelector(".stage-indicator").innerHTML = `<span class="material-symbols-outlined animation-spin" style="color: var(--color-accent-purple);">sync</span>`;
                }
                currentStage++;
                setTimeout(runNextStage, 300);
            } else {
                document.getElementById("upload-status-badge").textContent = "Completed";
                document.getElementById("upload-status-badge").className = "badge green";

                processExtractedDocument(filename, text);
            }
        }

        runNextStage();
    }

    function processExtractedDocument(filename, text) {
        const title = `Uploaded - ${filename}`;
        const newMtg = {
            id: String(meetings.length + 1),
            title: title,
            date: new Date().toISOString().split("T")[0],
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            duration: "10 minutes",
            participants: [],
            tags: ["engineering"],
            status: "Analyzed",
            summary: "",
            actionItems: [],
            decisions: [],
            messages: []
        };

        const participants = ["Priya", "Amit", "Rahul"]; 
        text.split("\n").forEach(line => {
            if (line.includes(":")) {
                const spk = line.split(":", 1)[0].trim();
                if (spk.length < 20 && !participants.includes(spk)) {
                    participants.push(spk);
                }
            }
        });
        newMtg.participants = participants;

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
                    priority: lower.includes("urgent") ? "high" : "medium",
                    status: "Pending"
                });
            }

            const decKws = ["decided", "approved", "agreed", "resolved"];
            if (decKws.some(kw => lower.includes(kw))) {
                newMtg.decisions.push(sent);
            }
        });

        const firstSentences = sentences.slice(0, 2).join(" ");
        newMtg.summary = `## Executive Summary\n${firstSentences || "Document text successfully analyzed."}\n\n## Key Outcomes\nDynamic analysis run on uploaded file.`;

        meetings.push(newMtg);
        saveStateToLocalStorage();

        setTimeout(() => {
            logContainer.classList.add("hidden");
            pushToast("Dynamic document analysis complete!", "success");
            addNotification(`Uploaded file processed: ${filename}`);

            window.location.href = `archive.html?id=${newMtg.id}`;
        }, 800);
    }
}

/* ====================================================
   MEETINGS ARCHIVE VIEW CONTROLLER
   ==================================================== */
function initArchiveView() {
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

    // Check query params for search keywords or direct target ID opening
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("q")) {
        const q = urlParams.get("q");
        document.getElementById("archive-search-input").value = q;
        triggerFilter();
    }
    if (urlParams.has("id")) {
        openMeetingDetails(urlParams.get("id"));
    }
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

function renderMeetingsGrid(list) {
    const container = document.getElementById("meetings-grid-container");
    if (!container) return;

    if (list.length === 0) {
        container.innerHTML = `<p class="empty-feed">No meetings found matching the filters.</p>`;
        return;
    }

    container.innerHTML = list.map(m => `
        <div class="meeting-card" onclick="openMeetingDetails('${m.id}')">
            <div class="card-header">
                <h4><span class="material-symbols-outlined" style="font-size: 18px; color: var(--color-accent-purple); vertical-align: -2px; margin-right: 6px;">folder</span> ${m.title}</h4>
                <span class="badge ${m.status === 'Processing' ? 'amber' : 'green'}">${m.status || 'Analyzed'}</span>
            </div>
            <div class="card-body">
                <p class="meeting-card-excerpt">${m.summary.replace(/#+\s+.*/g, '').substring(0, 120)}...</p>
            </div>
            <div class="card-footer">
                <span class="card-footer-item"><span class="material-symbols-outlined" style="font-size: 14px; vertical-align: -2px; margin-right: 4px;">calendar_today</span> ${m.date}</span>
                <span class="card-footer-item"><span class="material-symbols-outlined" style="font-size: 14px; vertical-align: -2px; margin-right: 4px;">schedule</span> ${m.duration}</span>
                <span class="card-footer-item"><span class="material-symbols-outlined" style="font-size: 14px; vertical-align: -2px; margin-right: 4px;">group</span> ${m.participants.length}</span>
            </div>
        </div>
    `).join("");
}

function openMeetingDetails(id) {
    const mtg = meetings.find(m => m.id === id);
    if (!mtg) return;

    document.getElementById("archive-list-panel").classList.add("hidden");
    const detailsPanel = document.getElementById("archive-details-panel");
    detailsPanel.classList.remove("hidden");
    detailsPanel.setAttribute("data-active-id", id);

    document.getElementById("details-meeting-title").textContent = mtg.title;
    document.getElementById("details-meeting-date").innerHTML = `<span class="material-symbols-outlined" style="font-size: 14px; margin-right: 4px; vertical-align: -2px;">calendar_today</span> ${mtg.date} • ${mtg.time || '10:00 AM'}`;
    document.getElementById("details-meeting-duration").innerHTML = `<span class="material-symbols-outlined" style="font-size: 14px; margin-right: 4px; vertical-align: -2px;">schedule</span> ${mtg.duration}`;
    document.getElementById("details-meeting-participants").innerHTML = `<span class="material-symbols-outlined" style="font-size: 14px; margin-right: 4px; vertical-align: -2px;">group</span> ${mtg.participants.join(", ")}`;

    let htmlSummary = mtg.summary
        .replace(/## (.*)/g, '<h3>$1</h3>')
        .replace(/- (.*)/g, '<li>$1</li>')
        .replace(/\n/g, '<br>');
    document.getElementById("details-summary-content").innerHTML = htmlSummary;

    const actionsBox = document.getElementById("details-actions-list");
    if (mtg.actionItems.length === 0) {
        actionsBox.innerHTML = "<p class='empty-feed'>No action items found.</p>";
    } else {
        actionsBox.innerHTML = mtg.actionItems.map((a, idx) => `
            <div class="checklist-item">
                <input type="checkbox" id="action-chk-${idx}" ${a.status === 'Completed' ? 'checked' : ''} onchange="toggleActionStatus('${mtg.id}', ${idx})">
                <div class="checklist-details">
                    <span class="checklist-title">${a.task}</span>
                    <span class="checklist-meta">Assigned to: <strong>${a.owner}</strong> | Deadline: ${a.deadline} | <span class="badge ${a.priority === 'high' ? 'red' : a.priority === 'medium' ? 'amber' : 'green'}">${a.priority}</span></span>
                </div>
            </div>
        `).join("");
    }

    const decisionsBox = document.getElementById("details-decisions-list");
    if (mtg.decisions.length === 0) {
        decisionsBox.innerHTML = "<p class='empty-feed'>No decisions logged.</p>";
    } else {
        decisionsBox.innerHTML = mtg.decisions.map(d => `
            <li>${d}</li>
        `).join("");
    }

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

    document.querySelectorAll(".tab-btn").forEach(b => {
        b.getAttribute("data-tab") === "tab-summary" ? b.classList.add("active") : b.classList.remove("active");
    });
    document.querySelectorAll(".tab-pane").forEach(p => {
        p.id === "tab-summary" ? p.classList.add("active") : p.classList.remove("active");
    });
}

function showArchiveList() {
    document.getElementById("archive-list-panel").classList.remove("hidden");
    document.getElementById("archive-details-panel").classList.add("hidden");
    renderMeetingsGrid(meetings);
}

function initSearch() {
    const archiveInput = document.getElementById("archive-search-input");
    const categorySelect = document.getElementById("archive-tag-filter");

    archiveInput.addEventListener("input", triggerFilter);
    categorySelect.addEventListener("change", triggerFilter);
}

function triggerFilter() {
    const archiveInput = document.getElementById("archive-search-input");
    const categorySelect = document.getElementById("archive-tag-filter");
    if (!archiveInput) return;

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

/* ====================================================
   SETTINGS PAGE CONTROLLERS
   ==================================================== */
function initSettingsView() {
    syncRoleUI();
    
    document.getElementById("btn-save-retention").addEventListener("click", () => {
        if (currentUserRole !== "Admin") return;
        const days = document.getElementById("settings-retention").value;
        pushToast(`Data retention period saved to ${days} days!`, "success");
        addNotification(`Data retention cycle policy adjusted to ${days} days.`);
    });
}

/* ====================================================
   MARKDOWN EXPORTER
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
            md += `- [${a.status === 'Completed' ? 'x' : ' '}] ${a.task} (Owner: ${a.owner} | Due: ${a.deadline} | Priority: ${a.priority})\n`;
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
   TOAST POPUPS
   ==================================================== */
function pushToast(message, type = "info") {
    const container = document.getElementById("toast-container");
    if (!container) return;
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    
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

    const timeout = setTimeout(() => {
        toast.remove();
    }, 5000);

    toast.querySelector(".toast-close").addEventListener("click", () => {
        clearTimeout(timeout);
        toast.remove();
    });
}
