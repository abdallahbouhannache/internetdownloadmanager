import create from "zustand";

type State = {
  count: number;
};

type Actions = {
  increaseCount: () => void;
  resetCount: () => void;
};

const useCountStore = create<State & Actions>((set) => ({
  count: 0,
  increaseCount: () => set((state) => ({ count: state.count + 1 })),
  resetCount: () => set({ count: 0 }),
}));

export default useCountStore;
