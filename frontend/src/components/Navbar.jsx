import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ROUTES } from '../config/constants.js';
import { useAuthContext } from '../contexts/AuthContext.jsx';
import { useNotificationsContext } from '../contexts/NotificationsContext.jsx';
import SearchBar from './SearchBar.jsx';

/**
 * Navbar — Top Application Bar (updated for React Router)
 *
 * Uses useNavigate for search submission.
 * Consumes AuthContext for role and NotificationsContext for bell badge.
 * Props: onToggleMobileSidebar
 */
export default function Navbar({ onToggleMobileSidebar = () => {} }) {
  const navigate = useNavigate();
  const { userRole, setUserRole } = useAuthContext();
  const { notifications } = useNotificationsContext();
  const [searchQuery, setSearchQuery] = useState('');
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleSearch = (query) => {
    setSearchQuery(query);
    if (query.trim()) {
      navigate(`${ROUTES.SEARCH}?q=${encodeURIComponent(query.trim())}`);
    }
  };

  const handleToggleRole = () => {
    const newRole = userRole === 'Member' ? 'Admin' : 'Member';
    setUserRole(newRole);
  };

  return (
    <header className="top-bar">
      {/* Mobile hamburger */}
      <button
        className="hamburger-btn"
        onClick={onToggleMobileSidebar}
        aria-label="Toggle Navigation Drawer"
      >
        <span className="material-symbols-outlined">menu</span>
      </button>

      <SearchBar
        searchQuery={searchQuery}
        onSearchChange={handleSearch}
      />

      <div className="top-bar-actions">
        {/* Role Toggle */}
        <button className="top-btn role-toggle-btn" onClick={handleToggleRole}>
          Active Role: <strong>{userRole.toUpperCase()}</strong>
        </button>

        {/* Notification Bell */}
        <button
          className="top-btn"
          onClick={() => setDrawerOpen(!drawerOpen)}
          aria-label="Notifications Drawer"
          aria-expanded={drawerOpen}
        >
          <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>
            notifications
          </span>
          {notifications.length > 0 && <span className="notification-dot" />}
        </button>

        {/* Notification Drawer */}
        {drawerOpen && (
          <div className="notification-drawer" role="dialog" aria-label="Notifications Panel">
            <div className="drawer-header">
              <h3>Notifications</h3>
              <button onClick={() => setDrawerOpen(false)} className="close-btn" aria-label="Close Notifications">
                &times;
              </button>
            </div>
            <div className="drawer-content">
              {notifications.length > 0 ? (
                notifications.map((noti) => (
                  <div key={noti.id} className="noti-item">
                    <p>{noti.text}</p>
                    <span className="noti-time">Just now</span>
                  </div>
                ))
              ) : (
                <p className="empty-noti">No new notifications.</p>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
