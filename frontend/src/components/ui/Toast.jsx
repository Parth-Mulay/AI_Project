import React, { useEffect } from 'react';

/**
 * Toast — Individual toast notification
 *
 * Types: info | success | error | warning
 *
 * Security: text is rendered via React text nodes — no HTML injection.
 */
export default function Toast({ notification, onDismiss }) {
  const { id, text, type = 'info' } = notification;

  const iconMap = {
    info: 'info',
    success: 'check_circle',
    error: 'error',
    warning: 'warning',
  };

  const colorMap = {
    info: 'var(--color-accent-blue)',
    success: 'var(--color-accent-green)',
    error: 'var(--color-accent-pink)',
    warning: 'var(--color-accent-yellow)',
  };

  return (
    <div className={`toast toast-${type}`} role="alert" aria-live="polite">
      <span
        className="material-symbols-outlined"
        style={{ fontSize: '18px', color: colorMap[type], flexShrink: 0 }}
        aria-hidden="true"
      >
        {iconMap[type]}
      </span>
      <span className="toast-text">{text}</span>
      <button
        className="toast-close-btn"
        onClick={() => onDismiss(id)}
        aria-label="Dismiss notification"
      >
        <span className="material-symbols-outlined" style={{ fontSize: '16px' }}>close</span>
      </button>
    </div>
  );
}
