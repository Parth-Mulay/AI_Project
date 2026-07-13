import React from 'react';

export default function Input({
  label,
  id,
  type = 'text',
  value,
  onChange,
  placeholder = '',
  error = '',
  required = false,
  className = '',
  ...props
}) {
  return (
    <div className={`input-group ${className}`.trim()}>
      {label && (
        <label htmlFor={id} className="input-label">
          {label} {required && <span style={{ color: 'var(--color-accent-red)' }}>*</span>}
        </label>
      )}
      <input
        type={type}
        id={id}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : undefined}
        className={`input-field ${error ? 'error-border' : ''}`.trim()}
        {...props}
      />
      {error && (
        <span id={`${id}-error`} className="error-text" role="alert">
          ⚠️ {error}
        </span>
      )}
    </div>
  );
}
