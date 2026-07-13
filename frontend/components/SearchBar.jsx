import React, { useEffect, useRef } from 'react';

export default function SearchBar({ searchQuery, onSearchChange }) {
  const inputRef = useRef(null);

  useEffect(() => {
    const handleKeyDown = (e) => {
      // Intercepts Ctrl+K or Cmd+K to focus search input
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="search-container">
      <span className="search-icon">
        <span className="material-symbols-outlined">search</span>
      </span>
      <input
        ref={inputRef}
        type="text"
        value={searchQuery}
        onChange={(e) => onSearchChange(e.target.value)}
        placeholder="Search meetings, tags, participants... (Ctrl+K)"
        aria-label="Global Workspace Search"
      />
      <span className="search-hint">⌘ K</span>
    </div>
  );
}
