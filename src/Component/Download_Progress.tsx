import React, { useEffect, useRef, useState } from "react";
import {
  Button,
  Col,
  Container,
  Form,
  Modal,
  Row,
  Tab,
  Tabs,
  ProgressBar,
  Collapse,
} from "react-bootstrap";
import { Clipboard, Percent } from "react-bootstrap-icons";
import BootstrapTable from "react-bootstrap-table-next";
import { CSSTransition } from "react-transition-group";
import "../Style/Download_Progress.css";
import CopyWrapper from "./copyClipBoard";
import io from "socket.io-client";
import axios from "axios";
// import { useStore } from "zustand";
import useAppState from "../zustand/useAppState";

// import {
//   InitSocketSession,
//   Follow_Progress_Item,
//   Follow_Progress_bundle,
//   Dowload_Actions,
// } from "../Utils/DownLoad_Action";

function Download_Progress({ dwAct, progresID, handleClose, show }) {
  // const [show, setShow] = useState(false);
  // const handleClose = () => setShow(false);
  // const handleShow = () => setShow(true);
  const [activeTab, setActiveTab] = useState("Download");

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  // var DownloadContent = {
  //   FileName: "",
  //   Status: "Get",
  //   File_Size: "25315364",
  //   Speed: "145",
  //   Downloaded: "5156235",
  //   Time_Left: "62536125",
  //   Resume: "true",
  // };

  var DownloadData = {
    id: "",
    Url: "",
    Status: false,
    // Status: "pending",
    Downloaded: 0,
    Speed: 256,
    Cmd_Option: "new",
    Catg: "UNKNOWN",
    Time_Left: 0,
    File_Size: 0,
    // FileName: "",
    SavePath: "./",
    Resume: false,
  };

  const data = [
    { N_Part: 1, Downloaded: "362kb", Status: "finished" },
    { N_Part: 2, Downloaded: "150kb", Status: "Downloading" },
    // ... other data
  ];

  const columns = [
    { dataField: "N_Part", text: "N°Part" },
    { dataField: "Downloaded", text: "Downloaded" },
    { dataField: "Status", text: "Status" },
  ];

  const [showContent, setshowContent] = useState(false);
  const [downloadProgress, setDownloadContent] = useState(DownloadData);
  const [new_url, setNew_Url] = useState("");
  const [progesX, setProgresX] = useState(0);

  const handleToggle = () => {
    setshowContent(!showContent);
  };

  const [fileContent, setfileContent] = useState("");
  const [theFile, settheFile] = useState(null);
  const [messages, setMessages] = useState([]);
  // const { addDownload, initDownloads, downloads } = useStore(useAppState);
  const { downloads } = useAppState();

  // useEffect(() => {
  //   let {
  //     FileName,
  //     Status,
  //     Speed,
  //     Finished,
  //     File_Size,
  //     Downloaded,
  //     Time_Left,
  //     Resume,
  //     url,
  //   } = item;

  //   DownloadContent = {
  //     FileName,
  //     Status,
  //     Speed,
  //     File_Size,
  //     Downloaded,
  //     Time_Left,
  //     Resume,
  //   };
  //   // const perCent = ((Downloaded / File_Size) * 100).toFixed(2);
  //   const perCent = Math.round((Downloaded / File_Size) * 100);
  //   setNew_Url(url);
  //   setProgresX(perCent);

  //   setDownloadContent(DownloadContent);
  //   // return () => {
  //   // }
  // }, [progresID,item]);

  // const socket = useRef(null);
  // const socketUrl = "http://localhost:5001";
  // socket.current = io(socketUrl, {
  //   autoConnect: false,
  // });
  // const downloadActions = Dowload_Actions();
  // downloadActions.StartSessions(socket);

  // const downloadActions = Dowload_Actions();
  // var downloadProgress = {};
  // var { id, FileName,...rest } = progresID;
  // console.log(progresID);

  // useEffect(() => {
  //   // let { id, name, ...rest } = progresID;
  //   console.log({ progresID: progresID });
  //   console.log("refreshing display");
  //   if(FileName){
  //     console.log("refreshing display inside");
  //     downloadProgress = downloadActions.useDownloadItem(id, FileName);
  //   }
  //   // console.log({ downloadItem: downloadProgress });
  //   // console.log({ downloads: downloads });
  //   // console.log({ progresID: progresID });
  //   // InitSocketSession(socket);
  //   // Follow_Progress_Item(socket);
  //   // Follow_Progress_bundle();
  // }, [downloads]);

  // useEffect(() => {
  //   // console.log({ progresID: progresID });
  //   console.log(progresID["Status"]);
  //   if (progresID["Status"]) {
  //     console.log("setting downloadProgress display");
  //     // console.log({ progresID: progresID });
  //     // console.log({ downloadProgress: downloadProgress });
  //     // var downloadProgress = progresID || DownloadData;
  //     setTimeout(() => {
  //       let dp = dwAct.useDownloadItem(progresID.id, progresID.FileName);
  //       setDownloadContent(dp);
  //       console.log(dp);
  //     }, 5000);
  //     console.log(downloadProgress);
  //     // var { id, FileName,...rest } = downloadProgress;
  //   }
  // }, []);

  // useEffect(() => {

  //   if (progresID["Status"]) {
  //     downloadProgress =dwAct.useDownloadItem(progresID.id, progresID.FileName);
  //     // let dp = dwAct.useDownloadItem(progresID.id, progresID.FileName);
  //     // if(dp){
  //     //   dwAct.useDownloadItem(progresID.id, progresID.FileName);
  //     //   // setDownloadContent(dp);
  //     // }
  //     console.log({downloadProgress});

  //   }
  // }, [progresID]);

  // console.log({progresID});
  // console.log({downloadProgress});
  
  // setTimeout(() => {
  //   const dp =dwAct.useDownloadItem(progresID.id, progresID.FileName);
  //   setDownloadContent(dp);

  // }, 10000);

  
  useEffect(() => {
    // console.log(progresID);
    // setTimeout(() => {
      // }, 10000);
    const dp =dwAct.useDownloadItem(progresID.id, progresID.FileName);
    setDownloadContent(dp);

    // console.log(downloadProgress)
    // var dp = dwAct.useDownloadItem(progresID.id, progresID.FileName);
    // setDownloadContent(dp);
    // console.log(downloadProgress)
  }, [downloads[progresID.FileName]]);

  // downloads[progresID.FileName]

  // progresID.FileName
  // myDictionary.hasOwnProperty('myKey')
  // console.log(downloads[progresID.FileName]);
  // console.log(downloadProgress);
  
  // return (
  //   <>
  //     {progresID.FileName && downloadProgress["Status"]
  //       ? downloadProgress["Downloaded"]
  //       : "Loading"}
  //   </>
  // );

  // if (!downloadProgress["Status"]) {
  // }

  return (
    <>
      <Modal size="lg" show={show} className="visible" onHide={handleClose}>
        {/* <Button variant="primary" onClick={sendMessage}>
          send MSG
        </Button> */}
        {/* {fileContent} */}
        {messages}
        <Modal.Header closeButton>
          <Modal.Title>
            Downloading
            {downloadProgress["Downloaded"]}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Tabs activeKey={activeTab} onSelect={handleTabChange}>
            {/* defaultActiveKey="Download" id="uncontrolled-tab-example" */}
            <Tab eventKey="Download" title="Download">
              <CSSTransition
                in={activeTab === "Download"}
                timeout={300}
                classNames="tab-transition"
                unmountOnExit
              >
                <div className="tab-content">
                  <Container>
                    <Row className=" justify-content-start">
                      <Form.Group xs={"9"} as={Col} controlId="urlInput">
                        <Form.Control
                          size="sm"
                          type="text"
                          value={new_url}
                          placeholder="URL"
                          plaintext
                          readOnly
                        />
                      </Form.Group>
                      <Col xs={"auto"}>
                        <CopyWrapper
                          text={new_url}
                          child={<Clipboard width="fit-content" />}
                        />
                        {/* <Clipboard width="fit-content" /> */}
                      </Col>
                    </Row>
                    {Object.entries(downloadProgress).map(([key, value]) => (
                      <Form.Group
                        key={key}
                        as={Row}
                        className="mb-3"
                        controlId="formPlaintextEmail"
                      >
                        <Form.Label column sm="4">
                          {key}:
                        </Form.Label>
                        <Col sm="8">
                          <Form.Control
                            size="sm"
                            type="text"
                            // defaultValue={value}
                            value={String(value)}
                            placeholder={key}
                            plaintext
                            readOnly
                          />
                        </Col>
                      </Form.Group>
                    ))}

                    <ProgressBar
                      now={progesX}
                      label={`${progesX}%`}
                      striped
                      animated
                    />

                    <Collapse in={showContent}>
                      <div id="example-collapse-text">
                        <Row>
                          <BootstrapTable
                            keyField="id"
                            data={data}
                            columns={columns}
                            bordered={false}
                          />
                        </Row>
                      </div>
                    </Collapse>
                  </Container>
                </div>
              </CSSTransition>
            </Tab>
            <Tab eventKey="Speed" title="Speed">
              <CSSTransition
                in={activeTab === "Speed"}
                timeout={300}
                classNames="tab-transition"
                unmountOnExit
              >
                <div className="tab-content">
                  <p>Speed</p>
                </div>
              </CSSTransition>
            </Tab>
            <Tab eventKey="contact" title="Contact">
              <CSSTransition
                in={activeTab === "contact"}
                timeout={300}
                classNames="tab-transition"
                unmountOnExit
              >
                <div className="tab-content">
                  <p>Other</p>
                </div>
              </CSSTransition>
            </Tab>
          </Tabs>
        </Modal.Body>
        <Modal.Footer className="justify-content-evenly">
          <Button onClick={handleClose} variant="outline-warning">
            Cancel
          </Button>
          <Button onClick={handleClose} variant="outline-dark">
            Pause
          </Button>
          <Button onClick={handleToggle} variant="outline-secondary">
            {showContent ? "Hide" : "Show"}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default Download_Progress;
