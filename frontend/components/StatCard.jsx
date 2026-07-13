import React from 'react';

export default function StatCard({
  label,
  value,
  changeText,
  theme = 'blue-theme',
  sparklinePath = 'M0 10 Q25 5 50 6 T100 2',
  strokeColor = '#3F83F8'
}) {
  const isIncrease = changeText ? changeText.includes('↑') : false;

  return (
    <div className={`stat-card ${theme}`}>
      <div className="stat-card-top">
        <span className="stat-lbl">{label}</span>
        <span className="stat-btn-add">+</span>
      </div>
      <div className="stat-num">{value}</div>
      <div className="stat-card-bottom">
        <span className={`stat-change ${isIncrease ? 'success' : 'warning'}`}>
          {changeText}
        </span>
        <svg className="sparkline-wave" viewBox="0 0 100 20">
          <path
            d={sparklinePath}
            fill="none"
            stroke={strokeColor}
            strokeWidth="1.5"
          />
        </svg>
      </div>
    </div>
  );
}
