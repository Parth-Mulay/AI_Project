import React from 'react';
import { NotificationsProvider } from './NotificationsContext.jsx';
import { AuthProvider } from './AuthContext.jsx';
import { MeetingsProvider } from './MeetingsContext.jsx';
import { ThemeProvider } from './ThemeContext.jsx';
import { SettingsProvider } from './SettingsContext.jsx';

/**
 * AppProviders — Combines All Context Providers
 *
 * Provider order matters:
 *  1. ThemeProvider     — no dependencies
 *  2. SettingsProvider  — no dependencies
 *  3. NotificationsProvider — no dependencies
 *  4. AuthProvider      — depends on NotificationsProvider (for error notifications)
 *  5. MeetingsProvider  — depends on NotificationsProvider + AuthProvider
 *
 * Wrap the entire application once in main.jsx.
 */
export default function AppProviders({ children }) {
  return (
    <ThemeProvider>
      <SettingsProvider>
        <NotificationsProvider>
          <AuthProvider>
            <MeetingsProvider>
              {children}
            </MeetingsProvider>
          </AuthProvider>
        </NotificationsProvider>
      </SettingsProvider>
    </ThemeProvider>
  );
}
