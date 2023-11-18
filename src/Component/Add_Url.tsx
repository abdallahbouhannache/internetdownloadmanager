import React, { useState } from "react";
import { Button, Form, InputGroup, Modal } from "react-bootstrap";

function Add_Url({ url, show, handleClose, openNewDownload }) {
  // const [newUrl, setNewUrl] = useState(url);
  const [newUrl, setNewUrl] = useState(
    "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-623.exe"
  );

  const isUrl = (e) => {
    return true;
  };
  return (
    <>
      {/* <Button variant="primary" onClick={handleShow}>
        Launch Confirmation Modal
      </Button> */}

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Confirmation</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <InputGroup className="mb-3">
            <InputGroup.Text id="basic-addon1">@</InputGroup.Text>
            <Form.Control
              size="sm"
              value={newUrl}
              type="text"
              placeholder="Enter URL"
              onChange={(e) => setNewUrl(e.target.value)}
            />
          </InputGroup>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="outline-dark"
            onClick={() => {
              if (isUrl(newUrl)) {
                handleClose();
                openNewDownload(newUrl);
                console.log("Confirmed!");
              }
              // Add your confirmation action here
            }}
          >
            ok
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default Add_Url;
