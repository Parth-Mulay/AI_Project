/**
 * formatters.js — Shared Display Formatting Utilities
 *
 * Pure functions with no side effects.
 * Import individually to keep tree-shaking effective.
 */

// ---------------------------------------------------------------------------
// Date & Time
// ---------------------------------------------------------------------------

/**
 * Format an ISO date string to a human-readable date.
 * @param {string} isoDate — e.g. "2026-07-13"
 * @returns {string} — e.g. "Jul 13, 2026"
 */
export function formatDate(isoDate) {
  if (!isoDate) return '—';
  const date = new Date(isoDate);
  if (isNaN(date.getTime())) return isoDate;
  return date.toLocaleDateString('en-IN', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

/**
 * Format a datetime-local string to a short time display.
 * @param {string} datetime
 * @returns {string} — e.g. "10:00 AM"
 */
export function formatTime(datetime) {
  if (!datetime) return '—';
  const date = new Date(datetime);
  if (isNaN(date.getTime())) return datetime;
  return date.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
}

/**
 * Return a relative time label ("Just now", "5 min ago", etc.)
 * @param {Date|string} timestamp
 * @returns {string}
 */
export function formatRelativeTime(timestamp) {
  const now = new Date();
  const past = new Date(timestamp);
  const diffMs = now - past;
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return 'Just now';
  if (diffMin < 60) return `${diffMin} min ago`;
  const diffHr = Math.floor(diffMin / 60);
  if (diffHr < 24) return `${diffHr} hr ago`;
  return formatDate(past.toISOString());
}

// ---------------------------------------------------------------------------
// File Size
// ---------------------------------------------------------------------------

/**
 * Format bytes into a human-readable string.
 * @param {number} bytes
 * @returns {string} — e.g. "4.2 MB"
 */
export function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${units[i]}`;
}

// ---------------------------------------------------------------------------
// Duration
// ---------------------------------------------------------------------------

/**
 * Format a duration number into a readable label.
 * @param {number|string} minutes
 * @returns {string} — e.g. "45 minutes" or "1 hr 30 min"
 */
export function formatDuration(minutes) {
  const m = parseInt(minutes, 10);
  if (isNaN(m) || m <= 0) return '—';
  if (m < 60) return `${m} minutes`;
  const hrs = Math.floor(m / 60);
  const rem = m % 60;
  return rem > 0 ? `${hrs} hr ${rem} min` : `${hrs} hr`;
}

// ---------------------------------------------------------------------------
// Text
// ---------------------------------------------------------------------------

/**
 * Truncate a string to a maximum character count.
 * @param {string} text
 * @param {number} max — default 120
 * @returns {string}
 */
export function truncate(text, max = 120) {
  if (!text) return '';
  return text.length <= max ? text : `${text.slice(0, max)}…`;
}

/**
 * Capitalize the first letter of a string.
 * @param {string} str
 * @returns {string}
 */
export function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}
