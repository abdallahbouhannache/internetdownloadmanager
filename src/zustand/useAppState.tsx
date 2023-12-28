import create, { useStore } from "zustand";
import { v4 as uuidv4 } from "uuid";



type WindowsStates = {
  progressON: boolean;
  addUrlON: boolean;
  newDownloadON: boolean;
  displayProgress: (status: boolean) => void;
  displayAddUrl: (status: boolean) => void;
  displayNewDownload: (status: boolean) => void;
};

export const useWindowsStore = create<WindowsStates>((set) => ({
  progressON: false,
  displayProgress: (value) => set((state) => ({ progressON: value })),

  addUrlON: false,
  displayAddUrl: (value) => set((state) => ({ addUrlON: value })),

  newDownloadON: false,
  displayNewDownload: (value) => set((state) => ({ newDownloadON: value })),
}));

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
  // FileName: string;
  SavePath: string;
  Resume: boolean;
  // Finished: boolean;
};

type AppState = {
  // downloads: Download[];
  fname:string;
  downloads: { [FileName: string]: Download };
  initDownloads: (initData: { [FileName: string]: Download }) => void;
  refreshDownload: (comingData: { [FileName: string]: Download }) => void;
  addDownload: (nwDown: { [FileName: string]: Download }) => void;
  refreshDownloadItem: (comingData: Download) => void;
  setfname: (fn: string) => void;
  // removeDownload: (id: string) => void;
  // updateDownloadStatus: (id: string, Status: Download["Status"]) => void;
  // updateDownloadProgress: (id: string, progress: number) => void;
  // updateDownloadSpeed: (id: string, speed: number) => void;
  // updateDownloadSize: (id: string, size: number) => void;
  // useDownloadItem: (id: string,url: string) => Download | any;
};

// type State = {
//   count: number;
// };

// type Actions = {
//   increaseCount: () => void;
//   resetCount: () => void;
// };

const useAppState = create<AppState>((set,get) => ({
  fname:"",
  downloads: {},

  initDownloads: (initData: { [FileName: string]: Download }) => {
    // console.log({ initData:initData });
    set((state) => ({ downloads: { ...initData } }));
  },
  // downloads: [],

  // initDownloads: (initData) => {
  //   set((state) => ({ downloads: [...initData] }));
  // },
  // console.log({comingData:comingData});
  refreshDownload: (comingData: { [FileName: string]: Download }) => {
    console.log("refresh called");
    set((state) => ({ downloads: { ...state.downloads,...comingData } }));
    
  },
  // getDownloads:()=>{
  //   get(()=>  )
  // },
  addDownload: (nwDown: { [FileName: string]: Download }) => {
    // const id = uuidv4(); // Implement a function to generate a unique ID
    // nwDown.id=id;

    // const newDownload: { [FileName: string]: Download } = {
    //   ...nwDown
    // };

    set((state) => ({ downloads: { ...state.downloads, ...nwDown } }));
    // return id;
  },

  refreshDownloadItem: (comingData) => {
    // set((state) => ({ downloads: [...state.downloads, ...comingData] }));
    // console.log(comingData);
    return;
    // set((state) => ({
    //   downloads: state.downloads.map((download) =>
    //     download.id === comingData.id ? { ...comingData } : download
    //   ),
    // }));
  },


  setfname: (fn) => {
    set((state) => ({
      fname: fn,
    }));
  },

  // removeDownload: (id) => {
  //   set((state) => ({
  //     downloads: state.downloads.filter((download) => download.id !== id),
  //   }));
  // },
  // updateDownloadStatus: (id, Status) => {
  //   set((state) => ({
  //     downloads: state.downloads.map((download) =>
  //       download.id === id ? { ...download, Status } : download
  //     ),
  //   }));
  // },
  // updateDownloadProgress: (id, progress) => {
  //   set((state) => ({
  //     downloads: state.downloads.map((download) =>
  //       download.id === id ? { ...download, progress } : download
  //     ),
  //   }));
  // },
  // updateDownloadSpeed: (id, speed) => {
  //   set((state) => ({
  //     downloads: state.downloads.map((download) =>
  //       download.id === id ? { ...download, speed } : download
  //     ),
  //   }));
  // },
  // updateDownloadSize: (id, size) => {
  //   set((state) => ({
  //     downloads: state.downloads.map((download) =>
  //       download.id === id ? { ...download, size } : download
  //     ),
  //   }));
  // },
  // useDownloadItem: (id="",url) => {
  //   return (state) => state.downloads.find((item) => item.url === url || item.id ===id);
  // },

  // useDownloadItem: (url) => set((state) => state.downloads.find((item) => item.url === url)),
}));

export default useAppState;

// Selector function to get a single download item

export const useDownloadItem = (id = "", name = "") => {
  const { downloads } = useAppState();
  // console.log({ downloadsInside: downloads });
  // If both id and url are provided, prioritize id
  if (name) {
    return downloads[name];
    // return downloads.find((download) => download.id === id);
  } else if (id) {
    return downloads[id];
    // return downloads.find((download) => download.Url === url);
  }

  // If neither id nor url is provided, return null
  // return null;
};

// const downloads=useStore(useAppState, (state) => state.downloads);

