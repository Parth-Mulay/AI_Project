import React, { createContext, useContext, useState, useCallback } from 'react';
import { MAX_NOTIFICATIONS } from '../config/constants.js';

/**
 * NotificationsContext — Toast Notifications State
 *
 * Provides addNotification, removeNotification, clearAll.
 * Consumed by the useNotifications hook.
 *
 * Security: Notification text is rendered as React text nodes (auto-escaped).
 * No HTML is injected. Never include sensitive data in notification messages.
 */

const NotificationsContext = createContext(null);

let _nextId = 1;

export function NotificationsProvider({ children }) {
  const [notifications, setNotifications] = useState([]);

  const addNotification = useCallback((text, type = 'info', duration = 4000) => {
    const id = _nextId++;
    setNotifications((prev) => [
      { id, text, type, duration, timestamp: Date.now() },
      ...prev.slice(0, MAX_NOTIFICATIONS - 1),
    ]);
    if (duration > 0) {
      setTimeout(() => removeNotification(id), duration);
    }
    return id;
  }, []);

  const removeNotification = useCallback((id) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  }, []);

  const clearAll = useCallback(() => setNotifications([]), []);

  return (
    <NotificationsContext.Provider value={{ notifications, addNotification, removeNotification, clearAll }}>
      {children}
    </NotificationsContext.Provider>
  );
}

export function useNotificationsContext() {
  const ctx = useContext(NotificationsContext);
  if (!ctx) throw new Error('useNotificationsContext must be used within NotificationsProvider');
  return ctx;
}
