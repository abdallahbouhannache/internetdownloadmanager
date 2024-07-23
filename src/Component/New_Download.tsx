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
import { useIdmRequests } from "../zustand/useAppState";



function New_Download({
  theUrl,
  show,
  DownloadLater,
  startProgress,
  handleClose,
}) {
  const idmR = IdmReq();
  // the store manager
  const { NewItem, CreateReq } = useIdmRequests();

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
    SavePath: "./downloads/",
    Resume: true,
  };

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

  const [LocalData, setLocalData] = useState(data);

  useEffect(() => {
    if (theUrl) {
      setLocalData({ ...NewItem });
    }
  }, [theUrl, NewItem]);

  const handleSavePath = async (v) => {
    // console.log(`path set ${v}`);
    // data["SavePath"]=v;
    // setLocalData({...LocalData,'SavePath':v})
    // setSelectdPath("./")
    console.log("handleSavePath");
    try {
      const dirHandle = await window.showDirectoryPicker();
      
      setLocalData({ ...LocalData, SavePath: dirHandle.name });
      // document.getElementById('fileOpener').value = dirHandle.name; // Display directory name
    } catch (err) {
      console.error("Failed to access directory:", err);
    }
  };

  const handleCategory = (v) => {
    setLocalData({ ...LocalData, Catg: v });
  };

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
          <Row className=" align-items-center justify-content-center pb-3 row">
            {/* <Form.Group className="mb-3" xs={"9"} as={Col} >
              <InputGroup.Text id="basic-addon1" onClick={()=>alert("sss")}
              onChange={(e) => handleSavePath(e.target.value)}>
              Select path
              </InputGroup.Text>
              <Form.Control
                  size="sm"
                  onChange={(e) => handleSavePath(e.target.value)}
                  type="text"
                />
            </Form.Group> */}

            {/* <Form.Group xs={"9"} as={Col} controlId="fileOpener">
              <InputGroup.Text id="basic-addon1" onClick={()=>alert("sss")}
                onChange={(e) => handleSavePath(e.target.value)}>
                Select path
              </InputGroup.Text>
              <Form.Control
                size="sm"
                onChange={(e) => handleSavePath(e.target.value)}
                type="text"
              />
            </Form.Group>
            <Col xs={"auto"}>
              <Save />
            </Col> */}
            <Col xs={"auto"} className="m-0 p-0">
              <Button className="" onClick={(v) => handleSavePath(v)}>
                Browse
              </Button>
            </Col>
            <Form.Group className=" m-0 p-0" xs={"7"} as={Col}>
              {/* controlId="fileOpener" */}
              <Form.Control
                as={Col}
                size="sm"
                value={LocalData.SavePath}
                type="text"
                id="fileOpener" // Ensure this ID matches the getElementById call in selectDirectory
              >
                {LocalData.SavePath}
              </Form.Control>
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
