/**
 * userService.js — User Profile & Auth API Service
 *
 * Handles authentication status and user profile.
 *
 * Security:
 *   - Auth tokens are managed server-side via HttpOnly cookies.
 *   - This service reads non-sensitive profile metadata only.
 *   - TODO(security): Implement OAuth 2.0 / OpenID Connect login flow.
 *   - TODO(security): Add MFA support.
 */

import apiClient from '../api/apiClient.js';
import env from '../config/env.js';

const MOCK_DELAY = (ms = 400) => new Promise((res) => setTimeout(res, ms));

/** Mock user matching the seed data in previous days */
const MOCK_USER = {
  id: 'usr_priya_001',
  name: 'Priya',
  email: 'priya@example.com',
  role: 'Member',
  avatarInitial: 'P',
  plan: 'Pro',
  storageUsedGb: 24.5,
  storageLimitGb: 100,
  createdAt: '2026-01-01T00:00:00Z',
};

/**
 * Fetch the currently authenticated user's profile.
 * @returns {Promise<Object>} — user object
 */
export async function fetchCurrentUser() {
  if (env.AI_PROVIDER === 'mock') {
    await MOCK_DELAY();
    return { ...MOCK_USER };
  }
  const { data } = await apiClient.get('/users/me');
  return data;
}

/**
 * Update the current user's role (admin action — mock only).
 * @param {string} role — 'Member' | 'Admin'
 * @returns {Promise<Object>} — updated user object
 */
export async function updateUserRole(role) {
  if (env.AI_PROVIDER === 'mock') {
    await MOCK_DELAY(200);
    return { ...MOCK_USER, role };
  }
  const { data } = await apiClient.patch('/users/me/role', { role });
  return data;
}

/**
 * Log out the current user.
 * Clears server-side session. Frontend clears context state.
 * @returns {Promise<void>}
 */
export async function logout() {
  if (env.AI_PROVIDER === 'mock') {
    await MOCK_DELAY(200);
    return;
  }
  await apiClient.post('/auth/logout');
}
