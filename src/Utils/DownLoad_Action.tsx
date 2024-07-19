import useAppState, { useIdmRequests } from "../zustand/useAppState";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import { CATEGORY_TYPES } from "../Constant/Constant";
import swal from "sweetalert";
import { Bounce, Slide, toast } from "react-toastify";

export function Dowload_Actions() {
  const { downloads, refreshDownload, initDownloads } = useAppState();

  const StartSessions = (socket) => {
    socket.current.connect();

    // Handle connection events
    socket.current.on("connect", () => {
      toast("Welcome", {
        position: "bottom-right",
        autoClose: 500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "light",
        transition: Bounce,
      });
      console.log("Connected to socket  server");
    });

    socket.current.on("load", (data) => {
      initDownloads(data);
    });

    socket.current.on("progres", (refreshData) => {
      console.log(refreshData);
      console.log("progres refresh");
      refreshDownload(refreshData);
    });

    socket.current.on("disconnect", () => {
      console.log("Disconnected from server");
    });
  };

  const Follow_Progress_Item = (socket) => {
    socket.current.on("progres", (refreshData) => {
      console.log("Refreshing single progres item  from downloads from server");
      console.log({ refreshData: refreshData });
    });
  };

  const useDownloadItem = (id = "", name = ""): {} => {
    if (name) {
      return downloads[name];
    } else if (id) {
      return downloads[id];
    }
    return {};
  };

  return {
    StartSessions,
    Follow_Progress_Item,
    useDownloadItem,
  };
}

export function InitSocketSession(socket) {
  const { downloads, refreshDownload } = useAppState();
  console.log("trying to initiate socket connect");
  socket.current.connect();

  // Handle connection events
  socket.current.on("connect", () => {
    console.log("Connected to socket  server");
  });

  socket.current.on("disconnect", () => {
    console.log("Disconnected from server");
  });
}

export function Follow_Progress_Item(socket) {
  socket.current.on("progres", (refreshData) => {
    console.log("Refreshing singe item  from downloads from server");
    console.log(refreshData);
  });
}

export function Follow_Progress_bundle(socket) {
  socket.current.on("progres", (refreshData) => {
    console.log("Refreshing data from downloads from server");
  });
}

export const StopListeners = (socket) => {
  socket.current.off("progres");
  console.log("stopped progress");
};

// function
export const IdmReq = () => {
  // the store manager
  const { NewItem, CreateReq, CurrentRow, SetCurrentRow } = useIdmRequests();
  const { addDownload } = useAppState();

  // @ts-ignore
  const cat_selector = (ext: string) => {
    let category = Object.entries(CATEGORY_TYPES).find(([key, value]) => {
      const fileInfoAny = value as any; // Type assertion to 'any'
      return fileInfoAny.includes(ext);
    });
    return category ? category[0] : "UNKNOWN";
  };

  async function getFileDtailsFront(url) {
    try {
      let newData = {
        id: "11",
        Url: url,
        Status: true,
        Downloaded: 0,
        Speed: 120000,
        Cmd_Option: "new",
        Catg: "UNKNOWN",
        Time_Left: 0,
        File_Size: 100000,
        FileName: "winrar",
        SavePath: "./",
        Resume: true,
        Finished: false,
      };
      // add handling if no result or error in head
      const response1 = await axios.head(url);
      const contentDisposition = response1.headers["content-disposition"];
      newData["File_Size"] = parseInt(response1.headers["content-length"], 10);
      if (contentDisposition) {
        newData["FileName"] = contentDisposition.split("filename=")[0];
      } else {
        newData["FileName"] = url.split("/").pop().trim();
      }
      let [file_name, ext] = newData["FileName"].split(".") || "download.html";

      newData["id"] = uuidv4();
      newData["Catg"] = cat_selector(ext);

      const response2 = await axios.get("http://localhost:5001/get_file_name", {
        params: {
          name: file_name,
          ext: ext,
        },
      });

      newData["FileName"] = response2.data;
      console.log(newData);
      CreateReq(newData);

      return newData;
    } catch (error) {
      console.log("Error: getFileDtailsFront >");
      if (error.response) {
        console.log(error.response.data);
        console.log(error.response.status);
      } else if (error.request) {
        console.log(error.request);
      } else {
        console.log(error.message);
      }
    }
  }

  const InitItem = async (url) => {
    const filedata = await getFileDtailsFront(url);
  };

  const StartItem = async (data) => {
    let newFileD = {};
    newFileD[data["FileName"]] = data;

    addDownload(newFileD);
    axios.post("http://localhost:5001/download_file", data).then((response) => {
      console.log({ "download_file_server_response ended": response });
    });
  };

  const ContinueItems = async (par) => {
    console.log(par);
    axios
      .post("http://localhost:5001/resume_download", par)
      .then((response) => {
        console.log({ "download_file_server_response ended": response });
      });
  };

  const StopItems = async (par) => {
    console.log(par);
    axios.post("http://localhost:5001/stop_download", par).then((response) => {
      console.log({ "download_file_server_response ended": response });
    });
  };

  const DelItems = async (par) => {
    // console.log("from the down_actions > DelItems ");
    // console.log(par);

    swal({
      title: "Are you sure?",
      text: "Once deleted, you will not be able to recover this file!",
      icon: "warning",
      buttons: ["No", "Yes"],
      dangerMode: true,
    }).then((willDelete) => {
      if (willDelete) {
        axios
          .post("http://localhost:5001/delete_download", par)
          .then((response) => {
            
            let info = "Selected Files Were Deleted";
            toast(info, {
              position: "bottom-right",
              autoClose: 300,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: true,
              draggable: true,
              progress: undefined,
              theme: "colored",
              transition: Bounce,
            });
          });
      }
    });

    return;
    axios.post("http://localhost:5001/delete_download", par).then((rs) => {
      if (rs["status"] == 200) {
        console.log("file deleted from list", rs.data["rs"]);
      } else {
        console.log("file not found on download list", rs.data["rs"]);
      }
    });
  };

  return {
    InitItem,
    StartItem,
    ContinueItems,
    StopItems,
    DelItems,
  };
};
