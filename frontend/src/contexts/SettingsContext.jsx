import React, { createContext, useContext, useState } from 'react';

/**
 * SettingsContext — Application Settings State
 *
 * Stores user preferences like notifications enabled, language, etc.
 * Non-sensitive data only. Persisted in localStorage.
 */

const SettingsContext = createContext(null);

const SETTINGS_KEY = 'ai_notes_settings';

const DEFAULT_SETTINGS = {
  notificationsEnabled: true,
  autoDismissToasts: true,
  compactView: false,
  language: 'en',
  defaultCategory: 'Planning',
};

function loadSettings() {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY);
    if (raw) return { ...DEFAULT_SETTINGS, ...JSON.parse(raw) };
  } catch {
    // Silently fall back to defaults
  }
  return DEFAULT_SETTINGS;
}

export function SettingsProvider({ children }) {
  const [settings, setSettings] = useState(loadSettings);

  const updateSetting = (key, value) => {
    setSettings((prev) => {
      const next = { ...prev, [key]: value };
      try {
        localStorage.setItem(SETTINGS_KEY, JSON.stringify(next));
      } catch {
        // Silently ignore storage errors
      }
      return next;
    });
  };

  const resetSettings = () => {
    setSettings(DEFAULT_SETTINGS);
    try {
      localStorage.removeItem(SETTINGS_KEY);
    } catch { }
  };

  return (
    <SettingsContext.Provider value={{ settings, updateSetting, resetSettings }}>
      {children}
    </SettingsContext.Provider>
  );
}

export function useSettingsContext() {
  const ctx = useContext(SettingsContext);
  if (!ctx) throw new Error('useSettingsContext must be used within SettingsProvider');
  return ctx;
}
