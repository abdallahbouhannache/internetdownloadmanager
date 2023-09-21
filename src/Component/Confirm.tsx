import React from "react";
import { Button, Card, Image } from "react-bootstrap";
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
// import { faIconName } from '@fortawesome/free-solid-svg-icons';
import Warn from "../assets/Danger.svg";

const Confirm = ({
  message = "Do you want to Confirm",
  subMsg = "confirm the operation",
}) => {
  return (
    <Card
      className="shadow-sm p-3 mb-5 bg-body rounded"
      style={{ width: "30em" }}
    >
      <Card.Body>
        <Card.Title className="m-0 d-flex justify-content-around align-items-center">
          {message} ?
          <Image src={Warn} alt="Image 1" />
        </Card.Title>
        <p className="fw-light text-start ms-5">
            {subMsg}
        </p>

        <div className="d-flex flex-row justify-content-around">
          <Button variant="outline-secondary">
            <span>Discard</span>
          </Button>
          <Button variant="outline-danger">
            <span>Confirm</span>
          </Button>
        </div>

      </Card.Body>
    </Card>
  );
};

export default Confirm;
