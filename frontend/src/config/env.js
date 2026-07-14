/**
 * env.js — Centralized Environment Configuration Accessor
 *
 * All import.meta.env access is funnelled through this module.
 * Components and services import from here rather than referencing
 * import.meta.env directly, making it easy to mock in tests and
 * change variable names in one place.
 *
 * Security note: Only VITE_-prefixed variables are included in the
 * client bundle by Vite. Never place JWT secrets, DB credentials, or
 * private API keys in VITE_ variables.
 */

const env = {
  /** Public app display name */
  APP_NAME: import.meta.env.VITE_APP_NAME ?? 'AI Meeting Notes Manager',

  /** SemVer string */
  APP_VERSION: import.meta.env.VITE_APP_VERSION ?? '1.0.0',

  /** Backend API base URL — no trailing slash */
  API_URL: import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000/api/v1',

  /** Axios request timeout in milliseconds */
  API_TIMEOUT_MS: Number(import.meta.env.VITE_API_TIMEOUT_MS ?? 15000),

  /** Max document upload size in bytes */
  UPLOAD_LIMIT_DOCS_BYTES: Number(import.meta.env.VITE_UPLOAD_LIMIT_DOCS_MB ?? 10) * 1024 * 1024,

  /** Max audio upload size in bytes */
  UPLOAD_LIMIT_AUDIO_BYTES: Number(import.meta.env.VITE_UPLOAD_LIMIT_AUDIO_MB ?? 100) * 1024 * 1024,

  /** Max document size in MB (for display) */
  UPLOAD_LIMIT_DOCS_MB: Number(import.meta.env.VITE_UPLOAD_LIMIT_DOCS_MB ?? 10),

  /** Max audio size in MB (for display) */
  UPLOAD_LIMIT_AUDIO_MB: Number(import.meta.env.VITE_UPLOAD_LIMIT_AUDIO_MB ?? 100),

  /** AI provider identifier */
  AI_PROVIDER: import.meta.env.VITE_AI_PROVIDER ?? 'mock',

  /** Feature flags */
  FEATURE_LIVE_CAPTURE: import.meta.env.VITE_FEATURE_LIVE_CAPTURE === 'true',
  FEATURE_ANALYTICS: import.meta.env.VITE_FEATURE_ANALYTICS === 'true',
  FEATURE_WORKSPACE: import.meta.env.VITE_FEATURE_WORKSPACE === 'true',

  /** True when running in development mode */
  IS_DEV: import.meta.env.DEV === true,

  /** True when running the production build */
  IS_PROD: import.meta.env.PROD === true,
};

export default env;
