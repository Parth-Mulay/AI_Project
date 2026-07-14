/**
 * useDebounce.js — Search Debounce Utility Hook
 *
 * Delays updating the value until the user stops typing.
 * Prevents an API call on every keystroke.
 *
 * @param {*} value — the raw value to debounce
 * @param {number} delay — milliseconds to wait (default: 350)
 * @returns {*} — debounced value
 */
import { useState, useEffect } from 'react';

export function useDebounce(value, delay = 350) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
