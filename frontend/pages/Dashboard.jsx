import React, { useState } from 'react';
import StatCard from '../components/StatCard';
import MeetingCard from '../components/MeetingCard';
import ActionItem from '../components/ActionItem';

export default function Dashboard({
  meetings = [],
  onDeleteMeeting,
  onToggleActionItem,
  onAddActionItem,
  searchQuery = '',
  userRole = 'Member'
}) {
  const [priorityFilter, setPriorityFilter] = useState('all');

  // Compute metrics dynamically from state
  const timeSaved = meetings.length * 2.5; // Assume 2.5 hrs saved per analyzed meeting
  const totalMeetingsCount = meetings.length;
  
  // Flatten action items
  const allActions = meetings.reduce((acc, m) => {
    if (m.actionItems) {
      // Attach meeting ID to identify item later
      const items = m.actionItems.map((item, idx) => ({
        ...item,
        meetingId: m.id,
        itemIndex: idx
      }));
      return [...acc, ...items];
    }
    return acc;
  }, []);

  const pendingActionsCount = allActions.filter(a => a.status === 'Pending').length;
  const completedActionsCount = allActions.filter(a => a.status === 'Completed').length;
  const completionRate = allActions.length > 0 
    ? Math.round((completedActionsCount / allActions.length) * 100) 
    : 0;

  // Filter meetings by search query
  const filteredMeetings = meetings.filter(m => {
    const q = searchQuery.toLowerCase();
    return (
      m.title.toLowerCase().includes(q) ||
      (m.tags && m.tags.some(t => t.toLowerCase().includes(q))) ||
      (m.participants && m.participants.some(p => p.toLowerCase().includes(q)))
    );
  });

  // Filter actions by priority tab
  const filteredActions = allActions.filter(a => {
    if (priorityFilter === 'all') return true;
    return a.priority.toLowerCase() === priorityFilter.toLowerCase();
  });

  // SVG Progress Ring Offset
  // Radius = 45, Circumference = 2 * PI * R = 282.7
  const circumference = 282.7;
  const strokeDashoffset = circumference - (completionRate / 100) * circumference;

  return (
    <div className="view-panel">
      {/* Greeting Row */}
      <div className="dashboard-greeting-row">
        <div className="view-header">
          <h2>Welcome back, Priya!</h2>
          <p className="subtitle">Here's what's happening with your meetings today.</p>
        </div>
        <div className="date-picker-widget">
          <span className="material-symbols-outlined" style={{ fontSize: '16px', marginRight: '6px' }}>
            calendar_today
          </span>
          <span>July 13 - July 19, 2026</span>
        </div>
      </div>

      {/* Statistics Cards Telemetry */}
      <div className="stats-grid">
        <StatCard
          label="Time Saved"
          value={`${timeSaved.toFixed(1)} hrs`}
          changeText="↑ 15% vs last week"
          theme="purple-theme"
          sparklinePath="M0 15 Q25 5 50 12 T100 2"
          strokeColor="#8B5CF6"
        />
        <StatCard
          label="Meetings Analyzed"
          value={`${totalMeetingsCount} total`}
          changeText="↑ 20% vs last week"
          theme="blue-theme"
          sparklinePath="M0 18 Q25 12 50 8 T100 3"
          strokeColor="#3F83F8"
        />
        <StatCard
          label="Actions Pending"
          value={String(pendingActionsCount)}
          changeText="↓ 5% vs last week"
          theme="pink-theme"
          sparklinePath="M0 5 Q25 15 50 8 T100 14"
          strokeColor="#E52E71"
        />
        <StatCard
          label="AI Uptime"
          value="99.9%"
          changeText="↑ 2% vs last week"
          theme="green-theme"
          sparklinePath="M0 10 Q25 5 50 6 T100 2"
          strokeColor="#10B981"
        />
      </div>

      {/* SVG Charts Rows */}
      <div className="analytics-charts-row">
        {/* Trend Area Line Chart */}
        <div className="analytics-card trend-card">
          <div className="chart-header">
            <h3>Time Saved Trend</h3>
            <span className="chart-meta-dropdown">This Week</span>
          </div>
          <div className="chart-content">
            <svg viewBox="0 0 400 120" className="trend-svg">
              <defs>
                <linearGradient id="trend-area-grad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#8B5CF6" stopOpacity="0.3" />
                  <stop offset="100%" stopColor="#8B5CF6" stopOpacity="0.0" />
                </linearGradient>
              </defs>
              <line x1="20" y1="20" x2="380" y2="20" stroke="#243249" strokeDasharray="4 4" />
              <line x1="20" y1="50" x2="380" y2="50" stroke="#243249" strokeDasharray="4 4" />
              <line x1="20" y1="80" x2="380" y2="80" stroke="#243249" strokeDasharray="4 4" />
              <line x1="20" y1="110" x2="380" y2="110" stroke="#243249" strokeDasharray="4 4" />

              <path
                d="M 20 120 L 20 100 Q 80 95 140 115 T 260 50 T 380 40 L 380 120 Z"
                fill="url(#trend-area-grad)"
              />
              <path
                d="M 20 100 Q 80 95 140 115 T 260 50 T 380 40"
                fill="none"
                stroke="#8B5CF6"
                strokeWidth="3"
              />

              <circle cx="260" cy="50" r="5" fill="#8B5CF6" />
              <circle cx="260" cy="50" r="10" fill="none" stroke="#8B5CF6" strokeWidth="1.5" opacity="0.5" />
            </svg>
            <div className="chart-tooltip" style={{ top: '15px', left: '210px' }}>
              <span className="tooltip-title">Thu, July 16</span>
              <span className="tooltip-val">{timeSaved.toFixed(1)} hrs</span>
            </div>
            <div className="chart-axes">
              <span>Mon</span>
              <span>Tue</span>
              <span>Wed</span>
              <span>Thu</span>
              <span>Fri</span>
              <span>Sat</span>
              <span>Sun</span>
            </div>
          </div>
        </div>

        {/* Category breakdown donut segment */}
        <div className="analytics-card category-card">
          <div className="chart-header">
            <h3>Meetings by Category</h3>
          </div>
          <div className="chart-donut-container">
            <svg viewBox="0 0 120 120" className="donut-svg">
              <circle cx="60" cy="60" r="45" fill="none" stroke="#243249" strokeWidth="10" />
              {/* Render dynamic donut portions matching Figma layout seeds */}
              <circle cx="60" cy="60" r="45" fill="none" stroke="#3F83F8" strokeWidth="10"
                strokeDasharray="282.7" strokeDashoffset="113"
                transform="rotate(-90 60 60)" />
              <circle cx="60" cy="60" r="45" fill="none" stroke="#8B5CF6" strokeWidth="10"
                strokeDasharray="282.7" strokeDashoffset="183.7"
                transform="rotate(54 60 60)" />
              <circle cx="60" cy="60" r="45" fill="none" stroke="#E52E71" strokeWidth="10"
                strokeDasharray="282.7" strokeDashoffset="226.1"
                transform="rotate(144 60 60)" />
              <text x="60" y="58" textAnchor="middle" fontFamily="Outfit" fontWeight="bold" fontSize="16" fill="#F3F4F6">
                {totalMeetingsCount}
              </text>
              <text x="60" y="74" textAnchor="middle" fontFamily="Inter" fontSize="9" fill="#9CA3AF">
                Total
              </text>
            </svg>
            <div className="donut-legend">
              <div className="legend-item"><span className="color-dot blue"></span> Planning</div>
              <div className="legend-item"><span className="color-dot purple"></span> Marketing</div>
              <div className="legend-item"><span className="color-dot pink"></span> Operations</div>
            </div>
          </div>
        </div>

        {/* Action Completion dial ring */}
        <div className="analytics-card progress-card">
          <div className="chart-header">
            <h3>Actions Overview</h3>
          </div>
          <div className="chart-donut-container justify-center">
            <svg viewBox="0 0 120 120" className="progress-ring-svg">
              <circle cx="60" cy="60" r="45" fill="none" stroke="#243249" strokeWidth="10" />
              <circle
                cx="60"
                cy="60"
                r="45"
                fill="none"
                stroke="#10B981"
                strokeWidth="10"
                strokeDasharray={String(circumference)}
                strokeDashoffset={String(strokeDashoffset)}
                transform="rotate(-90 60 60)"
              />
              <text x="60" y="58" textAnchor="middle" fontFamily="Outfit" fontWeight="bold" fontSize="16" fill="#F3F4F6">
                {completionRate}%
              </text>
              <text x="60" y="74" textAnchor="middle" fontFamily="Inter" fontSize="9" fill="#9CA3AF">
                Completed
              </text>
            </svg>
            <div className="donut-legend inline-legend">
              <div className="legend-item"><span className="color-dot green"></span> Done ({completedActionsCount})</div>
              <div className="legend-item"><span className="color-dot border-gray"></span> Pending ({pendingActionsCount})</div>
            </div>
          </div>
        </div>
      </div>

      {/* Split Card Row */}
      <div className="dashboard-split">
        {/* Recent Meetings Table */}
        <div className="split-card recent-meetings-card">
          <div className="card-header">
            <h3>Recent Meetings</h3>
            <span style={{ fontSize: '11px', color: 'var(--color-text-secondary)' }}>
              Showing {filteredMeetings.length} of {meetings.length}
            </span>
          </div>
          <div className="table-container">
            <table className="dashboard-table">
              <thead>
                <tr>
                  <th>Meeting Title</th>
                  <th>Date & Time</th>
                  <th>Participants</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {filteredMeetings.length > 0 ? (
                  filteredMeetings.map((meeting) => (
                    <MeetingCard
                      key={meeting.id}
                      meeting={meeting}
                      userRole={userRole}
                      onDelete={onDeleteMeeting}
                    />
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" style={{ textAlign: 'center', padding: '24px', color: 'var(--color-text-secondary)' }}>
                      No meetings matched your query.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Action Checklist Board */}
        <div className="split-card action-checklist-card">
          <div className="card-header">
            <h3>Aggregated Action Items</h3>
            <span style={{ fontSize: '11px', color: 'var(--color-text-secondary)' }}>
              ({pendingActionsCount} pending)
            </span>
          </div>
          <div className="priority-tabs-bar">
            <button
              onClick={() => setPriorityFilter('all')}
              className={`p-tab ${priorityFilter === 'all' ? 'active' : ''}`}
            >
              All ({allActions.length})
            </button>
            <button
              onClick={() => setPriorityFilter('high')}
              className={`p-tab ${priorityFilter === 'high' ? 'active' : ''}`}
            >
              High ({allActions.filter(a => a.priority.toLowerCase() === 'high').length})
            </button>
            <button
              onClick={() => setPriorityFilter('medium')}
              className={`p-tab ${priorityFilter === 'medium' ? 'active' : ''}`}
            >
              Med ({allActions.filter(a => a.priority.toLowerCase() === 'medium').length})
            </button>
            <button
              onClick={() => setPriorityFilter('low')}
              className={`p-tab ${priorityFilter === 'low' ? 'active' : ''}`}
            >
              Low ({allActions.filter(a => a.priority.toLowerCase() === 'low').length})
            </button>
          </div>
          <div className="checklist-container" role="list">
            {filteredActions.length > 0 ? (
              filteredActions.map((action, idx) => (
                <ActionItem
                  key={`${action.meetingId}-${action.itemIndex}`}
                  action={action}
                  onToggle={() => onToggleActionItem(action.meetingId, action.itemIndex)}
                />
              ))
            ) : (
              <div style={{ textAlign: 'center', padding: '24px', color: 'var(--color-text-secondary)', fontSize: '12px' }}>
                No actions found for this category.
              </div>
            )}
          </div>

          <button 
            className="add-action-item-btn" 
            onClick={onAddActionItem}
            title="Shortcuts a pre-configured action item for test"
          >
            + Add Test Action Item
          </button>
        </div>
      </div>
    </div>
  );
}
