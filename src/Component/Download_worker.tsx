import DownloadProgress from "./Download_Progress";
import NewDownload from "./New_Download";
import AddUrl from "./Add_Url";
import { useEffect, useState } from "react";
import axios from "axios";
import useAppState, { useIdmRequests, useWindowsStore } from "../zustand/useAppState";
import { IdmReq } from "../Utils/DownLoad_Action";

import { v4 as uuidv4 } from "uuid";

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

  const { addDownload, downloads } = useAppState();

  const idmR = IdmReq();
  
  const { CreateReq,NewItem } = useIdmRequests(state => state);

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

    idmR.InitItem(uri);
    
    // console.log({uri});
    // CreateReq(newData)
    // AddX(55)
    // console.log({x});
    // console.log({"this has been .added to table ":NewItem});

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

  const DownloadLater = (data) => {
    // displayProgress(false);
    // displayProgress(!progressON);
    // console.log("download_later:: ",data);
    // idmR.AppendToDownloads(data);
    idmR.StartItem(data);
    displayNewDownload(false);

    // return
    
    // let newFileD = {};
    // newFileD[data["FileName"]] = data;

    // let newData = {
    //   id: "11",
    //   Url: "url",
    //   Status: true,
    //   Downloaded: 0,
    //   Speed: 120000,
    //   Cmd_Option: "new",
    //   Catg: "UNKNOWN",
    //   Time_Left: 0,
    //   File_Size: 0,
    //   FileName: "winrar",
    //   SavePath: "./",
    //   Resume: false,
    //   Finished: false,
    // };

    // console.log("later download",data);

    // addDownload(newFileD);

  };
  const startProgress = (data) => {
    // let name=newDownloadData['FileName']
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

    setprogresID(data);
    displayNewDownload(false);
    displayProgress(!progressON);
    idmR.StartItem(data);
    

    // downloadFile(data);
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
        show={addUrlON}
        handleClose={handleAddUrlClose}
        openNewDownload={openNewDownload}
           // url={""}
          // openNewDownload={getFileDetails}
        />
      )}

      {newDownloadON && (
        <NewDownload
          theUrl={link}
          show={newDownloadON}
          startProgress={startProgress}
          DownloadLater={DownloadLater}
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
