import React from 'react';

/**
 * ErrorState — Friendly error display with optional retry button
 *
 * Props:
 *   title   — short headline
 *   message — descriptive error text (generic, no raw server detail)
 *   onRetry — callback for retry button (omit to hide button)
 *   isOffline — shows offline-specific icon and message
 *   isTimeout — shows timeout-specific message
 */
export default function ErrorState({ title, message, onRetry, isOffline = false, isTimeout = false }) {
  const icon = isOffline ? 'wifi_off' : isTimeout ? 'timer_off' : 'error_outline';
  const headline = title ?? (isOffline ? 'You appear to be offline' : isTimeout ? 'Request timed out' : 'Something went wrong');
  const body = message ?? (isOffline
    ? 'Check your internet connection and try again.'
    : isTimeout
    ? 'The server took too long to respond. Please try again.'
    : 'An unexpected error occurred. Please try again.');

  return (
    <div className="state-container" role="alert">
      <span className="material-symbols-outlined state-icon" style={{ color: 'var(--color-accent-pink)' }}>
        {icon}
      </span>
      <h3 className="state-title">{headline}</h3>
      <p className="state-body">{body}</p>
      {onRetry && (
        <button className="btn btn-secondary" onClick={onRetry} style={{ marginTop: '12px' }}>
          <span className="material-symbols-outlined" style={{ fontSize: '16px', marginRight: '6px', verticalAlign: 'middle' }}>refresh</span>
          Try Again
        </button>
      )}
    </div>
  );
}
