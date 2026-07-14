import React from 'react';

/**
 * SkeletonCard — Animated placeholder while content loads
 * Mimics the shape of a MeetingCard row.
 */
export default function SkeletonCard({ count = 3 }) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="skeleton-card" aria-hidden="true">
          <div className="skeleton-line" style={{ width: '55%', height: '14px' }} />
          <div className="skeleton-line" style={{ width: '30%', height: '12px', marginTop: '8px' }} />
          <div style={{ display: 'flex', gap: '8px', marginTop: '10px' }}>
            <div className="skeleton-line" style={{ width: '60px', height: '10px' }} />
            <div className="skeleton-line" style={{ width: '60px', height: '10px' }} />
          </div>
        </div>
      ))}
    </>
  );
}
