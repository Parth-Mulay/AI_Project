import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { fetchMeetings, deleteMeeting, updateActionItemStatus } from '../services/meetingService.js';
import { useNotificationsContext } from './NotificationsContext.jsx';

/**
 * MeetingsContext — Meetings List State
 *
 * Centralizes all meeting data: fetch, add, delete, toggle actions.
 * Components receive data via useMeetings hook — no prop drilling.
 */

const MeetingsContext = createContext(null);

export function MeetingsProvider({ children }) {
  const [meetings, setMeetings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const { addNotification } = useNotificationsContext();

  const loadMeetings = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchMeetings();
      setMeetings(data);
    } catch (err) {
      setError(err.message ?? 'Failed to load meetings.');
      addNotification('Failed to load meetings. Please retry.', 'error');
    } finally {
      setIsLoading(false);
    }
  }, [addNotification]);

  useEffect(() => {
    loadMeetings();
  }, [loadMeetings]);

  const addMeeting = useCallback((meeting) => {
    setMeetings((prev) => [meeting, ...prev]);
    addNotification(`Processed meeting: "${meeting.title}"`, 'success');
  }, [addNotification]);

  const removeMeeting = useCallback(async (meetingId, userRole) => {
    if (userRole !== 'Admin') {
      addNotification('Action Denied: Administrator role required to delete meetings.', 'error');
      return;
    }
    const target = meetings.find((m) => m.id === meetingId);
    try {
      await deleteMeeting(meetingId);
      setMeetings((prev) => prev.filter((m) => m.id !== meetingId));
      addNotification(`Deleted meeting: "${target?.title ?? 'Unknown'}"`, 'info');
    } catch {
      addNotification('Failed to delete meeting. Please try again.', 'error');
    }
  }, [meetings, addNotification]);

  const toggleActionItem = useCallback(async (meetingId, itemIndex) => {
    setMeetings((prev) =>
      prev.map((meeting) => {
        if (meeting.id !== meetingId) return meeting;
        const updatedItems = meeting.actionItems.map((item, idx) => {
          if (idx !== itemIndex) return item;
          const newStatus = item.status === 'Completed' ? 'Pending' : 'Completed';
          addNotification(
            `Marked task "${item.task.slice(0, 30)}…" as ${newStatus}`,
            newStatus === 'Completed' ? 'success' : 'info'
          );
          return { ...item, status: newStatus };
        });
        return { ...meeting, actionItems: updatedItems };
      })
    );
    // Sync to backend (fire-and-forget in mock mode)
    const meeting = meetings.find((m) => m.id === meetingId);
    if (meeting) {
      const item = meeting.actionItems[itemIndex];
      const newStatus = item?.status === 'Completed' ? 'Pending' : 'Completed';
      try {
        await updateActionItemStatus(meetingId, itemIndex, newStatus);
      } catch {
        // Optimistic update already applied; log silently in dev
      }
    }
  }, [meetings, addNotification]);

  const addTestActionItem = useCallback(() => {
    if (meetings.length === 0) return;
    setMeetings((prev) => {
      const copy = [...prev];
      copy[0] = {
        ...copy[0],
        actionItems: [
          ...(copy[0].actionItems ?? []),
          { task: 'Verify WCAG 2.1 accessibility constraints', owner: 'Priya', deadline: 'ASAP', priority: 'High', status: 'Pending' },
        ],
      };
      return copy;
    });
    addNotification('Added new test action item.', 'info');
  }, [meetings, addNotification]);

  return (
    <MeetingsContext.Provider value={{
      meetings,
      isLoading,
      error,
      loadMeetings,
      addMeeting,
      removeMeeting,
      toggleActionItem,
      addTestActionItem,
    }}>
      {children}
    </MeetingsContext.Provider>
  );
}

export function useMeetingsContext() {
  const ctx = useContext(MeetingsContext);
  if (!ctx) throw new Error('useMeetingsContext must be used within MeetingsProvider');
  return ctx;
}
