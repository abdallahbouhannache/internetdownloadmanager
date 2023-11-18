import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useState } from "react";
import Image from "react-bootstrap/Image";
import New_Download from "./New_Download";
import Add_Url from "./Add_Url";
import Download_Progress from "./Download_Progress";
import logo from "../assets/download.gif";
import Add from "../assets/add-file.png";
import Stop from "../assets/stop (1).png";
import Recyle from "../assets/waste.png";
import Play from "../assets/play-button.png";
import io from "socket.io-client";
import axios from "axios";
import { CATEGORY_TYPES } from "../Constant/Constant";
import useAppState, { useWindowsStore } from "../zustand/useAppState";
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
  const defaultDownload = {
    new_url: "",
    savePath: "./",
    name_file: "",
    catg: "UNKNOWN",
    size: 0,
    speed_limit: 256,
    command_option: "new",
    downloaded: 0,
    Resume: "false",
  };

  const {
    displayProgress,
    progressON,
    addUrlON,
    displayAddUrl,
    displayNewDownload,
    newDownloadON,
  } = useStore(useWindowsStore);
  const { fname } = useAppState();

  const [searchTerm, setSearchTerm] = useState("");
  // const [newDownloadON, displayNewDownload] = useState(false);
  // const [showProgress, setshowProgress] = useState(false);
  // const [showAdd_Url, setshowAdd_Url] = useState(false);
  const [nwDownload, setNewDownload] = useState(defaultDownload);
  const handleClose = () => displayProgress(false);
  const Close_New_Down = () => displayNewDownload(false);
  const Close_Add_url = () => displayAddUrl(false);

  // var socket=null;
  // const response =  fetch(
  //   url,
  //   {
  //     method: "GET",
  //     mode: "no-cors",
  //     credentials: 'same-origin',
  //   },
  // );
  // const instance = axios.create({
  //   headers: {
  //     method: "GET",
  //     mode: "no-cors",
  //     "Access-Control-Allow-Origin": "*",
  //     // "Content-Type": "application/json",
  //     credentials: 'same-origin',
  //     withCredentials: true,
  //   },
  // });
  // const res = instance.get(url);

  // const inst = axios.create({
  //   withCredentials: true,
  //   headers: {
  //     mode: "no-cors",
  //     'Access-Control-Allow-Origin' : '*',
  //     'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
  //     }
  // });

  async function getFileDetails(url) {
    // setshowAdd_Url(!showAdd_Url);
    // setnewDownloadON(!newDownloadON);
    displayNewDownload(!newDownloadON);
    try {
      const response = axios.head(url);
      response
        .then((rs) => {
          // console.log(rs);
          // console.log(rs.headers["content-length"]);
          let newData = {
            new_url: url,
            savePath: "./",
            name_file: "",
            catg: "UNKNOWN",
            size: 0,
            speed_limit: 256,
            command_option: "new",
            downloaded: 0,
            Resume: "false",
          };
          newData["name_file"] = url.split("/").pop();
          newData["size"] = rs.headers["content-length"];

          // cat_selector("")
          setNewDownload(newData);
        })
        .catch((error) => {
          console.log({ errr: error });
        });
    } catch (error) {
      console.error("Error:fin", error.message);
    }
  }

  const handleFilterClick = () => {
    // Perform filtering logic here based on searchTerm, filter1, and filter2
    // Update the table data accordingly
  };

  // function connectSocket() {
  //   socket = io("http://localhost:5001");

  //   // Listen for the `connect` event
  //   socket.on("connect", () => {
  //     console.log("Connected to server.");
  //   });

  //   // Listen for the `message` event
  //   socket.on("message", (data) => {
  //     console.log(`Received message: ${data}`);
  //   });

  //   // Send a message
  //   socket.emit("message", "Hello from the client!");

  //   // Close the connection
  //   // setTimeout(() => {
  //   //   socket.disconnect();
  //   // }, 5000000);
  // }

  const handleAddClick = () => {
    // setshowAdd_Url(!showAdd_Url);
    displayAddUrl(!addUrlON);

    // if(socket){
    //   socket.disconnect();
    // }
    // connectSocket();
    // startNewDownload
    // getFileDetails(nwDownload.new_url);
    // setshowAdd_Url(!showAdd_Url)
    // setshowProgress(!showProgress);
    // setnewDownloadON(!newDownloadON);
    console.log("open download");
  };

  const handleContinueClick = () => {
    displayNewDownload(!newDownloadON);

    console.log("continue 2 clicked");
  };

  const handleStopClick = () => {
    let xd = { filename: fname };

    console.log("stop 3 clicked to stop", { xd });
    axios
      .post("http://localhost:5001/stop", xd)
      .then((response) =>
        console.log({ download_file_server_response: response })
      );
  };

  const handleRemoveClick = () => {
    console.log("remove 4 clicked");
  };
  // let xurl =
  //   "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-623.exe";
  return (
    <>
      {/* {showAdd_Url && (
        <Add_Url
          url={xurl}
          show={showAdd_Url}
          handleClose={Close_Add_url}
          openNewDownload={getFileDetails}
        />
      )}
      {newDownloadON && (
        <New_Download
          data={nwDownload}
          show={newDownloadON}
          showProgresBox={()=>setshowProgress(!showProgress)}
          handleClose={Close_New_Down}
        />
      )}

      {showProgress && (
        <Download_Progress
          downloadDetails={defaultDownload}
          show={showProgress}
          handleClose={handleClose}
        />
      )} */}

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
            onClick={handleRemoveClick}
            variant="outline-warning"
            style={style.btn}
          >
            <span>Remove</span>
            <Image src={Recyle} style={style.pic} />
          </Button>
          <Button
            onClick={handleRemoveClick}
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
