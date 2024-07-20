import create, { useStore } from "zustand";

type Download = {
  id: string;
  Url: string;
  Status: boolean;
  // "pending" | "downloading" | "completed" | "error"|"stoped"|"paused"
  Downloaded: number;
  Speed: number;
  Cmd_Option: string;
  Catg: string;
  Time_Left: number;
  File_Size: number;
  FileName: string;
  SavePath: string;
  Resume: boolean;
  Finished: boolean;
};

type ProgresDownload = {
  id: string;
  FileName: string;
  // Status: boolean;
};

type ProgresData = {
  progresID: ProgresDownload;
  setprogresID: (prg: ProgresDownload) => void;
};

type WindowsStates = {
  progressON: boolean;
  addUrlON: boolean;
  newDownloadON: boolean;
  displayProgress: (status: boolean) => void;
  displayAddUrl: (status: boolean) => void;
  displayNewDownload: (status: boolean) => void;
};

type IdmRequests = {
  NewItem: Download;
  CreateReq: (nwDown: Download) => void;
  CurrentRow: { [FileName: string]: Download };
  SetCurrentRow: (CurrentRow: { [FileName: string]: Download }) => void;
};

export const useProgresID = create<ProgresData>((set) => ({
  progresID: { id: "", FileName: "" },

  setprogresID: (theNewProgress: ProgresDownload) => {
    set((state) => ({ progresID: theNewProgress }));
  },
}));

export const useIdmRequests = create<IdmRequests>((set, get) => ({
  NewItem: null,
  CreateReq: (nwDown: Download) => {
    set((state) => {
      const n = { ...state.NewItem, NewItem: nwDown };
      // console.log("from state", state);
      return n;
    });
  },
  CurrentRow: null,
  SetCurrentRow: (theRow: { [FileName: string]: Download }) => {
    set((state) => ({ CurrentRow: theRow }));
  },
}));

export const useWindowsStore = create<WindowsStates>((set) => ({
  progressON: false,  
  addUrlON: false,
  newDownloadON: false,
  
  displayProgress: (value) => set((state) => ({ progressON: value })),
  displayAddUrl: (value) => set((state) => ({ addUrlON: value })),
  displayNewDownload: (value) => set((state) => ({ newDownloadON: value })),
}));

type AppState = {
  fname: string;
  downloads: { [FileName: string]: Download };
  initDownloads: (initData: { [FileName: string]: Download }) => void;
  refreshDownload: (comingData: { [FileName: string]: Download }) => void;
  addDownload: (nwDown: { [FileName: string]: Download }) => void;
};

const useAppState = create<AppState>((set, get) => ({
  fname: "",
  downloads: {},

  initDownloads: (initData: { [FileName: string]: Download }) => {
    
    set((state) => {
      state.downloads = { ...initData };
      return state.downloads;
    });
  },

  refreshDownload: (comingData: { [FileName: string]: Download }) => {
    console.log(comingData);
    set((state) => {
      state.downloads = {...comingData };
      return state.downloads;
    });
  },

  addDownload: (nwDown: { [FileName: string]: Download }) => {
    set((state) => {
      state.downloads = { ...state.downloads, ...nwDown };
      return null;
    });
  },
}));

export default useAppState;

export function useDownloadTable() {
  const { downloads } = useAppState();
  const downloadsArray = Object.values(downloads);
  return downloadsArray || [];
}
