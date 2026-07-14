import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { fetchCurrentUser } from '../services/userService.js';

/**
 * AuthContext — Authentication & User Profile State
 *
 * Provides: user, isAuthenticated, isLoading, userRole,
 *           setUserRole, logout, refreshUser
 *
 * Security:
 *   - Auth tokens are NEVER stored in localStorage/sessionStorage.
 *   - Backend manages tokens via HttpOnly, Secure, SameSite=Lax cookies.
 *   - On logout, context state is cleared and a full redirect is triggered
 *     to prevent cached sensitive views.
 *   - TODO(security): Integrate OAuth 2.0 / OpenID Connect provider.
 *   - TODO(security): Add MFA support.
 */

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [authError, setAuthError] = useState(null);

  const loadUser = useCallback(async () => {
    setIsLoading(true);
    setAuthError(null);
    try {
      const profile = await fetchCurrentUser();
      setUser(profile);
    } catch {
      // In mock mode this never fails; in real mode, 401 means not logged in.
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  const setUserRole = useCallback((role) => {
    setUser((prev) => prev ? { ...prev, role } : prev);
  }, []);

  const logout = useCallback(async () => {
    try {
      const { logout: logoutApi } = await import('../services/userService.js');
      await logoutApi();
    } catch {
      // Proceed with local logout even if server call fails
    } finally {
      // Clear all in-memory state
      setUser(null);
      // Full page redirect clears React state, browser cache, and any
      // sensitive data visible in current session — security requirement.
      window.location.href = '/';
    }
  }, []);

  const isAuthenticated = Boolean(user);

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated,
      isLoading,
      authError,
      userRole: user?.role ?? 'Member',
      setUserRole,
      logout,
      refreshUser: loadUser,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuthContext() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuthContext must be used within AuthProvider');
  return ctx;
}
