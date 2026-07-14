import React, { createContext, useContext, useState, useEffect } from 'react';

/**
 * ThemeContext — Application Theme State
 *
 * Currently the design system uses a dark theme by default (per Figma).
 * This context is wired for future light/dark toggle support.
 * Theme preference is persisted in localStorage (non-sensitive data).
 */

const ThemeContext = createContext(null);

const THEME_KEY = 'ai_notes_theme';

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem(THEME_KEY) ?? 'dark';
    } catch {
      return 'dark';
    }
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem(THEME_KEY, theme);
    } catch {
      // Silently fail if localStorage is blocked (incognito, strict policies)
    }
  }, [theme]);

  const toggleTheme = () => setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, isDark: theme === 'dark' }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useThemeContext() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useThemeContext must be used within ThemeProvider');
  return ctx;
}
