import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useState } from "react";
import Image from "react-bootstrap/Image";

import logo from "../assets/download.gif";
import Add from "../assets/add-file.png";
import Stop from "../assets/stop (1).png";
import Recyle from "../assets/waste.png";
import Play from "../assets/play-button.png";

const style = {
  btn: {
    padding: "5px 12px",
    display: "flex",
    alignItems: "center",
  },
  pic: { width: "1rem", marginLeft: "12px" },
};
function NavHead() {
  const [searchTerm, setSearchTerm] = useState("");
  const handleFilterClick = () => {
    // Perform filtering logic here based on searchTerm, filter1, and filter2
    // Update the table data accordingly
  };

  return (
    <>
      <Navbar className="bg-body-tertiary" bg="light" data-bs-theme="light">
        <Container>
          <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
          {/* <img src={logo} alt="Description of the GIF" /> */}
          <Image src={logo} style={{ width: "1rem" }} />

          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="#home">File</Nav.Link>
              <Nav.Link href="#link">Download</Nav.Link>
              <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                <NavDropdown.Item href="#action/3.1">Options</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">
                  View
                </NavDropdown.Item>
                <NavDropdown.Item href="#action/3.3">
                  speed
                </NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item href="#action/3.4">
                  All
                </NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <Navbar className="bg-body-tertiary">
        <Container>
          <Button  variant="outline-primary" style={style.btn}>
            <span>Add</span>
            <Image src={Add} style={style.pic} />
          </Button>
          <Button variant="outline-success" style={style.btn}>
            <span>Continue</span>
            <Image src={Play} style={style.pic} />
          </Button>
          <Button variant="outline-danger" style={style.btn}>
            <span>Stop</span>
            <Image src={Stop} style={style.pic} />
          </Button>
          <Button variant="outline-warning" style={style.btn}>
            <span>Remove</span>
            <Image src={Recyle} style={style.pic} />
          </Button>
          <Button variant="outline-warning" style={style.btn}>
            <span>Del/all</span>
            <Image src={Recyle} style={style.pic} />
          </Button>
        </Container>
      </Navbar>
    </>
  );
}

export default NavHead;
