import io from "socket.io-client";
// import axios from "axios";
import useAppState from "../zustand/useAppState";

// import { useStore } from "zustand";

// const socket = useRef(null);
// const socketUrl = "http://localhost:5001";

// socket.current = io(socketUrl, {
//   autoConnect: false,
// });

// const socket = io('http://localhost:5000'); // replace with your server URL

export function Dowload_Actions() {
  const { downloads, refreshDownloadItem, refreshDownload, initDownloads } =
    useAppState();
  // const init = () => {
  //   const { downloads, refreshDownloadItem, refreshDownload } =
  //     useStore(useAppState);
  // };
  var dd = {
    id: "0",
    Url: "",
    Status: "pending",
    Downloaded: 0,
    Speed: 256,
    Cmd_Option: "new",
    Catg: "UNKNOWN",
    Time_Left: 0,
    File_Size: 0,
    FileName: "",
    SavePath: "./",
    Resume: false,
  };
  
  const StartSessions = (socket) => {
    // console.log({"stateDownloads":downloads});

    socket.current.connect();
    // Handle connection events
    socket.current.on("connect", () => {
      console.log("Connected to socket  server");
      // initDownloads(data)
    });

    socket.current.on("load", (data) => {
      console.log({ "received data": data });
      initDownloads({ ...data });
      console.log({downloads:downloads});
    });

    socket.current.on("progres", (refreshData) => {
      console.log(`Refreshing singe item  from downloads from server,${refreshData}`);
      console.log({refreshData:refreshData})
      // Call the refreshDownload action in your Zustand store
      refreshDownload(refreshData);
    });

    // socket.current.on("initData", (initData) => {
    //   console.log("socket  setting up downloads from server");
    // });

    socket.current.on("disconnect", () => {
      console.log("Disconnected from server");
    });

  };

  const Follow_Progress_Item = (socket) => {
    socket.current.on("progres", (refreshData) => {
      console.log("Refreshing single progres item  from downloads from server");
      console.log({ refreshData: refreshData });
      // Call the refreshDownload action in your Zustand store
      refreshDownload(refreshData);
    });
  };

   const useDownloadItem = (id = "", name = "") => {
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

  return {
    StartSessions,
    Follow_Progress_Item,
    useDownloadItem,
  };
}

export function InitSocketSession(socket) {
  // const { downloads, initDownloads } = useStore(useAppState);
  const { downloads, refreshDownloadItem, refreshDownload } = useAppState();

  console.log("trying to initiate socket connect");
  socket.current.connect();

  // Handle connection events
  socket.current.on("connect", () => {
    console.log("Connected to socket  server");
  });
  
  // socket.current.on("initData", (initData) => {
  //   console.log("socket  setting up downloads from server");
  //   initDownloads(initData)
  // });

  socket.current.on("disconnect", () => {
    console.log("Disconnected from server");
  });
  // return Socket;
}

export function Follow_Progress_Item(socket) {
  // console.log("Follow progress item started");
  // socket.current.emit("progres", "whats up");
  socket.current.on("progres", (refreshData) => {
    console.log("Refreshing singe item  from downloads from server");
    console.log(refreshData);
    // Call the refreshDownload action in your Zustand store
    // refreshDownload(refreshData);
  });
}

export function Follow_Progress_bundle(socket) {
  socket.current.on("progres", (refreshData) => {
    console.log("Refreshing data from downloads from server");
    // Call the refreshDownload action in your Zustand store
    // refreshDownload(refreshData);
  });
}

// export const Follow_Progress_bundle = (socket) {
//   const { downloads, refreshDownloadItem, refreshDownload } =
//     useStore(useAppState);
//   socket.current.on("progres", (refreshData) => {
//     console.log("Refreshing data from downloads from server");
//     // Call the refreshDownload action in your Zustand store
//     refreshDownload(refreshData);
//   });
// };

export const StopListeners = (socket) => {
  socket.current.off("progres");
  console.log("stopped progress");
  //   if(dis){
  //     socket.current.disconnect();
  //     console.log("disconnected from server");
  //   }
};
