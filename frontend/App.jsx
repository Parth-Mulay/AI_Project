import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import UploadMeeting from './pages/UploadMeeting';

export default function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [userRole, setUserRole] = useState('Member');
  const [searchQuery, setSearchQuery] = useState('');
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  // Default seed data matches the Figma prototype
  const [meetings, setMeetings] = useState([
    {
      id: "1",
      title: "Government Planning Sync - 2027 Agenda",
      date: "2026-07-13",
      time: "10:00 AM",
      duration: "45 minutes",
      participants: ["Sharma", "Iyer", "Khan", "Deshmukh", "Patel"],
      tags: ["planning"],
      status: "Analyzed",
      summary: `## Executive Summary
All departments aligned key projects under the technological growth agenda. Major agreements included a 20% budget expansion for clean energy and digital code basics integration.

## Key Discussion Points
- Funding allocations for clean wind infrastructure.
- Improving rural clinical healthcare capacities.
- Initiating district-level digital literacy classes.

## Risks
- Rural clinical facility staffing gaps must be solved.`,
      actionItems: [
        { task: "Task force will be formed to assess rural healthcare gaps within three months.", owner: "Iyer", deadline: "Oct 13", priority: "Medium", status: "Pending" },
        { task: "A feasibility study on AI driven traffic management will be commissioned.", owner: "Deshmukh", deadline: "Dec 20", priority: "Low", status: "Pending" },
        { task: "Ministries will submit integrated action plans by March 2027.", owner: "Sharma", deadline: "Mar 30", priority: "Low", status: "Pending" }
      ],
      decisions: [
        "Launch a pilot program in 10 districts integrating coding and AI basics into curricula.",
        "Introduce a subsidy scheme for drought resistant seeds."
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
      status: "Completed",
      summary: `## Executive Summary
Brian raised a compliance concern regarding the deployment server's resource constraints. Priya agreed to conduct a thorough security assessment prior to launch.

## Key Discussion Points
- Server capability reviews.
- Performance profiling checks.

## Risks
- Blocker: Deployment server has limited RAM allocation.`,
      actionItems: [
        { task: "Priya will conduct a security review before launch.", owner: "Priya", deadline: "Jul 22", priority: "High", status: "Pending" }
      ],
      decisions: [
        "Agreed to hold release updates until performance profiles are signed off."
      ]
    },
    {
      id: "3",
      title: "Sprint Planning - Week 14",
      date: "2026-07-06",
      time: "11:00 AM",
      duration: "30 minutes",
      participants: ["Rahul", "Priya", "Amit"],
      tags: ["planning"],
      status: "Failed - Used Fallback",
      summary: `## Executive Summary
Rahul confirmed that the core authentication module is fully completed. The team discussed security configurations and resolved to implement JWT-based token management for cross-origin compliance.

## Key Discussion Points
- Authentication modules development cycle complete.
- Migration protocols and token setups.
- Database mapping rules.

## Risks
- Need to align schemas before staging deployments.`,
      actionItems: [
        { task: "Rahul will review the database API schema tomorrow.", owner: "Rahul", deadline: "Jul 20", priority: "High", status: "Pending" },
        { task: "Priya will deploy the cache layer by Friday.", owner: "Priya", deadline: "Jul 18", priority: "High", status: "Pending" }
      ],
      decisions: [
        "We decided to use JWT for token management."
      ]
    }
  ]);

  const [notifications, setNotifications] = useState([
    { text: "Welcome to AI Meeting Notes Manager Dashboard!", time: "Just now" },
    { text: "Loaded 3 historical documents from database sync.", time: "1 min ago" }
  ]);

  const handleToggleRole = () => {
    setUserRole((prev) => {
      const newRole = prev === 'Member' ? 'Admin' : 'Member';
      addNotification(`Switched user role to ${newRole}.`);
      return newRole;
    });
  };

  const addNotification = (text) => {
    setNotifications((prev) => [
      { text, time: 'Just now' },
      ...prev.slice(0, 4) // Keep last 5 notifications
    ]);
  };

  const handleAddMeeting = (meeting) => {
    setMeetings((prev) => [meeting, ...prev]);
    addNotification(`Processed meeting: "${meeting.title}"`);
  };

  const handleDeleteMeeting = (meetingId) => {
    if (userRole !== 'Admin') {
      addNotification("Action Denied: Administrator role required to delete meetings.");
      return;
    }
    const meetingToDelete = meetings.find(m => m.id === meetingId);
    setMeetings((prev) => prev.filter((m) => m.id !== meetingId));
    addNotification(`Deleted meeting: "${meetingToDelete?.title || 'Unknown'}"`);
  };

  const handleToggleActionItem = (meetingId, itemIndex) => {
    setMeetings((prev) =>
      prev.map((meeting) => {
        if (meeting.id === meetingId) {
          const updatedItems = meeting.actionItems.map((item, idx) => {
            if (idx === itemIndex) {
              const newStatus = item.status === 'Completed' ? 'Pending' : 'Completed';
              addNotification(`Marked task "${item.task.slice(0, 20)}..." as ${newStatus}`);
              return { ...item, status: newStatus };
            }
            return item;
          });
          return { ...meeting, actionItems: updatedItems };
        }
        return meeting;
      })
    );
  };

  const handleShortcutAddActionItem = () => {
    // Inserts a test action item in the first meeting to showcase reactivity
    if (meetings.length === 0) return;
    
    setMeetings((prev) => {
      const copy = [...prev];
      const targetMeeting = copy[0];
      const newItem = {
        task: "Verify WCAG 2.1 accessibility constraints",
        owner: "Priya",
        deadline: "ASAP",
        priority: "High",
        status: "Pending"
      };
      
      copy[0] = {
        ...targetMeeting,
        actionItems: [...(targetMeeting.actionItems || []), newItem]
      };
      
      addNotification("Added new test action item.");
      return copy;
    });
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <Sidebar
        currentPage={currentPage}
        onPageChange={setCurrentPage}
        userRole={userRole}
        mobileOpen={mobileSidebarOpen}
        onCloseMobile={() => setMobileSidebarOpen(false)}
      />

      {/* Main Content Area */}
      <main className="main-canvas">
        <Navbar
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          userRole={userRole}
          onToggleRole={handleToggleRole}
          onToggleMobileSidebar={() => setMobileSidebarOpen(!mobileSidebarOpen)}
          notifications={notifications}
        />

        <div className="canvas-content">
          {currentPage === 'dashboard' ? (
            <Dashboard
              meetings={meetings}
              onDeleteMeeting={handleDeleteMeeting}
              onToggleActionItem={handleToggleActionItem}
              onAddActionItem={handleShortcutAddActionItem}
              searchQuery={searchQuery}
              userRole={userRole}
            />
          ) : (
            <UploadMeeting
              onAddMeeting={handleAddMeeting}
              onPageChange={setCurrentPage}
            />
          )}
        </div>
      </main>
    </div>
  );
}
