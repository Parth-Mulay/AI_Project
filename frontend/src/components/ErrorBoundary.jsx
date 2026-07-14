import React from 'react';

/**
 * ErrorBoundary — Catches unhandled React render errors
 *
 * Must be a class component (React requirement for componentDidCatch).
 * Wraps the entire app to prevent white-screen crashes.
 *
 * Security: error.stack is NOT shown to the user — only a generic message.
 * Detailed errors are logged to console (dev only) for debugging.
 */
export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, errorId: null };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    // Log only in development — do NOT expose stack traces to users
    if (import.meta.env.DEV) {
      console.error('[ErrorBoundary] Unhandled render error:', error);
      console.error('[ErrorBoundary] Component stack:', info.componentStack);
    }
    // TODO(security): In production, send error.message (no stack) to an
    // error monitoring service (e.g. Sentry) with PII stripped.
  }

  handleReset = () => {
    this.setState({ hasError: false });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '16px',
            background: 'var(--color-bg-base)',
            color: 'var(--color-text-primary)',
            padding: '32px',
            textAlign: 'center',
          }}
          role="alert"
        >
          <span
            className="material-symbols-outlined"
            style={{ fontSize: '64px', color: 'var(--color-accent-pink)' }}
          >
            error
          </span>
          <h1 style={{ fontSize: '22px', fontWeight: 700, margin: 0 }}>
            Unexpected Application Error
          </h1>
          <p style={{ color: 'var(--color-text-secondary)', maxWidth: '400px', margin: 0 }}>
            Something went wrong while rendering this view. Your data is safe.
            Please try refreshing the page.
          </p>
          <div style={{ display: 'flex', gap: '12px', marginTop: '8px' }}>
            <button
              className="btn btn-primary"
              onClick={() => window.location.reload()}
            >
              Refresh Page
            </button>
            <button className="btn btn-secondary" onClick={this.handleReset}>
              Try Recovery
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
