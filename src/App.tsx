import "./App.css";
import Confirm from "./Component/Confirm";
import DataTable from "./Component/DataTable";
import NavHead from "./Component/NavHead";
import New_Download from "./Component/New_Download";
import Add_Url from "./Component/Add_Url";
import Download_Progress from "@src/Component/Download_Progress";
import { useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";
import { Button } from "react-bootstrap";
import DownloadWorker from "./Component/Download_worker";

import useAppState from "./zustand/useAppState";
import { useStore } from "zustand";

import { Follow_Progress_Item, InitSocketSession ,Dowload_Actions} from "./Utils/DownLoad_Action";

function App() {
  const [tableData, settableData] = useState([]);
  
  const { downloads, refreshDownloadItem, refreshDownload,initDownloads } =
      useAppState();

  const refreshData = (json_data: ArrayLike<unknown>) => {

    const data = Object.entries(json_data).map(
      ([fileName, fileInfo], index) => {
        const fileInfoAny = fileInfo as any; // Type assertion to 'any'
        return {
          N: index + 1,
          fileName,
          Status: fileInfoAny.running ? "downloading" : "stop",
          Finished: false,
          Time_Left: fileInfoAny.Time_Left,
          Downloaded: fileInfoAny.Downloaded,
          Speed: fileInfoAny.Speed,
          Extension: fileName.substring(fileName.lastIndexOf(".")),
          FileSize: fileInfoAny.Size,
          Url: fileInfoAny.Url,
        };
      }
    );
    return data;
  };

  
  const socket = useRef(null);
  const socketUrl = "http://localhost:5001";
  socket.current = io(socketUrl, {
    autoConnect: false,
  });

  // InitSocketSession(socket);
  // Follow_Progress_Item(socket);

  const downloadActions = Dowload_Actions();
    
  useEffect(()=>{
    // initDownloads({})
    downloadActions.StartSessions(socket);

    // setTimeout(() => {
    //   downloadActions.Follow_Progress_Item(socket);
    // }, 5000);
    
  },[])
  
  

  // useEffect(() => {
    // socket = io("http://localhost:5001");
    

    // socket.current.connect();
    
    // Follow_Progress_Item(socket);

    // Listen for the `connect` event
    // socket.current.on("connect", () => {
    //   console.log("Connected to server.");
    // });

  //   socket.current.on("initData", (initData) => {
  //     console.log("setting up downloads from server");
  //     initDownloads(initData)
  //   });

  //   socket.current.on("progress", (refreshData) => {
  //     console.log("refreshing data from downloads from server");
  //     refreshDownload(refreshData)
  //   });

  //   // Listen for the `progres` event
  //   socket.current.on("progres", (data) => {
  //     let nwData = refreshData(data);
  //     console.log(nwData);
  //     // let download_sts = Object.entries(data);
  //     // let download_status = Object.keys(data);
  //     // console.log(download_sts);
  //     settableData(nwData);
  //   });

  //   // Listen for the `message` event
  //   socket.current.on("message", (msg) => {
  //     console.log({ msg });
  //     // let download_status = Object.entries(data);
  //     // console.log({ received: download_status });
  //     // setMessages(() => data);
  //   });

  //   // Send a message
  //   socket.current.emit("message", "Hello from the FRONTEND!");

  //   return () => {
  //     socket.current.disconnect();
  //     console.log("disconnected");
  //   };
    
  // }, [socketUrl]);

  const sendMessage = (message) => {
    console.log(message);
    // if (socket.current.connected) {
    //   socket.current.emit("progres", "send me updates ");
    // }
  };

  return (
    <div className="App" style={{ border: "1px solid " }}>
      <NavHead />
      <DownloadWorker stc={socket.current} />

      <Button variant="primary" onClick={sendMessage}>
        send MSG
      </Button>
      <DataTable dataTable={tableData} />
      {/* <Confirm /> */}
      {/* <New_Download /> */}
      {/* <Add_Url /> */}
      {/* <Download_Progress /> */}
    </div>
  );

}

export default App;