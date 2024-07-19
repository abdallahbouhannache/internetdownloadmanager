import DownloadProgress from "./Download_Progress";
import NewDownload from "./New_Download";
import AddUrl from "./Add_Url";
import { useEffect, useState } from "react";
import axios from "axios";
import useAppState, { useIdmRequests, useWindowsStore } from "../zustand/useAppState";
import { IdmReq } from "../Utils/DownLoad_Action";

const DownloadWorker = ({ stc, dwAct }) => {

  const [progresID, setprogresID] = useState({});
  const [link, setLink] = useState("");
  
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

 

  const downloadFile = async (filedata) => {
    try {
     
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
    
  };
  const handleAddUrlClose = () => {
    displayAddUrl(false);
  };

  const handleNewDownloadClose = () => {
    displayNewDownload(false);
  };

  const handleProgressClose = () => {
    displayProgress(!progressON);
  };

  const DownloadLater = (data) => {
    
    idmR.StartItem(data);
    displayNewDownload(false);
 
  };

  const startProgress = (data) => {
    setprogresID(data);
    displayNewDownload(false);
    displayProgress(!progressON);
    idmR.StartItem(data);
    
  };

  return (
    <>
      {addUrlON && (
        <AddUrl
        show={addUrlON}
        handleClose={handleAddUrlClose}
        openNewDownload={openNewDownload}
        />
      )}

      {newDownloadON && (
        <NewDownload
          theUrl={link}
          show={newDownloadON}
          startProgress={startProgress}
          DownloadLater={DownloadLater}
          handleClose={handleNewDownloadClose}
        />
      )}

      {progressON && (
        <DownloadProgress
          dwAct={dwAct}
          progresID={progresID} 
          // change it to id?(could not be provided if new download),url to use them for grabbing/tracking the data from store
          show={progressON}
          handleClose={handleProgressClose}
        />
      )}

    </>
  );
};

export default DownloadWorker;
