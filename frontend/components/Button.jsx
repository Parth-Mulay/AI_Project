import React from 'react';

export default function Button({
  children,
  onClick,
  type = 'button',
  variant = 'primary',
  fullWidth = false,
  small = false,
  disabled = false,
  ariaLabel = undefined,
  className = ''
}) {
  const baseClass = 'btn';
  const variantClass = `btn-${variant}`;
  const widthClass = fullWidth ? 'btn-full' : '';
  const sizeClass = small ? 'btn-small' : '';

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      aria-label={ariaLabel}
      className={`${baseClass} ${variantClass} ${widthClass} ${sizeClass} ${className}`.trim()}
    >
      {children}
    </button>
  );
}
