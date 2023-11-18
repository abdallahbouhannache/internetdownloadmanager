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
import { useStore } from "zustand";
import useAppState, { useDownloadItem } from "../zustand/useAppState";
import {
  InitSocketSession,
  Follow_Progress_Item,
  Follow_Progress_bundle,
  Dowload_Actions,
} from "../Utils/DownLoad_Action";

function Download_Progress({ progresID, handleClose, show }) {
  // const [show, setShow] = useState(false);
  // const handleClose = () => setShow(false);
  // const handleShow = () => setShow(true);
  const [activeTab, setActiveTab] = useState("Download");

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  var DownloadContent = {
    FileName: "",
    Status: "Get",
    File_Size: "25315364",
    Speed: "145",
    Downloaded: "5156235",
    Time_Left: "62536125",
    Resume: "true",
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
  // const [downloadProgress, setDownloadContent] = useState(DownloadContent);
  const [new_url, setNew_Url] = useState("");
  const [progesX, setProgresX] = useState(0);

  const handleToggle = () => {
    setshowContent(!showContent);
  };

  const [fileContent, setfileContent] = useState("");
  const [theFile, settheFile] = useState(null);
  const [messages, setMessages] = useState([]);
  // const { addDownload, initDownloads, downloads } = useStore(useAppState);
  const { addDownload, initDownloads, downloads } = useAppState();

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

  const downloadActions = Dowload_Actions();
  var downloadProgress = progresID || {};
  // var { id, name } = progresID;
  // console.log(progresID);

  useEffect(() => {

    // let { id, name, ...rest } = progresID;
    console.log({ progresID: progresID });

    // downloadProgress = downloadActions.useDownloadItem(id, name);
    // console.log({ downloadItem: downloadProgress });

    // console.log({ downloads: downloads });
    // console.log({ progresID: progresID });
    // InitSocketSession(socket);
    // Follow_Progress_Item(socket);
    // Follow_Progress_bundle();
  }, [downloads]);

  // useEffect(() => {
  //   console.log({ progresID: progresID });
  // }, [progresID]);

  return (
    <>
      <Modal size="lg" show={show} className="visible" onHide={handleClose}>
        {/* <Button variant="primary" onClick={sendMessage}>
          send MSG
        </Button> */}
        {/* {fileContent} */}
        {messages}
        <Modal.Header closeButton>
          <Modal.Title>Downloading</Modal.Title>
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
