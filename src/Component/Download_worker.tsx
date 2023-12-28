import DownloadProgress from "./Download_Progress";
import NewDownload from "./New_Download";
import AddUrl from "./Add_Url";

import { v4 as uuidv4 } from "uuid";

import { useEffect, useState } from "react";
import axios from "axios";

import  useAppState, { useWindowsStore  }  from "../zustand/useAppState";
// import { useStore } from "zustand";

const DownloadWorker = ({ stc, dwAct }) => {
  //   function getFileExtension(url) {
  //     var match = url.match(/\.[^.]+$/);
  //     return match ? match[0].substring(1) : '';
  //  }

  const [progresID, setprogresID] = useState({});
  // var DownloadItem = {};
  const [link, setLink] = useState("");
  // const [progresID, setprogresID] = useState({ id: "0", name: "" });

  // for managing state of  the views
  const {
    displayNewDownload,
    newDownloadON,
    displayProgress,
    progressON,
    addUrlON,
    displayAddUrl,
  } = useWindowsStore();

  const { addDownload ,downloads} = useAppState();
  // const downloads=useStore(useAppState, (state) => state.downloads);

  // for manaing state of functionalities
  // const { addDownload, initDownloads, downloads, setfname } = useAppState();

  // for setting intial values
  //for displaying the modals
  // const [progressON, displayProgress] = useState(false);
  // const [addUrlON, displayAddUrl] = useState(false);
  // const [newDowloadON, displayNewDownload] = useState(false);

  const downloadFile = async (filedata) => {
    try {
      // const fileInfos = {
      //   Url: "https://example.com/file-url",
      //   SavePath: "./path/to/save",
      //   FileName: "example-file.txt",
      //   Speed: 1024,
      //   Cmd_Option: "new",
      // };

      // const response = await axios.post('http://localhost:5000/download_file', filedata);
      console.log("STARTING DOWNLOAD WITH");
      console.log({ "SENDING THIS FILE DTAILS TO BACKEND": filedata });

      axios
        .post("http://localhost:5001/download_file", filedata)
        .then((response) => {
          console.log({ "download_file_server_response ended": response });
        });
    } catch (error) {
      console.error(error);
    }

  };

  const openNewDownload = (uri) => {
    setLink(uri);
    displayNewDownload(!newDownloadON);
  };
  const handleAddUrlClose = () => {
    displayAddUrl(false);
  };

  const handleNewDownloadClose = () => {
    displayNewDownload(false);
  };

  const handleProgressClose = () => {
    // displayProgress(false);
    displayProgress(!progressON);
  };


  const startProgress = (data) => {
    // let name=newDownloadData['FileName']
    console.log({ "startprogress data": data });
    
    // var dd = {
    //   id: "0",
    //   Url: "",
    //   Status: false,
    //   Downloaded: 0,
    //   Speed: 256,
    //   Cmd_Option: "new",
    //   Catg: "UNKNOWN",
    //   Time_Left: 0,
    //   File_Size: 0,
    //   FileName: "winrar-x64-623(3).exe",
    //   SavePath: "./",
    //   Resume: false,
    // };

    let newItem = {}
    newItem[data['FileName']]=data;
    setprogresID(data);
    
    addDownload(newItem);
    displayNewDownload(false);
    displayProgress(!progressON);
    
    downloadFile(data);
    
    // socket.current.off("filed", ()=>{});
    // if (id) {
    //   // newDownloadData.id = id;
    // } else {
    //   console.log("error in adding to store");
    // }
  };

  // useEffect(() => {
  //   console.log({ stc: stc });
  //   stc.on("filed", (fileDetails) => {
  //     console.log({ ...fileDetails });
  //     // setprogresID({ id: fileDetails.id, name: fileDetails.FileName });
  //     setprogresID(fileDetails);
  //     stc.off("filed", () => {});
  //   });
  // }, [progressON]);

  return (
    <>
      {addUrlON && (
        <AddUrl
          // url={""}
          show={addUrlON}
          handleClose={handleAddUrlClose}
          // openNewDownload={getFileDetails}
          openNewDownload={openNewDownload}
        />
      )}

      {newDownloadON && (
        <NewDownload
          theUrl={link}
          show={newDownloadON}
          startProgress={startProgress}
          handleClose={handleNewDownloadClose}
          // showProgressBox={() => displayProgress(!progressON)}
        />
      )}

      {progressON && (
        <DownloadProgress
          dwAct={dwAct}
          progresID={progresID} // change it to id?(could not be provided if new download),url to use them for grabbing/tracking the data from store
          show={progressON}
          handleClose={handleProgressClose}
        />
      )}
    </>
  );
};

export default DownloadWorker;
