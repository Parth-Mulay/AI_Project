import React from 'react';

export default function ActionItem({ action, onToggle }) {
  const isChecked = action.status === 'Completed';

  return (
    <div className="checklist-item" role="listitem">
      <div className="chk-box-wrap" onClick={onToggle} role="checkbox" aria-checked={isChecked}>
        <div className={`checkbox-custom ${isChecked ? 'checked' : ''}`}>
          {isChecked && <span className="check-symbol">✓</span>}
        </div>
      </div>

      <div className="chk-content">
        <span className={`chk-title ${isChecked ? 'checked-line' : ''}`}>
          {action.task}
        </span>
        <div className="chk-meta">
          <span>Assignee: <strong>{action.owner}</strong></span>
          <span>Due: {action.deadline}</span>
          <span className={`item-p-badge ${action.priority ? action.priority.toLowerCase() : 'low'}`}>
            {action.priority}
          </span>
        </div>
      </div>
    </div>
  );
}
