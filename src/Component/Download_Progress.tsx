import React, { useState } from "react";
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
import { Clipboard } from "react-bootstrap-icons";
import BootstrapTable from "react-bootstrap-table-next";
import { CSSTransition } from "react-transition-group";
import "../Style/Download_Progress.css";

function Download_Progress() {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [activeTab, setActiveTab] = useState("Download");

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  const DownloadContent = {
    status: "Get",
    File_Size: "10mb",
    Speed: "145kb",
    Downloaded: "5.78mb",
    Time_Left: "1min 25sec",
    Resume: "True",
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

  const handleToggle = () => {
    setshowContent(!showContent);
  };

  return (
    <>
      <Button variant="primary" onClick={handleShow}>
        Launch Modal
      </Button>

      <Modal size="lg" show={show} onHide={handleClose}>
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
                          defaultValue="https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-623.exe"
                          placeholder="URL"
                          plaintext
                          readOnly
                        />
                      </Form.Group>
                      <Col xs={"auto"}>
                        <Clipboard width="fit-content" />
                      </Col>
                    </Row>
                    {Object.entries(DownloadContent).map(([key, value]) => (
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
                            defaultValue={value}
                            placeholder={key}
                            plaintext
                            readOnly
                          />
                        </Col>
                      </Form.Group>
                    ))}
                    <ProgressBar now={60} label={`${60}%`} striped animated />

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
