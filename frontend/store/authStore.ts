import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: number;
  username: string;
  email: string;
  age_verified: boolean;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  setTokens: (access: string, refresh: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      setUser: (user) =>
        set({ user, isAuthenticated: !!user }),
      setTokens: (access, refresh) => {
        if (typeof window !== 'undefined') {
          localStorage.setItem('access_token', access);
          localStorage.setItem('refresh_token', refresh);
        }
        set({ isAuthenticated: true });
      },
      logout: () => {
        if (typeof window !== 'undefined') {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
        set({ user: null, isAuthenticated: false });
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
