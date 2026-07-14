/**
 * useApi.js — Generic Async Data Fetching Hook
 *
 * Provides: data, isLoading, error, retry, isOffline, isTimeout
 *
 * Usage:
 *   const { data, isLoading, error, retry } = useApi(() => fetchMeetings(), []);
 */

import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * @param {Function} apiFn — async function returning data
 * @param {Array} deps — dependency array (like useEffect)
 * @param {Object} options
 * @param {boolean} options.immediate — fetch on mount (default: true)
 * @returns {{ data, isLoading, error, retry, isOffline, isTimeout }}
 */
export function useApi(apiFn, deps = [], { immediate = true } = {}) {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(immediate);
  const [error, setError] = useState(null);
  const [isOffline, setIsOffline] = useState(!navigator.onLine);
  const [isTimeout, setIsTimeout] = useState(false);
  const callRef = useRef(0); // Prevents stale state from cancelled calls

  const execute = useCallback(async () => {
    const callId = ++callRef.current;
    setIsLoading(true);
    setError(null);
    setIsTimeout(false);

    try {
      const result = await apiFn();
      if (callId === callRef.current) {
        setData(result);
      }
    } catch (err) {
      if (callId !== callRef.current) return;
      if (err.code === 'TIMEOUT') setIsTimeout(true);
      setIsOffline(!navigator.onLine);
      setError(err.message ?? 'An unexpected error occurred.');
    } finally {
      if (callId === callRef.current) {
        setIsLoading(false);
      }
    }
  }, deps); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (immediate) execute();
  }, [execute, immediate]);

  // Monitor online/offline status
  useEffect(() => {
    const handleOnline = () => setIsOffline(false);
    const handleOffline = () => setIsOffline(true);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return { data, isLoading, error, retry: execute, isOffline, isTimeout };
}
