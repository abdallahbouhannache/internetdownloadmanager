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
import useAppState from "../zustand/useAppState";

function Download_Progress({ dwAct, progresID, handleClose, show }) {
  const [activeTab, setActiveTab] = useState("Download");
  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

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

  
  const [messages, setMessages] = useState([]);
  const { downloads } = useAppState();

  useEffect(() => {
    // const dp =dwAct.useDownloadItem(progresID.id, progresID.FileName);
    // setDownloadContent(dp);

  }, [downloads[progresID.FileName]]);

  return (
    <>
      <Modal size="lg" show={show} className="visible" onHide={handleClose}>
        
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
