/**
 * sanitize.js — Safe Text Rendering Helpers
 *
 * React's JSX auto-escapes all text content in {} expressions,
 * which covers the vast majority of XSS vectors. This module
 * documents best practices and provides helpers for the few
 * edge cases where additional care is needed.
 *
 * Security guidelines enforced:
 *   - MUST NOT use dangerouslySetInnerHTML without DOMPurify.
 *   - MUST NOT use innerHTML assignments in vanilla JS.
 *   - Use textContent / createElement for any DOM manipulation.
 *
 * TODO(security): If rich-text editor output ever needs to be rendered
 *   as HTML, install DOMPurify and use sanitizeHtml() below.
 */

// ---------------------------------------------------------------------------
// Safe Text Helpers
// ---------------------------------------------------------------------------

/**
 * Strip all HTML tags from a string, returning plain text.
 * Suitable for display in UI labels where HTML is unexpected.
 *
 * @param {string} str — potentially unsafe string
 * @returns {string} — plain text, safe for React text nodes
 */
export function stripTags(str) {
  if (!str || typeof str !== 'string') return '';
  // Replace tags with a space to avoid word merging
  return str.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
}

/**
 * Truncate and strip tags for safe preview snippets.
 * @param {string} str
 * @param {number} max
 * @returns {string}
 */
export function safePreview(str, max = 200) {
  return stripTags(str).slice(0, max);
}

/**
 * Validate that a string does not contain script injection patterns.
 * Returns true if the string is considered safe for further processing.
 * Note: This is a defence-in-depth check. React JSX rendering is the
 * primary XSS defence.
 *
 * @param {string} str
 * @returns {boolean}
 */
export function isSafeString(str) {
  if (!str || typeof str !== 'string') return true;
  const dangerousPatterns = [
    /<script/i,
    /javascript:/i,
    /on\w+\s*=/i,        // event handlers like onclick=
    /data:text\/html/i,
  ];
  return !dangerousPatterns.some((pattern) => pattern.test(str));
}
