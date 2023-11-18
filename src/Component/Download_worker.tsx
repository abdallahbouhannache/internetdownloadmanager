import DownloadProgress from "./Download_Progress";
import NewDownload from "./New_Download";
import AddUrl from "./Add_Url";
import useAppState, { useWindowsStore } from "../zustand/useAppState";

import { v4 as uuidv4 } from "uuid";

import { useEffect, useState } from "react";
import axios from "axios";
import { useStore } from "zustand";

const DownloadWorker = ({stc}) => {
  const defaultDownload = {
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
//   function getFileExtension(url) {
//     var match = url.match(/\.[^.]+$/);
//     return match ? match[0].substring(1) : '';
//  }

 
  const [newDownloadData, setNewDownloadData] = useState(defaultDownload);
  const [progresID, setprogresID] = useState();
  // const [progresID, setprogresID] = useState({ id: "0", name: "" });

  // for managing state of  the views
  const {
    displayNewDownload,
    newDownloadON,
    displayProgress,
    progressON,
    addUrlON,
    displayAddUrl,
  } = useStore(useWindowsStore);

  // const { addDownload } = useAppState();
  // const downloads=useStore(useAppState, (state) => state.downloads);

  // for manaing state of functionalities
  const { addDownload, initDownloads, downloads,setfname } = useAppState();

  // for setting intial values
  //for displaying the modals
  // const [progressON, displayProgress] = useState(false);
  // const [addUrlON, displayAddUrl] = useState(false);
  // const [newDowloadON, displayNewDownload] = useState(false);

  async function getFileDetails(url) {
    // setshowAdd_Url(!showAdd_Url);
    displayNewDownload(!newDownloadON);
    try {
      const response = axios.head(url);
      response
        .then((rs) => {
          // console.log(rs);
          // console.log(rs.headers["content-length"]);
          // let newData = {
          //   new_url: url,
          //   savePath: "./",
          //   name_file: "",
          //   catg: "UNKNOWN",
          //   size: 0,
          //   speed_limit: 256,
          //   command_option: "new",
          //   downloaded: 0,
          //   Resume: "false",
          // };
          let newData = {
            id: "0",
            Url: url,
            Status: "completed",
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

          const id = uuidv4(); // Implement a function to generate a unique ID
          
          
          // newData["FileName"] = getFileExtension(url)
          newData["FileName"] = url.split("/").pop().trim();
          newData["File_Size"] = rs.headers["content-length"];
          newData["id"]=id
          setfname(newData["FileName"])

          // cat_selector("")
          // console.log({"newData":newData});
          setNewDownloadData(newData);
          // addDownload(newData);
          console.log("send to backend from getFileDetails");
          //   updateDownloadStatus(newData.id, newData.status);
        })
        .catch((error) => {
          console.log({ errr: error });
        });
    } catch (error) {
      console.error("Error:fin", error.message);
    }
  }

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
      console.log({"SENDING THIS FILE DTAILS TO BACKEND":filedata});

      
      axios
      .post("http://localhost:5001/download_file", filedata)
      .then((response) => console.log({"download_file_server_response ended":response}));
      
    } catch (error) {
      console.error(error);
    }
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
    // addDownload({[name]:newDownloadData});
    console.log({"startprogress data":data});
    
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

  useEffect(()=>{
    console.log({"stc":stc});
    stc.on("filed", (fileDetails)=>{
      console.log({...fileDetails});
      // setprogresID({ id: fileDetails.id, name: fileDetails.FileName });
      setprogresID(fileDetails);
      stc.off("filed", ()=>{});
    });
  },[progressON])




  return (
    <>
      {addUrlON && (
        <AddUrl
          url={""}
          show={addUrlON}
          handleClose={handleAddUrlClose}
          openNewDownload={getFileDetails}
        />
      )}

      {newDownloadON && (
        <NewDownload
          data={newDownloadData}
          show={newDownloadON}
          // showProgressBox={() => displayProgress(!progressON)}
          startProgress={startProgress}
          handleClose={handleNewDownloadClose}
        />
      )}

      {progressON && (
        <DownloadProgress
          progresID={progresID} // change it to id?(could not be provided if new download),url to use them for grabbing/tracking the data from store
          show={progressON}
          handleClose={handleProgressClose}
        />
      )}
    </>
  );
};

export default DownloadWorker;
