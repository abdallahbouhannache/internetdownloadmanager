import React, { useState } from "react";
import { Button, Form, InputGroup, Modal } from "react-bootstrap";
import swal from "sweetalert";
import { Bounce, Slide, toast } from "react-toastify";

function Add_Url({ show, handleClose, openNewDownload }) {
  const [newUrl, setNewUrl] = useState("");

  // Regular expression to match URLs
  const urlRegex = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;

  const isUrl = (url) => {
    if (!url) return false; // Check if the URL is empty
    return urlRegex.test(url); // Test the URL against the regex
  };

  const begin = () => {
    if (isUrl(newUrl)) {
      handleClose();
      openNewDownload(newUrl);
    }else{
      toast("Url Format Incorrect", {
        position: "top-center",
        autoClose: 500,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "light",
        transition: Bounce,
      });
    }
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
          <Button variant="outline-dark" onClick={begin}>
            ok
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default Add_Url;
