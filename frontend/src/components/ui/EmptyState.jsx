import React from 'react';

/**
 * EmptyState — Professional empty state display with SVG illustration
 *
 * Props:
 *   icon    — material symbol name
 *   title   — headline text
 *   message — descriptive text
 *   action  — { label, onClick } optional CTA button
 */
export default function EmptyState({ icon = 'inbox', title = 'Nothing here yet', message = 'Add content to get started.', action }) {
  return (
    <div className="state-container">
      {/* Decorative SVG illustration */}
      <div className="empty-state-illustration" aria-hidden="true">
        <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
          <circle cx="40" cy="40" r="38" fill="rgba(139, 92, 246, 0.08)" stroke="rgba(139, 92, 246, 0.2)" strokeWidth="1.5" />
          <circle cx="40" cy="40" r="26" fill="rgba(139, 92, 246, 0.06)" />
          <text x="40" y="48" textAnchor="middle" fontSize="24" fill="rgba(139, 92, 246, 0.6)" fontFamily="Material Symbols Outlined">{icon}</text>
        </svg>
        <span className="material-symbols-outlined state-icon" style={{ color: 'var(--color-accent-purple)', opacity: 0.7 }}>
          {icon}
        </span>
      </div>
      <h3 className="state-title">{title}</h3>
      <p className="state-body">{message}</p>
      {action && (
        <button className="btn btn-primary" onClick={action.onClick} style={{ marginTop: '12px' }}>
          {action.label}
        </button>
      )}
    </div>
  );
}
