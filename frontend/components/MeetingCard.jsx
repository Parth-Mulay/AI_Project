import React, { useState } from 'react';

export default function MeetingCard({ meeting, userRole = 'Member', onDelete }) {
  const [expanded, setExpanded] = useState(false);

  const getStatusBadgeClass = (status) => {
    if (!status) return 'badge processing';
    const s = status.toLowerCase();
    if (s.includes('analyzed')) return 'badge analyzed';
    if (s.includes('completed')) return 'badge completed';
    if (s.includes('failed')) return 'badge failed';
    return 'badge processing';
  };

  const getAvatarLetters = (name) => {
    if (!name) return '?';
    return name.charAt(0).toUpperCase();
  };

  const hasAccessToDelete = userRole === 'Admin';

  return (
    <>
      <tr 
        onClick={() => setExpanded(!expanded)} 
        style={{ cursor: 'pointer' }}
        aria-expanded={expanded}
      >
        <td className="meeting-title-cell">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="material-symbols-outlined" style={{ fontSize: '18px', color: 'var(--color-accent-purple)' }}>
              {expanded ? 'keyboard_arrow_down' : 'keyboard_arrow_right'}
            </span>
            {meeting.title}
          </div>
        </td>
        <td>
          <div>{meeting.date}</div>
          <div style={{ fontSize: '10px', color: 'var(--color-text-secondary)' }}>
            {meeting.time || '10:00 AM'} ({meeting.duration || '30m'})
          </div>
        </td>
        <td>
          <div className="participants-stacked">
            {meeting.participants && meeting.participants.slice(0, 3).map((p, idx) => (
              <div 
                key={idx} 
                className="avatar-stack-item" 
                title={p}
              >
                {getAvatarLetters(p)}
              </div>
            ))}
            {meeting.participants && meeting.participants.length > 3 && (
              <div className="avatar-stack-item more" title={`${meeting.participants.length - 3} more`}>
                +{meeting.participants.length - 3}
              </div>
            )}
          </div>
        </td>
        <td>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '10px' }}>
            <span className={getStatusBadgeClass(meeting.status)}>
              {meeting.status}
            </span>
            {hasAccessToDelete && onDelete && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete(meeting.id);
                }}
                className="top-btn btn-small"
                style={{
                  border: '1px solid var(--color-accent-red)',
                  color: 'var(--color-accent-red)',
                  background: 'rgba(239, 68, 68, 0.05)',
                  padding: '3px 8px',
                  borderRadius: '4px'
                }}
                aria-label={`Delete meeting: ${meeting.title}`}
              >
                Delete
              </button>
            )}
          </div>
        </td>
      </tr>
      
      {/* Expandable summary details drawer */}
      {expanded && (
        <tr>
          <td colSpan="4" style={{ backgroundColor: 'rgba(22, 30, 46, 0.25)', padding: '16px 24px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div>
                <h4 style={{ fontSize: '12px', color: 'var(--color-accent-purple)', marginBottom: '4px', textTransform: 'uppercase' }}>
                  🤖 AI Summary
                </h4>
                <p style={{ color: 'var(--color-text-primary)', fontSize: '13px', lineHeight: '1.6', whiteSpace: 'pre-line' }}>
                  {meeting.summary ? meeting.summary.replace(/##\s+/g, '').replace(/-\s+/g, '• ') : 'No summary data available.'}
                </p>
              </div>

              {meeting.actionItems && meeting.actionItems.length > 0 && (
                <div>
                  <h4 style={{ fontSize: '12px', color: 'var(--color-accent-blue)', marginBottom: '4px', textTransform: 'uppercase' }}>
                    📝 Extracted Action Items
                  </h4>
                  <ul style={{ listStyleType: 'none', paddingLeft: '0', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    {meeting.actionItems.map((item, idx) => (
                      <li key={idx} style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>
                        <span style={{ color: 'var(--color-accent-blue)', marginRight: '6px' }}>•</span>
                        <strong>{item.owner}</strong>: {item.task} (Due: {item.deadline})
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {meeting.decisions && meeting.decisions.length > 0 && (
                <div>
                  <h4 style={{ fontSize: '12px', color: 'var(--color-accent-green)', marginBottom: '4px', textTransform: 'uppercase' }}>
                    💡 Key Decisions
                  </h4>
                  <ul style={{ listStyleType: 'none', paddingLeft: '0', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    {meeting.decisions.map((dec, idx) => (
                      <li key={idx} style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>
                        <span style={{ color: 'var(--color-accent-green)', marginRight: '6px' }}>✔</span> {dec}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </td>
        </tr>
      )}
    </>
  );
}
