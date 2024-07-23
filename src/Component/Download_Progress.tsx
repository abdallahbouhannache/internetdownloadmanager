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
import useAppState, { useProgresID } from "../zustand/useAppState";
import { formatFileSize } from "../Utils/tools";
import { IdmReq } from "../Utils/DownLoad_Action";

function Download_Progress({ dwAct, handleClose, show }) {
  const idmR = IdmReq();
  const { progresID } = useProgresID();
  const [activeTab, setActiveTab] = useState("Download");

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  var DownloadData = {
    // id: "",
    Url: "",
    Status: false,
    Downloaded: 0,
    Speed: 256,
    Cmd_Option: "new",
    Catg: "UNKNOWN",
    Time_Left: 0,
    File_Size: 0,
    FileName: "",
    SavePath: "./downloads/",
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

  const handleStopContinue = () => {
    let rows = [downloadProgress];

    if (downloadProgress["Status"]) {
      idmR.StopItems({ rows });
    } else {
      idmR.ContinueItems({ rows });
    }
  };

  useEffect(() => {
    if (progresID.FileName !== "") {
      const dp = dwAct.useDownloadItem(progresID.id, progresID.FileName);

      // downloads[progresID.FileName];
      const { id, ...restOfDownProgress } = dp; // Destructure and exclude the 'id' property
      setDownloadContent(restOfDownProgress);
    }
  }, [downloads[progresID.FileName]]);

  return (
    <>
      <Modal size="lg" show={show} className="visible" onHide={handleClose}>
        {messages}
        <Modal.Header closeButton>
          <Modal.Title>
            Downloading
            {formatFileSize(downloadProgress["Downloaded"])}
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
                    <Row className=" justify-content-start mb-3 row" >
                      <Form.Label column sm="4">
                        {"URL"}:
                      </Form.Label>
                      <Form.Group xs={"6"}  as={Col} controlId="urlInput">
                        <Form.Control
                          size="sm"
                          type="text"
                          value={downloadProgress["Url"]}
                          placeholder="URL"
                          plaintext
                          readOnly
                        />
                      </Form.Group>
                      <Col xs={"auto"}>
                        <CopyWrapper
                          text={downloadProgress["Url"]}
                          child={<Clipboard width="fit-content" />}
                        />
                        {/* <Clipboard width="fit-content" /> */}
                      </Col>
                    </Row>
                    {Object.entries(downloadProgress).map(([key, v]) => (
                      <React.Fragment key={key}>
                        {key !== "Url" && (
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
                                // value={String(
                                //   key === ("Downloaded" || "Speed" || "File_Size")
                                //     ? formatFileSize(v)
                                //     : v
                                // )}
                                value={String(
                                  ["Downloaded", "Speed", "File_Size"].includes(
                                    key
                                  )
                                    ? formatFileSize(v)
                                    : v
                                )}
                                placeholder={key}
                                plaintext
                                readOnly
                              />
                            </Col>
                          </Form.Group>
                        )}
                      </React.Fragment>
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
          <Button onClick={handleStopContinue} variant="outline-dark">
            {downloadProgress["Status"] ? "Pause" : "Continue"}
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
