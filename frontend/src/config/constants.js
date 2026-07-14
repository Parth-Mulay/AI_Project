/**
 * constants.js — App-Wide Constants
 *
 * Route paths, labels, and other shared constants.
 * Import from this file instead of hard-coding strings in components.
 */

// ---------------------------------------------------------------------------
// Route Paths
// ---------------------------------------------------------------------------
export const ROUTES = {
  HOME: '/',
  LIVE_CAPTURE: '/live-capture',
  UPLOAD: '/upload',
  MEETINGS: '/meetings',
  MEETING_DETAIL: '/meeting/:id',
  SEARCH: '/search',
  WORKSPACE: '/workspace',
  SETTINGS: '/settings',
  PROFILE: '/profile',
  NOT_FOUND: '/not-found',
};

/**
 * Build the concrete URL for a meeting detail page.
 * @param {string} id — meeting identifier
 * @returns {string} e.g. "/meeting/abc123"
 */
export const meetingDetailPath = (id) => `/meeting/${id}`;

// ---------------------------------------------------------------------------
// File Upload
// ---------------------------------------------------------------------------
export const ALLOWED_DOC_EXTENSIONS = ['docx', 'pdf', 'txt'];
export const ALLOWED_AUDIO_EXTENSIONS = ['mp3', 'wav'];
export const ALLOWED_EXTENSIONS = [...ALLOWED_DOC_EXTENSIONS, ...ALLOWED_AUDIO_EXTENSIONS];

// ---------------------------------------------------------------------------
// Meeting Status Labels
// ---------------------------------------------------------------------------
export const MEETING_STATUS = {
  ANALYZED: 'Analyzed',
  COMPLETED: 'Completed',
  PROCESSING: 'Processing',
  FAILED: 'Failed - Used Fallback',
  PENDING: 'Pending',
};

// ---------------------------------------------------------------------------
// Priority Labels
// ---------------------------------------------------------------------------
export const PRIORITY = {
  HIGH: 'High',
  MEDIUM: 'Medium',
  LOW: 'Low',
};

// ---------------------------------------------------------------------------
// Action Item Status
// ---------------------------------------------------------------------------
export const ACTION_STATUS = {
  PENDING: 'Pending',
  COMPLETED: 'Completed',
};

// ---------------------------------------------------------------------------
// Notification Limits
// ---------------------------------------------------------------------------
export const MAX_NOTIFICATIONS = 5;
