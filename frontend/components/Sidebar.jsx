import React from 'react';

export default function Sidebar({
  currentPage,
  onPageChange,
  userRole = 'Member',
  mobileOpen = false,
  onCloseMobile = () => {}
}) {
  const handleNavClick = (page) => {
    onPageChange(page);
    onCloseMobile(); // Closes menu on mobile when a link is clicked
  };

  return (
    <aside className={`sidebar ${mobileOpen ? 'mobile-open' : ''}`}>
      <div className="sidebar-top-group">
        <div className="sidebar-brand">
          <span className="ai-sparkle">
            <span className="material-symbols-outlined" style={{ fontSize: '24px', color: 'var(--color-accent-purple)' }}>
              smart_toy
            </span>
          </span>
          <h1>AI NOTES</h1>
        </div>

        <nav className="sidebar-nav">
          <button
            onClick={() => handleNavClick('dashboard')}
            className={`nav-item ${currentPage === 'dashboard' ? 'active' : ''}`}
          >
            <span className="material-symbols-outlined nav-icon">grid_view</span>
            <span>Dashboard</span>
          </button>

          <button
            onClick={() => handleNavClick('upload')}
            className={`nav-item ${currentPage === 'upload' ? 'active' : ''}`}
          >
            <span className="material-symbols-outlined nav-icon">cloud_upload</span>
            <span>Upload File</span>
          </button>

          {/* Seed/Mock placeholders exactly matching Figma */}
          <button className="nav-item" disabled style={{ opacity: 0.5, cursor: 'not-allowed' }}>
            <span className="material-symbols-outlined nav-icon">mic</span>
            <span>Live Capture</span>
          </button>
          
          <button className="nav-item" disabled style={{ opacity: 0.5, cursor: 'not-allowed' }}>
            <span className="material-symbols-outlined nav-icon">folder_open</span>
            <span>Meetings Archive</span>
          </button>

          <button className="nav-item" disabled style={{ opacity: 0.5, cursor: 'not-allowed' }}>
            <span className="material-symbols-outlined nav-icon">group</span>
            <span>Workspace Directory</span>
          </button>

          <button className="nav-item" disabled style={{ opacity: 0.5, cursor: 'not-allowed' }}>
            <span className="material-symbols-outlined nav-icon">auto_awesome</span>
            <span>AI Assistant</span>
            <span className="nav-new-chip">New</span>
          </button>

          <button className="nav-item" disabled style={{ opacity: 0.5, cursor: 'not-allowed' }}>
            <span className="material-symbols-outlined nav-icon">monitoring</span>
            <span>Analytics</span>
          </button>

          <button className="nav-item" disabled style={{ opacity: 0.5, cursor: 'not-allowed' }}>
            <span className="material-symbols-outlined nav-icon">settings</span>
            <span>System Settings</span>
          </button>
        </nav>
      </div>

      <div className="sidebar-bottom-group">
        {/* Storage status meter */}
        <div className="sidebar-storage-card">
          <div className="storage-meta">
            <span className="storage-title">Storage Used</span>
            <span className="storage-percent">24%</span>
          </div>
          <div className="storage-numbers">24.5 GB / 100 GB</div>
          <div className="storage-bar">
            <div className="storage-progress" style={{ width: '24.5%' }}></div>
          </div>
          <button className="btn btn-secondary btn-full btn-small" style={{ fontSize: '10px', padding: '6px' }}>
            Upgrade Plan
          </button>
        </div>

        {/* User profile tags */}
        <div className="sidebar-user">
          <div className="user-avatar">P</div>
          <div className="user-details">
            <span className="user-name">Priya</span>
            <span className="user-role-badge">{userRole}</span>
          </div>
          <span className="user-dropdown-arrow">▼</span>
        </div>
      </div>
    </aside>
  );
}
