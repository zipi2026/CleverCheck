import { create } from 'zustand';
import type { User } from '../types';

type AuthState = {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
};

export const useAuthStore = create<AuthState>((set: (partial: Partial<AuthState>) => void) => ({
  user: null,
  isAuthenticated: false,
  loading: true,
  setUser: (user: User | null) => set({ user, isAuthenticated: !!user, loading: false }),
  setLoading: (loading: boolean) => set({ loading }),
}));
