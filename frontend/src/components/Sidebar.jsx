import React from 'react';
import { NavLink } from 'react-router-dom';
import { ROUTES } from '../config/constants.js';
import { useAuthContext } from '../contexts/AuthContext.jsx';
import ToastContainer from './ui/ToastContainer.jsx';

/**
 * Sidebar — Main Navigation (updated for React Router v6)
 *
 * Replaced onPageChange callbacks with NavLink components.
 * Active state is handled by React Router's NavLink isActive prop.
 *
 * Props:
 *   mobileOpen    — boolean
 *   onCloseMobile — callback
 */
export default function Sidebar({ mobileOpen = false, onCloseMobile = () => {} }) {
  const { userRole } = useAuthContext();

  const handleNavClick = () => {
    onCloseMobile();
  };

  const navLinkClass = ({ isActive }) =>
    `nav-item${isActive ? ' active' : ''}`;

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

        <nav className="sidebar-nav" aria-label="Primary Navigation">
          <NavLink to={ROUTES.HOME} end className={navLinkClass} onClick={handleNavClick}>
            <span className="material-symbols-outlined nav-icon">grid_view</span>
            <span>Dashboard</span>
          </NavLink>

          <NavLink to={ROUTES.UPLOAD} className={navLinkClass} onClick={handleNavClick}>
            <span className="material-symbols-outlined nav-icon">cloud_upload</span>
            <span>Upload File</span>
          </NavLink>

          <NavLink to={ROUTES.MEETINGS} className={navLinkClass} onClick={handleNavClick}>
            <span className="material-symbols-outlined nav-icon">folder_open</span>
            <span>Meetings Archive</span>
          </NavLink>

          <NavLink to={ROUTES.SEARCH} className={navLinkClass} onClick={handleNavClick}>
            <span className="material-symbols-outlined nav-icon">search</span>
            <span>Search</span>
          </NavLink>

          <NavLink to={ROUTES.LIVE_CAPTURE} className={navLinkClass} onClick={handleNavClick}>
            <span className="material-symbols-outlined nav-icon">mic</span>
            <span>Live Capture</span>
            <span className="nav-new-chip">Beta</span>
          </NavLink>

          <NavLink to={ROUTES.WORKSPACE} className={navLinkClass} onClick={handleNavClick}>
            <span className="material-symbols-outlined nav-icon">group</span>
            <span>Workspace</span>
          </NavLink>

          <NavLink to={ROUTES.SETTINGS} className={navLinkClass} onClick={handleNavClick}>
            <span className="material-symbols-outlined nav-icon">settings</span>
            <span>Settings</span>
          </NavLink>
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

        {/* User profile tag */}
        <NavLink to={ROUTES.PROFILE} className="sidebar-user" onClick={handleNavClick} style={{ textDecoration: 'none' }}>
          <div className="user-avatar">P</div>
          <div className="user-details">
            <span className="user-name">Priya</span>
            <span className="user-role-badge">{userRole}</span>
          </div>
          <span className="user-dropdown-arrow">▼</span>
        </NavLink>
      </div>
    </aside>
  );
}
