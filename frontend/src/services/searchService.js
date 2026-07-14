/**
 * searchService.js — Search API Service
 *
 * Full-text search across the user's meeting archive.
 */

import apiClient from '../api/apiClient.js';
import env from '../config/env.js';

const MOCK_DELAY = (ms = 500) => new Promise((res) => setTimeout(res, ms));

/**
 * Search meetings by query string.
 * In mock mode, client-side filters the provided meetings array.
 *
 * @param {string} query — user search input
 * @param {Array} meetings — local meetings array (mock mode only)
 * @returns {Promise<Array>} — filtered/ranked meeting results
 */
export async function searchMeetings(query, meetings = []) {
  if (!query || !query.trim()) return [];

  if (env.AI_PROVIDER === 'mock') {
    await MOCK_DELAY();
    const q = query.toLowerCase().trim();
    return meetings.filter((m) =>
      m.title.toLowerCase().includes(q) ||
      (m.tags ?? []).some((t) => t.toLowerCase().includes(q)) ||
      (m.participants ?? []).some((p) => p.toLowerCase().includes(q)) ||
      (m.summary ?? '').toLowerCase().includes(q)
    );
  }

  const { data } = await apiClient.get('/search', {
    params: { q: query, limit: 50 },
  });
  return data;
}
