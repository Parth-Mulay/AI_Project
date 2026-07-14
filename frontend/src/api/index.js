/**
 * api/index.js — API Layer Re-exports
 *
 * Convenience barrel file so callers can do:
 *   import apiClient, { ApiError } from '../api';
 */

export { default, ApiError } from './apiClient.js';
