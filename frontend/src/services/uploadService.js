/**
 * uploadService.js — File Upload API Service
 *
 * Handles multipart/form-data file upload to the AI processing pipeline.
 * The service is designed to work with the existing UploadMeeting form.
 *
 * Security:
 *   - Client validates extension + size before calling this service.
 *   - TODO(security): Backend MUST validate magic bytes, re-check size,
 *     rename file to UUID, store outside web root, and scan for malware.
 */

import apiClient from '../api/apiClient.js';
import env from '../config/env.js';

const MOCK_DELAY = (ms = 1000) => new Promise((res) => setTimeout(res, ms));

/**
 * Upload a meeting file and metadata for AI processing.
 *
 * @param {Object} formData — { title, datetime, duration, category, participants, file }
 * @param {Function} onProgress — optional progress callback (0–100)
 * @returns {Promise<Object>} — processed meeting object
 */
export async function uploadMeeting(formData, onProgress) {
  if (env.AI_PROVIDER === 'mock') {
    // Simulate a 6-stage pipeline with progress updates
    for (let i = 1; i <= 6; i++) {
      await MOCK_DELAY(900);
      onProgress?.(Math.round((i / 6) * 100));
    }

    const participantsArray = formData.participants
      .split(',')
      .map((p) => p.trim())
      .filter(Boolean);

    return {
      id: String(Date.now()),
      title: formData.title,
      date: formData.datetime.split('T')[0],
      time: new Date(formData.datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      duration: `${formData.duration} minutes`,
      participants: participantsArray,
      tags: [formData.category.toLowerCase()],
      status: 'Analyzed',
      summary: `## Executive Summary\nAll departments aligned key plans under the ${formData.category} agenda.\n\n## Key Discussion Points\n- Detailed discussion of ${formData.title}.\n\n## Risks\n- Staffing schedules require alignment.`,
      actionItems: [
        { task: `Verify action items for ${formData.title}`, owner: participantsArray[0] ?? 'Priya', deadline: 'Jul 20', priority: 'High', status: 'Pending' },
        { task: 'Review pipeline output data', owner: participantsArray[1] ?? 'Rahul', deadline: 'Jul 25', priority: 'Medium', status: 'Pending' },
      ],
      decisions: [
        `Approved roadmap for ${formData.category}.`,
        'Decided on database layout optimizations.',
      ],
    };
  }

  // Real multipart upload
  const payload = new FormData();
  payload.append('file', formData.file);
  payload.append('title', formData.title);
  payload.append('datetime', formData.datetime);
  payload.append('duration', String(formData.duration));
  payload.append('category', formData.category);
  payload.append('participants', formData.participants);

  const { data } = await apiClient.post('/upload', payload, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (event) => {
      if (event.total) {
        onProgress?.(Math.round((event.loaded / event.total) * 100));
      }
    },
  });
  return data;
}
