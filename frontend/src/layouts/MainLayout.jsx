import React, { useState } from 'react';
import Sidebar from '../components/Sidebar.jsx';
import Navbar from '../components/Navbar.jsx';
import ToastContainer from '../components/ui/ToastContainer.jsx';

/**
 * MainLayout — Primary application shell
 *
 * Renders the sidebar, navbar, and content area.
 * All authenticated pages render as children within this layout.
 */
export default function MainLayout({ children }) {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  return (
    <div className="app-container">
      <Sidebar
        mobileOpen={mobileSidebarOpen}
        onCloseMobile={() => setMobileSidebarOpen(false)}
      />
      <main className="main-canvas">
        <Navbar
          onToggleMobileSidebar={() => setMobileSidebarOpen(!mobileSidebarOpen)}
        />
        <div className="canvas-content">
          {children}
        </div>
      </main>
      <ToastContainer />
    </div>
  );
}
