import React, { useState } from "react";
import { Button, Form, InputGroup, Modal } from "react-bootstrap";

export default function Add_Url() {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  return (
    <>
      <Button variant="primary" onClick={handleShow}>
        Launch Confirmation Modal
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Confirmation</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <InputGroup className="mb-3">
              <InputGroup.Text id="basic-addon1">@</InputGroup.Text>
              <Form.Control
                size="sm"
                placeholder="Username"
                aria-label="Username"
                aria-describedby="basic-addon1"
              />
            </InputGroup>
          
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="outline-dark"
            onClick={() => {
              handleClose();
              // Add your confirmation action here
              console.log("Confirmed!");
            }}>
            ok
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
