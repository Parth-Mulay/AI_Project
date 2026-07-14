/**
 * apiClient.js — Centralized Axios HTTP Client
 *
 * All API calls go through this module. Never call axios directly
 * from UI components — always use the service layer which imports here.
 *
 * Features:
 *   - Base URL from environment config
 *   - Request timeout
 *   - Request interceptor: attaches CSRF-safe headers
 *   - Response interceptor: normalizes errors into ApiError shape
 *   - Generic error messages surfaced to users (no raw backend detail)
 *
 * Security notes:
 *   - Auth tokens are handled by HttpOnly cookies set by the backend.
 *     This client does NOT read or write tokens from localStorage.
 *     (TODO(security): When backend is live, confirm cookie flags:
 *      HttpOnly, Secure, SameSite=Lax.)
 *   - withCredentials: true ensures cookies are sent cross-origin.
 *   - HTTPS enforcement is a deployment concern. In development the
 *     API URL uses http://127.0.0.1 which is loopback-only.
 */

import axios from 'axios';
import env from '../config/env.js';

// ---------------------------------------------------------------------------
// ApiError — normalized error shape for the UI layer
// ---------------------------------------------------------------------------

export class ApiError extends Error {
  /**
   * @param {string} message — user-friendly generic message
   * @param {number} status  — HTTP status code (0 = network/timeout)
   * @param {string} code    — machine-readable error code
   */
  constructor(message, status = 0, code = 'UNKNOWN_ERROR') {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }
}

// ---------------------------------------------------------------------------
// Axios Instance
// ---------------------------------------------------------------------------

const apiClient = axios.create({
  baseURL: env.API_URL,
  timeout: env.API_TIMEOUT_MS,
  withCredentials: true,        // Send HttpOnly auth cookies automatically
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest', // CSRF defence-in-depth header
  },
});

// ---------------------------------------------------------------------------
// Request Interceptor
// ---------------------------------------------------------------------------

apiClient.interceptors.request.use(
  (config) => {
    // Logging is intentionally minimal — avoid logging sensitive request data.
    if (env.IS_DEV) {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => Promise.reject(new ApiError('Failed to send request.', 0, 'REQUEST_SETUP_ERROR'))
);

// ---------------------------------------------------------------------------
// Response Interceptor — normalize errors
// ---------------------------------------------------------------------------

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isCancel(error)) {
      return Promise.reject(new ApiError('Request was cancelled.', 0, 'CANCELLED'));
    }

    if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
      return Promise.reject(
        new ApiError(
          'The request timed out. Please check your connection and try again.',
          0,
          'TIMEOUT'
        )
      );
    }

    if (!error.response) {
      return Promise.reject(
        new ApiError(
          'Unable to reach the server. Please check your internet connection.',
          0,
          'NETWORK_ERROR'
        )
      );
    }

    const { status } = error.response;

    // Map HTTP status codes to friendly messages. Do NOT surface raw backend
    // error details to the user — log them for developers only.
    const statusMessages = {
      400: 'The request was invalid. Please check your input.',
      401: 'You are not authenticated. Please sign in.',
      403: 'You do not have permission to perform this action.',
      404: 'The requested resource was not found.',
      409: 'A conflict occurred. The resource may already exist.',
      413: 'The file is too large to upload.',
      422: 'The submitted data could not be processed.',
      429: 'Too many requests. Please wait a moment and try again.',
      500: 'A server error occurred. Please try again later.',
      502: 'The server is temporarily unavailable.',
      503: 'The service is under maintenance. Please try again soon.',
    };

    const message = statusMessages[status] ?? `An unexpected error occurred (${status}).`;

    if (env.IS_DEV) {
      // Only log full error detail in development
      console.error('[API Error]', status, error.response?.data);
    }

    return Promise.reject(new ApiError(message, status, `HTTP_${status}`));
  }
);

export default apiClient;
