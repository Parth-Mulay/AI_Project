/**
 * validators.js — Shared Form Validation Helpers
 *
 * Returns an error string on failure, or empty string on success.
 * Pure functions — no side effects.
 */

import env from '../config/env.js';
import { ALLOWED_DOC_EXTENSIONS, ALLOWED_AUDIO_EXTENSIONS } from '../config/constants.js';

// ---------------------------------------------------------------------------
// Field Validators
// ---------------------------------------------------------------------------

/**
 * Validate a required string field.
 * @param {string} value
 * @param {string} fieldName — used in the error message
 * @param {number} minLength
 * @returns {string} error or ''
 */
export function validateRequired(value, fieldName = 'This field', minLength = 1) {
  if (!value || !String(value).trim()) return `${fieldName} is required.`;
  if (String(value).trim().length < minLength) {
    return `${fieldName} must be at least ${minLength} characters.`;
  }
  return '';
}

/**
 * Validate a comma-separated participant list.
 * @param {string} value
 * @param {number} min — minimum number of participants
 * @returns {string} error or ''
 */
export function validateParticipants(value, min = 2) {
  if (!value || !value.trim()) return 'Please specify participants.';
  const list = value.split(',').map((p) => p.trim()).filter(Boolean);
  if (list.length < min) {
    return `Please list at least ${min} participants (comma-separated).`;
  }
  return '';
}

/**
 * Validate a positive integer duration.
 * @param {string|number} value
 * @returns {string} error or ''
 */
export function validateDuration(value) {
  const n = parseInt(value, 10);
  if (!value || isNaN(n) || n <= 0) return 'Please provide a valid duration in minutes.';
  return '';
}

/**
 * Validate a datetime-local input.
 * @param {string} value
 * @returns {string} error or ''
 */
export function validateDatetime(value) {
  if (!value) return 'Meeting date & time is required.';
  return '';
}

// ---------------------------------------------------------------------------
// File Validators
// ---------------------------------------------------------------------------

/**
 * Validate an uploaded file against allowed extensions and size limits.
 * NOTE: Client-side validation only — server MUST also validate.
 * TODO(security): Backend must re-validate file content via magic bytes.
 *
 * @param {File} file
 * @returns {string} error or ''
 */
export function validateUploadedFile(file) {
  if (!file) return 'Please upload a meeting document or audio file.';

  const extension = file.name.split('.').pop().toLowerCase();
  const isDoc = ALLOWED_DOC_EXTENSIONS.includes(extension);
  const isAudio = ALLOWED_AUDIO_EXTENSIONS.includes(extension);

  if (!isDoc && !isAudio) {
    return `Invalid extension .${extension}. Permitted: ${[...ALLOWED_DOC_EXTENSIONS, ...ALLOWED_AUDIO_EXTENSIONS].join(', ')}`;
  }

  const limit = isAudio ? env.UPLOAD_LIMIT_AUDIO_BYTES : env.UPLOAD_LIMIT_DOCS_BYTES;
  const limitMb = isAudio ? env.UPLOAD_LIMIT_AUDIO_MB : env.UPLOAD_LIMIT_DOCS_MB;

  if (file.size > limit) {
    return `File size exceeds the ${limitMb}MB limit for ${isAudio ? 'audio' : 'document'} files.`;
  }

  return '';
}

// ---------------------------------------------------------------------------
// Upload Form
// ---------------------------------------------------------------------------

/**
 * Validate the entire upload form, returning an errors object.
 * @param {Object} formData
 * @returns {{ [field: string]: string }}
 */
export function validateUploadForm(formData) {
  const errors = {};

  const titleErr = validateRequired(formData.title, 'Meeting Title', 5);
  if (titleErr) errors.title = titleErr;

  const dtErr = validateDatetime(formData.datetime);
  if (dtErr) errors.datetime = dtErr;

  const durErr = validateDuration(formData.duration);
  if (durErr) errors.duration = durErr;

  const partErr = validateParticipants(formData.participants, 2);
  if (partErr) errors.participants = partErr;

  const fileErr = validateUploadedFile(formData.file);
  if (fileErr) errors.file = fileErr;

  return errors;
}
