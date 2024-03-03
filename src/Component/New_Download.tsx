import {
  Container,
  Row,
  Col,
  Form,
  Button,
  Image,
  InputGroup,
  FormControl,
  Modal,
} from "react-bootstrap";
import { PlusSquare, Save, Clipboard } from "react-bootstrap-icons";
import fileIcon from "../assets/categoryFile.png";
import React, { useEffect, useState } from "react";

import { CATEGORY_TYPES } from "../Constant/Constant";
import CopyWrapper from "./copyClipBoard";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import { IdmReq } from "../Utils/DownLoad_Action";
import  { useIdmRequests }  from "../zustand/useAppState";

// import { useFilePicker } from "use-file-picker";

// --------------
// i need to compare received name of file with
// names in downloads file of global stats
// if it matches ,should ask question of do you want restart download

// ------
// setfname(newData["FileName"]);
// setNewDownloadData(newData);
// setprogresID(newData);
// -----

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
// let newData = {
//   id: "0",
//   Url: url,
//   Status: "completed",
//   Downloaded: 0,
//   Speed: 256,
//   Cmd_Option: "new",
//   Catg: "UNKNOWN",
//   Time_Left: 0,
//   File_Size: 0,
//   FileName: "",
//   SavePath: "./",
//   Resume: false,
// };

// const id = uuidv4(); // Implement a function to generate a unique ID
// // newData["FileName"] = getFileExtension(url)
// newData["FileName"] = url.split("/").pop().trim();
// newData["File_Size"] = rs.headers["content-length"];

// newData["id"] = id;

// cat_selector("")
// console.log({"newData":newData});
// addDownload(newData);
// updateDownloadStatus(newData.id, newData.status);

function New_Download({ theUrl, show, DownloadLater,startProgress, handleClose }) {

  const idmR = IdmReq();
  // the store manager 
  const {
    NewItem,
    CreateReq
  } = useIdmRequests();

  // var data = {
  //   Url: "",
  //   SavePath: "",
  //   FileName: "",
  //   Catg: "",
  //   size: "",
  //   speed_limit: "",
  //   command_option: "",
  //   ext: "",
  // };

  var data = {
    id: "",
    Url: "",
    Status: true,
    Downloaded: 0,
    Speed: 256,
    Cmd_Option: "new",
    Catg: "UNKNOWN",
    Time_Left: 0,
    File_Size: 10000,
    FileName: "",
    SavePath: "./",
    Resume: true,
  };

  // let defaultDownload = {
  //   id: "0",
  //   Url: "",
  //   Status: "pending",
  //   Downloaded: 0,
  //   Speed: 256,
  //   Cmd_Option: "new",
  //   Catg: "UNKNOWN",
  //   Time_Left: 0,
  //   File_Size: 0,
  //   FileName: "",
  //   SavePath: "./",
  //   Resume: false,
  // };

  function getFileExtension(url) {
    var match = url.match(/\.[^.]+$/);
    return match ? match[0].substring(1) : "";
  }

  // @ts-ignore
  const cat_selector = (ext: string) => {
    let category = Object.entries(CATEGORY_TYPES).find(([key, value]) => {
      const fileInfoAny = value as any; // Type assertion to 'any'
      return fileInfoAny.includes(ext);
    });
    return category ? category[0] : "UNKNOWN";
  };

  // const getFileName=(url:string)=>{
  //   let {file_name,ext}=url.split("/").pop().trim();
  //   // get fileName from downloads state
  //   downloads
  // }

  const [LocalData, setLocalData] = useState(data);

  // const [url, setUrl] = useState(data.Url);
  // const [selectdPath, setSelectdPath] = useState(data.SavePath);
  // const [filename, setFilename] = useState(data.FileName);
  // const [category, setCategory] = useState(data.Catg);
  // const [fileSize, setFileSize] = useState(data.File_Size);

  // const afterOpenModal = () => {
  //   // data = props.data;
  //   // setLocalData(e=>({...e,...props.data}))
  //   // setLocalData(e=>({...LocalData,...props.data}))
  //   // setUrl(props.data.Url);
  //   // setSelectdPath(data.SavePath);
  //   // setFilename(data.FileName);
  //   // setFileSize(data.File_Size);
  //   // console.log({"props.data":props.data});
  //   // console.log({"localdata":LocalData});

  //   if (theUrl.FileName) {
  //     console.log(data.FileName);
  //     let ext = data.FileName.split(".")[1];
  //     // console.log({ext:ext});
  //     // console.log({ ext: cat_selector(ext) });
  //     // setCategory(cat_selector(ext));
  //     setLocalData({ ...data, Catg: cat_selector(ext) });
  //   }
  // };

  async function getFileDetails(file_details) {
    // setshowAdd_Url(!showAdd_Url);
    // displayNewDownload(!newDownloadON);
    try {
      // const response = axios.head(url);
      const response = axios.post(
        "http://localhost:5001/prepare_download_file",
        file_details
      );
      response
        .then((rs) => {
          console.log({ response: rs.data });
          setLocalData({ ...rs.data });
        })
        .catch((error) => {
          console.log({ errr: error });
        });
    } catch (error) {
      console.error("Error:fin", error.message);
    }
  }

  // async function getFileDtailsFront(url) {
  //   // setshowAdd_Url(!showAdd_Url);
  //   // setnewDownloadON(!newDownloadON);
  //   // displayNewDownload(!newDownloadON);

  //   try {
  //     let newData = {
  //       id: "",
  //       Url: url,
  //       Status: true,
  //       Downloaded: 0,
  //       Speed: 256,
  //       Cmd_Option: "new",
  //       Catg: "UNKNOWN",
  //       Time_Left: 0,
  //       File_Size: 0,
  //       FileName: "",
  //       SavePath: "./",
  //       Resume: false,
  //     };
  //     const response1 = await axios.head(url);
  //     const contentDisposition = response1.headers["content-disposition"];
  //     newData["File_Size"] = parseInt(response1.headers["content-length"], 10);
  //     if (contentDisposition) {
  //       newData["FileName"] = contentDisposition.split("filename=")[0];
  //       // here define also download.html
  //     } else {
  //       newData["FileName"] = url.split("/").pop().trim();
  //     }
  //     let [file_name, ext] = newData["FileName"].split(".") || "download.html"

  //     newData["id"] = uuidv4();
  //     newData["Catg"] = cat_selector(ext);

  //     const response2 = await axios.get("http://localhost:5001/get_file_name", {
  //       params: {
  //         name: file_name,
  //         ext: ext,
  //       },
  //     });

  //     newData["FileName"] = response2.data;

  //     setLocalData({ ...newData, Catg: newData["Catg"] });
  //   } catch (error) {
  //     console.error("Error:fin", error.message);
  //   }

  // }

  useEffect(() => {
    if (theUrl) {
      // console.log(theUrl);
      // setLocalData({ ...data, Url: theUrl });
      // getFileDtailsFront(theUrl);
      setLocalData({ ...NewItem });
      // console.log(NewItem);
      // getFileDetails(LocalData);
      // afterOpenModal();
    }
  }, [theUrl,NewItem]);

  // useEffect(() => {
  //   if (LocalData.Url) {
  //     // getFileDetails(LocalData);
  //     getFileDtailsFront(LocalData.Url)
  //   }
  // }, [LocalData.Url]);

  const handleSavePath = (v) => {
    // console.log(`path set ${v}`);
    // data["SavePath"]=v;
    // setLocalData({...LocalData,'SavePath':v})
    // setSelectdPath("./")
  };

  const handleCategory = (v) => {
    // console.log(v);
    setLocalData({ ...LocalData, Catg: v });
    // setCategory(v);
    // data["Catg"]=v;
    // data['Catg']="dddddddd"
  };

  // const handleDirectoryChange = (event) => {
  //   const selectedFile = event.target.files[0];
  //   if (selectedFile.type === "directory") {
  //     setSelectdPath(selectedFile.path);
  //   }
  // };

  const handleCancel = () => {
    console.log("handleCancel pressed");
    handleClose();
  };

  const handleLater = () => {
    console.log(LocalData);
    setLocalData({ ...LocalData, Status: false });
    DownloadLater(LocalData);
    console.log("handleLater pressed to add to store and download it later");
  };
  

  const handleDownload = () => {
    // props.showProgresBox();
    // data={
    //   url
    //   selectdPath
    //   filename
    //   category
    //   fileSize
    // }

    // console.log({"props":props.data});
    // console.log({LocalData});

    // getFileDetails(LocalData);
    startProgress(LocalData);

    console.log("start download btn pressed");
  };

  return (
    <Modal size="lg" show={show} onHide={handleCancel}>
      <Container
        style={{ width: "500px", marginTop: "15em", background: "#b1b1b1" }}
      >
        {/* style={{ width: "fit-content" }} */}
        <div>
          <Row className="pb-3 pt-5 justify-content-center">
            <Form.Group xs={"9"} as={Col} controlId="urlInput">
              <Form.Control
                size="sm"
                value={LocalData.Url}
                type="text"
                placeholder="Enter URL"
                readOnly
                // onChange={() => setUrl}
              />
            </Form.Group>
            <Col xs={"auto"}>
              <CopyWrapper
                text={LocalData.Url}
                child={<Clipboard width="fit-content" />}
              />
            </Col>
          </Row>
          <Row className="pb-3 justify-content-center">
            <Form.Group xs={"9"} as={Col} controlId="fileOpener">
              <Form.Control
                size="sm"
                onChange={(e) => handleSavePath(e.target.value)}
                type="file"
                accept=".txt"
              />
            </Form.Group>
            <Col xs={"auto"}>
              <Save />
            </Col>
          </Row>
          <Row className="pb-3 justify-content-center">
            <Form.Group xs={"9"} as={Col} controlId="categorySelect">
              <Form.Select
                aria-label="category select"
                size="sm"
                value={LocalData.Catg}
                onChange={(e) => handleCategory(e.target.value)}
              >
                {Object.keys(CATEGORY_TYPES).map((key) => (
                  <option key={key} value={key}>
                    {key}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
            <Col xs={"auto"}>
              <PlusSquare />
            </Col>
          </Row>
        </div>
        <Row className="pb-3  justify-content-end align-items-center">
          <Form.Group xs={"auto"} as={Col} controlId="checkbox">
            <Form.Check
              type="checkbox"
              label="Remember path for this Category "
            />
          </Form.Group>
          <Col xs={"auto"} className="text-center">
            <Image width="55" src={fileIcon} alt="Image 1" />
            <div className="pt-3 pb-1">{LocalData.FileName} </div>
            <div>{LocalData.File_Size} </div>
          </Col>
        </Row>
        <Row className="pb-4 justify-content-end">
          <Col>
            <Button onClick={handleCancel} variant="primary">
              Cancel
            </Button>
          </Col>
          <Col>
            <Button onClick={handleLater} variant="secondary">
              Later
            </Button>
          </Col>
          <Col>
            <Button onClick={handleDownload} variant="success">
              Download
            </Button>
          </Col>
        </Row>
      </Container>
    </Modal>
  );
}

export default New_Download;
