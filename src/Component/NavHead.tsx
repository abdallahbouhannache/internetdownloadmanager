import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import Button from "react-bootstrap/Button";
import { useState } from "react";
import Image from "react-bootstrap/Image";
import Play from "../assets/play-button.png";
import logo from "../assets/download.gif";
import Add from "../assets/add-file.png";
import Stop from "../assets/stop (1).png";
import Recyle from "../assets/waste.png";
import axios from "axios";
import {
  useIdmRequests,
  useProgresID,
  useWindowsStore,
} from "../zustand/useAppState";
import { IdmReq } from "../Utils/DownLoad_Action";
import { useStore } from "zustand";

const style = {
  btn: {
    padding: "5px 12px",
    display: "flex",
    alignItems: "center",
  },
  pic: { width: "1rem", marginLeft: "12px" },
};

function NavHead() {
  // const defaultDownload = {
  //   new_url: "",
  //   savePath: "./downloads/",
  //   name_file: "",
  //   catg: "UNKNOWN",
  //   size: 0,
  //   speed_limit: 256,
  //   command_option: "new",
  //   downloaded: 0,
  //   Resume: "false",
  // };

  const {
    displayProgress,
    progressON,
    addUrlON,
    displayAddUrl,
    displayNewDownload,
    newDownloadON,
  } = useStore(useWindowsStore);

  const { CurrentRow, SetCurrentRow } = useIdmRequests((state) => state);
  const idmR = IdmReq();
  const { progresID, setprogresID } = useProgresID();

  // const [nwDownload, setNewDownload] = useState(defaultDownload);

  // async function getFileDetails(url) {
  //   displayNewDownload(!newDownloadON);
  //   try {
  //     const response = axios.head(url);
  //     response
  //       .then((rs) => {
  //         let newData = {
  //           new_url: url,
  //           savePath: "./",
  //           name_file: "",
  //           catg: "UNKNOWN",
  //           size: 0,
  //           speed_limit: 256,
  //           command_option: "new",
  //           downloaded: 0,
  //           Resume: "false",
  //         };
  //         newData["name_file"] = url.split("/").pop();
  //         newData["size"] = rs.headers["content-length"];

  //         // setNewDownload(newData);
  //       })
  //       .catch((error) => {
  //         console.log({ errr: error });
  //       });
  //   } catch (error) {
  //     console.error("Error:fin", error.message);
  //   }
  // }

  const handleAddClick = () => {
    displayAddUrl(!addUrlON);
    // console.log("open download");
  };

  const handleContinueClick = () => {
    const par = {};
    par["rows"] = [CurrentRow];
    if (CurrentRow) {
      // console.log(CurrentRow);
      par["rows"].length == 1 && displayProgress(!progressON);
      let data = {
        id: par["rows"][0].id ||  "",
        FileName:par["rows"][0].FileName ||  "",
      };
      setprogresID(data);
      // console.log(data);
      // console.log(progresID);
      // console.log({par});
      
      idmR.ContinueItems(par)
    }
    // console.log("continue clicked");
  };

  const handleStopClick = () => {
    // console.log(CurrentRow);
    const par = {};
    par["rows"] = [CurrentRow];
    if (CurrentRow) {
      idmR.StopItems(par);
    }
    // console.log("stop clicked");
  };

  const handleRemoveItems = () => {
    const par = {};
    par["rows"] = [CurrentRow];
    if (CurrentRow) {
      idmR.DelItems(par);
    }
    // console.log("selected item has been removed");
  };

  const handleDelAll = () => {
    const par = {};
    par["all"] = true;
    idmR.DelItems(par);
    // console.log("all items has been removed");
  };

  return (
    <>
      <Navbar className="bg-body-tertiary" bg="light" data-bs-theme="light">
        <Container>
          <Navbar.Brand href="#home">Download Manager</Navbar.Brand>
          {/* <img src={logo} alt="Description of the GIF" /> */}
          <Image src={logo} style={{ width: "1rem" }} />

          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="#home">File</Nav.Link>
              <Nav.Link href="#link">Download</Nav.Link>
              <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                <NavDropdown.Item href="#action/3.1">Options</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">View</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.3">speed</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item href="#action/3.4">All</NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <Navbar className="bg-body-tertiary">
        <Container>
          <Button
            onClick={handleAddClick}
            variant="outline-primary"
            style={style.btn}
          >
            <span>Add</span>
            <Image src={Add} style={style.pic} />
          </Button>
          <Button
            onClick={handleContinueClick}
            variant="outline-success"
            style={style.btn}
          >
            <span>Continue</span>
            <Image src={Play} style={style.pic} />
          </Button>
          <Button
            onClick={handleStopClick}
            variant="outline-danger"
            style={style.btn}
          >
            <span>Stop</span>
            <Image src={Stop} style={style.pic} />
          </Button>
          <Button
            onClick={handleRemoveItems}
            variant="outline-warning"
            style={style.btn}
          >
            <span>Remove</span>
            <Image src={Recyle} style={style.pic} />
          </Button>
          <Button
            onClick={handleDelAll}
            variant="outline-warning"
            style={style.btn}
          >
            <span>Del/all</span>
            <Image src={Recyle} style={style.pic} />
          </Button>
        </Container>
      </Navbar>
    </>
  );
}

export default NavHead;
