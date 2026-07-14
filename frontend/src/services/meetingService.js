/**
 * meetingService.js — Meeting API Service
 *
 * All meeting-related API calls. Components never call apiClient directly;
 * they use this service module and its typed return values.
 *
 * When the FastAPI backend is live, replace the MOCK_DELAY blocks with
 * the real apiClient calls (already written below each mock section).
 */

import apiClient from '../api/apiClient.js';
import env from '../config/env.js';

// ---------------------------------------------------------------------------
// Mock helpers (used when VITE_AI_PROVIDER=mock)
// ---------------------------------------------------------------------------

const MOCK_DELAY = (ms = 800) => new Promise((res) => setTimeout(res, ms));

/** Seed meetings matching the existing App.jsx state */
const MOCK_MEETINGS = [
  {
    id: '1',
    title: 'Government Planning Sync - 2027 Agenda',
    date: '2026-07-13',
    time: '10:00 AM',
    duration: '45 minutes',
    participants: ['Sharma', 'Iyer', 'Khan', 'Deshmukh', 'Patel'],
    tags: ['planning'],
    status: 'Analyzed',
    summary: `## Executive Summary\nAll departments aligned key projects under the technological growth agenda.\n\n## Key Discussion Points\n- Funding allocations for clean wind infrastructure.\n- Improving rural clinical healthcare capacities.\n\n## Risks\n- Rural clinical facility staffing gaps must be solved.`,
    actionItems: [
      { task: 'Task force will be formed to assess rural healthcare gaps within three months.', owner: 'Iyer', deadline: 'Oct 13', priority: 'Medium', status: 'Pending' },
      { task: 'A feasibility study on AI driven traffic management will be commissioned.', owner: 'Deshmukh', deadline: 'Dec 20', priority: 'Low', status: 'Pending' },
      { task: 'Ministries will submit integrated action plans by March 2027.', owner: 'Sharma', deadline: 'Mar 30', priority: 'Low', status: 'Pending' },
    ],
    decisions: [
      'Launch a pilot program in 10 districts integrating coding and AI basics into curricula.',
      'Introduce a subsidy scheme for drought resistant seeds.',
    ],
  },
  {
    id: '2',
    title: 'Marketing Alignment Call',
    date: '2026-07-10',
    time: '02:30 PM',
    duration: '20 minutes',
    participants: ['Brian', 'Priya'],
    tags: ['marketing'],
    status: 'Completed',
    summary: `## Executive Summary\nBrian raised a compliance concern regarding the deployment server's resource constraints.\n\n## Key Discussion Points\n- Server capability reviews.\n- Performance profiling checks.\n\n## Risks\n- Blocker: Deployment server has limited RAM allocation.`,
    actionItems: [
      { task: 'Priya will conduct a security review before launch.', owner: 'Priya', deadline: 'Jul 22', priority: 'High', status: 'Pending' },
    ],
    decisions: ['Agreed to hold release updates until performance profiles are signed off.'],
  },
  {
    id: '3',
    title: 'Sprint Planning - Week 14',
    date: '2026-07-06',
    time: '11:00 AM',
    duration: '30 minutes',
    participants: ['Rahul', 'Priya', 'Amit'],
    tags: ['planning'],
    status: 'Failed - Used Fallback',
    summary: `## Executive Summary\nRahul confirmed that the core authentication module is fully completed.\n\n## Key Discussion Points\n- Authentication modules development cycle complete.\n- Migration protocols and token setups.\n\n## Risks\n- Need to align schemas before staging deployments.`,
    actionItems: [
      { task: 'Rahul will review the database API schema tomorrow.', owner: 'Rahul', deadline: 'Jul 20', priority: 'High', status: 'Pending' },
      { task: 'Priya will deploy the cache layer by Friday.', owner: 'Priya', deadline: 'Jul 18', priority: 'High', status: 'Pending' },
    ],
    decisions: ['We decided to use JWT for token management.'],
  },
];

// ---------------------------------------------------------------------------
// Service Functions
// ---------------------------------------------------------------------------

/**
 * Fetch all meetings for the current workspace.
 * @returns {Promise<Array>} — array of meeting objects
 */
export async function fetchMeetings() {
  if (env.AI_PROVIDER === 'mock') {
    await MOCK_DELAY();
    return [...MOCK_MEETINGS];
  }
  const { data } = await apiClient.get('/meetings');
  return data;
}

/**
 * Fetch a single meeting by ID.
 * @param {string} id
 * @returns {Promise<Object>}
 */
export async function fetchMeetingById(id) {
  if (env.AI_PROVIDER === 'mock') {
    await MOCK_DELAY(400);
    const meeting = MOCK_MEETINGS.find((m) => m.id === id);
    if (!meeting) throw new Error('Meeting not found.');
    return { ...meeting };
  }
  const { data } = await apiClient.get(`/meetings/${id}`);
  return data;
}

/**
 * Delete a meeting by ID.
 * @param {string} id
 * @returns {Promise<void>}
 */
export async function deleteMeeting(id) {
  if (env.AI_PROVIDER === 'mock') {
    await MOCK_DELAY(300);
    return;
  }
  await apiClient.delete(`/meetings/${id}`);
}

/**
 * Update a specific action item's status within a meeting.
 * @param {string} meetingId
 * @param {number} itemIndex
 * @param {string} status — 'Pending' | 'Completed'
 * @returns {Promise<void>}
 */
export async function updateActionItemStatus(meetingId, itemIndex, status) {
  if (env.AI_PROVIDER === 'mock') {
    await MOCK_DELAY(200);
    return;
  }
  await apiClient.patch(`/meetings/${meetingId}/actions/${itemIndex}`, { status });
}
