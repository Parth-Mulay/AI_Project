import React, { useState } from 'react';
import SearchBar from './SearchBar';

export default function Navbar({
  searchQuery,
  onSearchChange,
  userRole = 'Member',
  onToggleRole = () => {},
  onToggleMobileSidebar = () => {},
  notifications = []
}) {
  const [drawerOpen, setDrawerOpen] = useState(false);

  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  };

  return (
    <header className="top-bar">
      {/* Mobile Hamburger toggle */}
      <button 
        className="hamburger-btn" 
        onClick={onToggleMobileSidebar}
        aria-label="Toggle Navigation Drawer"
      >
        <span className="material-symbols-outlined">menu</span>
      </button>

      <SearchBar searchQuery={searchQuery} onSearchChange={onSearchChange} />

      <div className="top-bar-actions">
        {/* Role Toggle Switcher */}
        <button className="top-btn role-toggle-btn" onClick={onToggleRole}>
          Active Role: <strong>{userRole.toUpperCase()}</strong>
        </button>

        {/* Notification Bell */}
        <button 
          className="top-btn" 
          onClick={toggleDrawer}
          aria-label="Notifications Drawer"
          aria-expanded={drawerOpen}
        >
          <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>
            notifications
          </span>
          {notifications.length > 0 && <span className="notification-dot"></span>}
        </button>

        {/* Notification Drawer (Slide-down dropdown overlay) */}
        {drawerOpen && (
          <div className="notification-drawer" role="dialog" aria-label="Notifications Panel">
            <div className="drawer-header">
              <h3>Notifications</h3>
              <button onClick={toggleDrawer} className="close-btn" aria-label="Close Notifications">
                &times;
              </button>
            </div>
            <div className="drawer-content">
              {notifications.length > 0 ? (
                notifications.map((noti, idx) => (
                  <div key={idx} className="noti-item">
                    <p>{noti.text}</p>
                    <span className="noti-time">{noti.time}</span>
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
