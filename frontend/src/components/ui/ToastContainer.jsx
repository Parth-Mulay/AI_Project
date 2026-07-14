import React from 'react';
import { createPortal } from 'react-dom';
import Toast from './Toast.jsx';
import { useNotificationsContext } from '../../contexts/NotificationsContext.jsx';

/**
 * ToastContainer — Renders all active toasts via a React Portal
 *
 * Mounted once inside MainLayout. Portals into document.body so toasts
 * float above all other content without z-index conflicts.
 */
export default function ToastContainer() {
  const { notifications, removeNotification } = useNotificationsContext();

  if (notifications.length === 0) return null;

  return createPortal(
    <div className="toast-container" aria-live="polite" aria-label="Notifications">
      {notifications.map((n) => (
        <Toast key={n.id} notification={n} onDismiss={removeNotification} />
      ))}
    </div>,
    document.body
  );
}
