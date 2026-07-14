/**
 * dashboardService.js — Dashboard Stats API Service
 *
 * Fetches aggregated statistics for the dashboard view.
 */

import apiClient from '../api/apiClient.js';
import env from '../config/env.js';

const MOCK_DELAY = (ms = 600) => new Promise((res) => setTimeout(res, ms));

/**
 * Fetch dashboard statistics.
 * In mock mode these are computed client-side from meetings data.
 * When live, the backend returns pre-computed aggregates.
 *
 * @param {Array} meetings — current meetings array (used in mock mode)
 * @returns {Promise<Object>}
 */
export async function fetchDashboardStats(meetings = []) {
  if (env.AI_PROVIDER === 'mock') {
    await MOCK_DELAY();
    const allActions = meetings.flatMap((m) => m.actionItems ?? []);
    const pending = allActions.filter((a) => a.status === 'Pending').length;
    const completed = allActions.filter((a) => a.status === 'Completed').length;
    const rate = allActions.length > 0 ? Math.round((completed / allActions.length) * 100) : 0;

    return {
      timeSaved: meetings.length * 2.5,
      totalMeetings: meetings.length,
      pendingActions: pending,
      completedActions: completed,
      completionRate: rate,
      aiUptime: 99.9,
    };
  }

  const { data } = await apiClient.get('/dashboard/stats');
  return data;
}
