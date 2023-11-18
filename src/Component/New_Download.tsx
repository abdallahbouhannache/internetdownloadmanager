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
// import { useFilePicker } from "use-file-picker";

function New_Download(props) {
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

  // @ts-ignore
  const cat_selector = (ext:string) => {

    let category = Object.entries(CATEGORY_TYPES).find(([key, value]) => {
      const fileInfoAny = value as any ; // Type assertion to 'any'
      return fileInfoAny.includes(ext);
    });
    return category ? category[0] : "UNKNOWN";
  };

  const [LocalData, setLocalData] = useState(data);

  // const [url, setUrl] = useState(data.Url);
  // const [selectdPath, setSelectdPath] = useState(data.SavePath);
  // const [filename, setFilename] = useState(data.FileName);
  // const [category, setCategory] = useState(data.Catg);
  // const [fileSize, setFileSize] = useState(data.File_Size);

  const afterOpenModal = () => {
    // data = props.data;
    // setLocalData(e=>({...e,...props.data}))
    // setLocalData(e=>({...LocalData,...props.data}))

    // setUrl(props.data.Url);
    // setSelectdPath(data.SavePath);
    // setFilename(data.FileName);
    // setFileSize(data.File_Size);
    // console.log({"props.data":props.data});
    // console.log({"localdata":LocalData});
    if (props.data.FileName) {
      console.log(props.data.FileName);
      let ext = props.data.FileName.split(".")[1];
      // console.log({ext:ext});
      // console.log({ ext: cat_selector(ext) });
      // setCategory(cat_selector(ext));
      setLocalData({ ...props.data, Catg: cat_selector(ext) });
    }

  };

  useEffect(() => {
    console.log("changed data");
    if (props.data) {
      afterOpenModal();
    }
  }, [props.data]);

  // useEffect(() => {
  //   console.log({ localdata: LocalData });
  // }, [LocalData]);

  const handleSavePath = (v) => {
    console.log(`path set ${v}`);
    // data["SavePath"]=v;
    // setLocalData({...LocalData,'SavePath':v})
    // setSelectdPath("./")
  };

  const handleCategory = (v) => {
    console.log(v);
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
    props.handleClose();
  };

  const handleLater = () => {
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

    props.startProgress(LocalData);
    console.log("start download btn pressed");
  };

  return (
    <Modal size="lg" show={props.show} onHide={handleCancel}>
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
