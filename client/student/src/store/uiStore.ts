import { create } from 'zustand';

type UIState = {
  timerVisible: boolean;
  sidebarOpen: boolean;
  setTimerVisible: (value: boolean) => void;
  setSidebarOpen: (value: boolean) => void;
};

export const useUIStore = create<UIState>((set: (partial: Partial<UIState>) => void) => ({
  timerVisible: true,
  sidebarOpen: true,
  setTimerVisible: (timerVisible: boolean) => set({ timerVisible }),
  setSidebarOpen: (sidebarOpen: boolean) => set({ sidebarOpen }),
}));
