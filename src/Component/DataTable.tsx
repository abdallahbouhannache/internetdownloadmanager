import BootstrapTable from "react-bootstrap-table-next";
import { InputGroup, Form, Button } from "react-bootstrap";
import { IdmReq } from "../Utils/DownLoad_Action";
import {
  useIdmRequests,
  useProgresID,
  useWindowsStore,
} from "../zustand/useAppState";
import { useState } from "react";
import { formatFileSize } from "../Utils/tools";

const DataTable = ({ dataTable }) => {
  const [filterName, setFilterName] = useState("");
  const [filterCat, setFilterCat] = useState("");
  const { CurrentRow, SetCurrentRow } = useIdmRequests((state) => state);
  const { progresID, setprogresID } = useProgresID();
  const { displayProgress, progressON } = useWindowsStore();

  const handleRowDoubleClick = (e, row, rowIndex) => {
    e.stopPropagation();
    // console.log(`Double-clicked row ${rowIndex}:`, row, e);

    let data = {
      id: row.id || "",
      FileName: row.FileName || "",
    };

    setprogresID(data);
    displayProgress(!progressON);

    // Add your logic here, e.g., navigate to detail view, open modal, etc.
  };

  // const data = [
  //   {
  //     FileName: "ManuallyEntred.exe",
  //     SavePath: "/downloads/images",
  //     Status: true,
  //     Finished: false,
  //     Time_Left: 15241,
  //     Downloaded: 253612,
  //     File_Size: 10000,
  //     Speed: 14525,
  //     Url: "https",
  //     Catg: ".exe",
  //     Resume: false,
  //   },
  // ];
// Define a common style for all columns
  const columnStyle = {
    maxWidth: "20rem",
    whiteSpace: "nowrap",
    overflow: "hidden",
    textOverflow: "ellipsis",
    fontSize: "14px",
  };

  const columns = [
    { dataField: "FileName", text: "FileName", sort: true, style: columnStyle },
    { dataField: "Status", text: "Status", sort: true, style: columnStyle },
    { dataField: "Finished", text: "Finished", sort: true, style: columnStyle },
    { dataField: "Time_Left", text: "Time_Left", sort: true, style: columnStyle },
    {
      dataField: "Speed",
      text: "Speed",
      sort: true, style: columnStyle,
      formatter: (cellContent, row, rowIndex, formatExtraData) => {
        return formatFileSize(cellContent);
      },
    },
    {
      dataField: "Downloaded",
      text: "Downloaded",
      sort: true, style: columnStyle,
      formatter: (cellContent, row, rowIndex, formatExtraData) => {
        return formatFileSize(cellContent);
      },
    },
    { dataField: "SavePath", text: "SavePath", sort: true, style: columnStyle },
    {
      dataField: "File_Size",
      text: "File_Size",
      sort: true, style: columnStyle,
      formatter: (cellContent, row, rowIndex, formatExtraData) => {
        return formatFileSize(cellContent);
      },
    },
    {
      dataField: "Url",
      text: "Url",
      sort: true, style: columnStyle
    },
    { dataField: "Catg", text: "Catg", sort: true, style: columnStyle },
    { dataField: "Resume", text: "Resume", sort: true, style: columnStyle },
  ];

  const filteredData = dataTable.filter(
    (item) =>
      item.FileName.toLowerCase().includes(filterName.toLowerCase()) &&
      item.Catg.toLowerCase().includes(filterCat.toLowerCase())
  );

  // const [showProgress, setshowProgress] = useState(false);

  // var DownloadContent = {
  //   Status: "Get",
  //   File_Size: "10mb",
  //   Speed: "145kb",
  //   Downloaded: "5.78mb",
  //   Time_Left: "1min 25sec",
  //   Resume: "True",
  // };
  // const [nwDownload, setNewDownload] = useState(DownloadContent);

  const [selectedRowID, setSelectedRowID] = useState(null);
  const idmR = IdmReq();

  const rowEvents = {
    onDoubleClick: handleRowDoubleClick,
    onClick: (e, row, rowIndex) => {
      e.stopPropagation();
      let item = {
        Url: row.Url,
        FileName: row.FileName,
        Status: row.Status,
        Speed: row.Speed,
        finished: row.Finished,
        File_Size: row.File_Size,
        Downloaded: row.Downloaded,
        Time_Left: row.Time_Left,
        Resume: row.Resume,
      };
      // setNewDownload(item);
      // setshowProgress(!showProgress);
      setSelectedRowID(rowIndex);
      SetCurrentRow(item);
      // console.log(e.currentTarget);
      // console.log(`clicked on row with index: ${rowIndex}`);
      // idmR.InitItem(url);
      // idmR.ContinueItem(item);
      // e.currentTarget.style.backgroundColor = "red";
    },
  };
  // .bootstrap-table .table-hover tbody tr:hover
  // e.currentTarget.style.backgroundColor = "red";

  const rowCssStyle = (_, ind) => {
    if (ind === selectedRowID) {
      return {
        backgroundColor: "#6b3a00e8",
        "--bs-table-bg": "#6b3a00e8",
        "--bs-table-color": "#ffffff",
      }
    }else{
      return {
        backgroundColor: "#ffffff",
        "--bs-table-bg": "#ffffff",
        "--bs-table-color": "#000000",
      }
    }
  };

  return (
    <>
      <div className="d-flex justify-content-center">
        <InputGroup size="sm" className="mb-3" style={{ width: "fit-content" }}>
          <Form.Control
            type="text"
            value={filterCat}
            onChange={(e) => setFilterCat(e.target.value)}
            placeholder="Filter by extension"
          />
          <Form.Control
            aria-label="Small"
            aria-describedby="inputGroup-sizing-sm"
            type="text"
            value={filterName}
            onChange={(e) => setFilterName(e.target.value)}
            placeholder="Filter by name"
          />
        </InputGroup>
      </div>

      <div
        onClick={() => {
          setSelectedRowID(null);
        }}
        className="table-container"
        
      >
        <BootstrapTable
          keyField="id"
          rowStyle={rowCssStyle}
          data={filteredData}
          columns={columns}
          rowEvents={rowEvents}
          hover
          condensed
          // striped
        />
      </div>
    </>
  );
};

export default DataTable;
