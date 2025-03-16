import "./App.css";
import Confirm from "./Component/Confirm";
import DataTable from "./Component/DataTable";
import NavHead from "./Component/NavHead";
import New_Download from "./Component/New_Download";
import Add_Url from "./Component/Add_Url";
import Download_Progress from "@src/Component/Download_Progress";
import { Suspense, useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";
import { Button } from "react-bootstrap";
import DownloadWorker from "./Component/Download_worker";
import useAppState from "./zustand/useAppState";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import {
  Follow_Progress_Item,
  InitSocketSession,
  Dowload_Actions,
} from "./Utils/DownLoad_Action";


function App() {
  
  const donwloads = useAppState((state) => state.downloads);
  const dataTable = Object.values(donwloads);

  // const refreshData = (json_data: ArrayLike<unknown>) => {
  //   const data = Object.entries(json_data).map(
  //     ([fileName, fileInfo], index) => {
  //       const fileInfoAny = fileInfo as any; // Type assertion to 'any'
  //       return {
  //         N: index + 1,
  //         fileName,
  //         Status: fileInfoAny.running ? "downloading" : "stop",
  //         Finished: false,
  //         Time_Left: fileInfoAny.Time_Left,
  //         Downloaded: fileInfoAny.Downloaded,
  //         Speed: fileInfoAny.Speed,
  //         Extension: fileName.substring(fileName.lastIndexOf(".")),
  //         FileSize: fileInfoAny.Size,
  //         Url: fileInfoAny.Url,
  //       };
  //     }
  //   );
  //   return data;
  // };

  const socket = useRef(null);
  const socketUrl = "http://localhost:5001";
  socket.current = io(socketUrl, {
    autoConnect: false,
  });

  const downloadActions = Dowload_Actions();

  useEffect(() => {
    downloadActions.StartSessions(socket);

    return () => {
    };
  }, []);

  // console.log("re-rendring the app");


  const sendMessage = (message) => {
    toast("Hello Geeks");
    socket.current.emit('message', 'Hello am front ');
    // console.log(message);
  };

  return (
    <Suspense>
      {/* fallback={<Spin size="large" className="layout__loading" />} */}
      <div className="App" style={{ border: "1px solid " }}>
        <NavHead />
        <DownloadWorker dwAct={downloadActions} stc={socket.current} />

        <Button variant="primary" onClick={sendMessage}>
          send MSG
        </Button>
        <ToastContainer
          position="bottom-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />

        <DataTable dataTable={dataTable} />

        {/* <Confirm /> */}
        {/* <New_Download /> */}
        {/* <Add_Url /> */}
        {/* <Download_Progress /> */}
      </div>
    </Suspense>
  );
}

export default App;