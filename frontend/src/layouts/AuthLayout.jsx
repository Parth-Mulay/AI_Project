import React from 'react';
import env from '../config/env.js';

/**
 * AuthLayout — Centered card layout for future auth pages (login, signup)
 *
 * Currently a placeholder. Will be used when OAuth integration is added.
 * TODO(security): Add CSRF token handling when auth forms are implemented.
 */
export default function AuthLayout({ children }) {
  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'var(--color-bg-base)',
        padding: '32px',
      }}
    >
      <div style={{ textAlign: 'center', marginBottom: '32px' }}>
        <span className="material-symbols-outlined" style={{ fontSize: '40px', color: 'var(--color-accent-purple)' }}>
          smart_toy
        </span>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: 'var(--color-text-primary)', marginTop: '8px' }}>
          {env.APP_NAME}
        </h1>
      </div>
      <div
        style={{
          background: 'var(--color-surface-glass)',
          border: '1.5px solid var(--color-border-glass)',
          borderRadius: 'var(--radius-lg)',
          padding: '40px',
          width: '100%',
          maxWidth: '420px',
          backdropFilter: 'blur(12px)',
        }}
      >
        {children}
      </div>
    </div>
  );
}
