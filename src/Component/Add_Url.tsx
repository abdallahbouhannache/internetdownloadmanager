import React, { useEffect, useState } from "react";
import { Button, Form, InputGroup, Modal } from "react-bootstrap";
import { Bounce, Slide, toast } from "react-toastify";
import swal from "sweetalert";
const isUrl = (url) => {
  try {
    // Regular expression to match URLs
    // const urlRegex =
      // /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    let message = "";
    if (!url || typeof url !== "string") {
      message = "URL cannot be empty";
      return false; // Check if the URL is empty
    }
    url = url.trim();

    // Specific requirements for your IDM
    const checks = {
      hasProtocol: /^(https?:\/\/)/i.test(url),
      hasValidDomain: /[\w-]+(\.[\w-]+)+/.test(url),
      maxLength: url.length <= 2048, // Typical URL length limit
      noSpaces: !/\s/.test(url),
      validChars: /^[-A-Za-z0-9+&@#/%?=~_|!:,.;]*$/.test(url.split('/').slice(3).join('/'))
    };

    switch (true) {
      case !checks.hasProtocol:
        return { isValid: false, message: 'URL must include http:// or https://' };
      
      case !checks.hasValidDomain:
        return { isValid: false, message: 'Invalid domain format' };
      
      case !checks.maxLength:
        return { isValid: false, message: 'URL too long (max 2048 characters)' };
      
      case !checks.noSpaces:
        return { isValid: false, message: 'URL cannot contain spaces' };
      
      case !checks.validChars:
        return { isValid: false, message: 'URL contains invalid characters' };
      
      default:
        const urlObj = new URL(url);
        return {
          isValid: true,
          message: 'Valid URL',
          formattedUrl: urlObj.href,
          details: {
            protocol: urlObj.protocol,
            hostname: urlObj.hostname,
            pathname: urlObj.pathname
          }
        };
    }
    // return urlRegex.test(url); // Test the URL against the regex
  } catch (error) {
    return {
      isValid: false,
      message: 'Invalid URL: ' + error.message
    }
  }
};

function Add_Url({ show, handleClose, openNewDownload }) {
  const [newUrl, setNewUrl] = useState("");
  const [validationResult, setValidationResult] = useState(null);

  const begin = () => {
    const result = isUrl(newUrl)
    setValidationResult(result);
  };

  useEffect(() => {
      if (validationResult) { // Check if validationResult is not null   
        if (validationResult.isValid) {
          handleClose();
          openNewDownload(newUrl);
        } else {
          toast(validationResult.message , {
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
    }
  }, [validationResult]);

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
