import React from 'react';

/**
 * LoadingSpinner — Animated spinner for API loading states
 * Props: size ('sm' | 'md' | 'lg'), label (aria-label text)
 */
export default function LoadingSpinner({ size = 'md', label = 'Loading...' }) {
  const sizes = { sm: 20, md: 36, lg: 56 };
  const px = sizes[size] ?? sizes.md;

  return (
    <div
      className="loading-spinner-wrapper"
      role="status"
      aria-label={label}
      style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}
    >
      <svg
        width={px}
        height={px}
        viewBox="0 0 36 36"
        fill="none"
        style={{ animation: 'spin 0.9s linear infinite' }}
        aria-hidden="true"
      >
        <circle
          cx="18" cy="18" r="14"
          stroke="var(--color-border-glass)"
          strokeWidth="3"
        />
        <path
          d="M18 4 A14 14 0 0 1 32 18"
          stroke="var(--color-accent-purple)"
          strokeWidth="3"
          strokeLinecap="round"
        />
      </svg>
      {size !== 'sm' && (
        <span style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>{label}</span>
      )}
    </div>
  );
}
