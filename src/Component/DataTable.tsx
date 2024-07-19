import BootstrapTable from "react-bootstrap-table-next";
import { InputGroup, Form, Button } from "react-bootstrap";
import { IdmReq } from "../Utils/DownLoad_Action";
import { useIdmRequests } from "../zustand/useAppState";
import { useState } from "react";

const DataTable = ({ dataTable }) => {
  const [filterName, setFilterName] = useState("");
  const [filterCat, setFilterCat] = useState("");
  const { CurrentRow, SetCurrentRow } = useIdmRequests((state) => state);

  const data = [
    {
      FileName: "ManuallyEntred.exe",
      SavePath: "/downloads/images",
      Status: true,
      Finished: false,
      Time_Left: 15241,
      Downloaded: 253612,
      File_Size: 10000,
      Speed: 14525,
      Url: "https",
      Catg: ".exe",
      Resume: false,
    },
  ];

  const columns = [
    { dataField: "FileName", text: "FileName", sort: true },
    { dataField: "Status", text: "Status", sort: true },
    { dataField: "Finished", text: "Finished", sort: true },
    { dataField: "Time_Left", text: "Time_Left", sort: true },
    { dataField: "Speed", text: "Speed", sort: true },
    { dataField: "Downloaded", text: "Downloaded", sort: true },
    { dataField: "SavePath", text: "SavePath", sort: true },
    { dataField: "File_Size", text: "File_Size", sort: true },
    { dataField: "Url", text: "Url", sort: true },
    { dataField: "Catg", text: "Catg", sort: true },
    { dataField: "Resume", text: "Resume", sort: true },
  ];

  const filteredData = dataTable.filter(
    (item) =>
      item.FileName.toLowerCase().includes(filterName.toLowerCase()) &&
      item.Catg.toLowerCase().includes(filterCat.toLowerCase())
  );

  const [showProgress, setshowProgress] = useState(false);

  var DownloadContent = {
    Status: "Get",
    File_Size: "10mb",
    Speed: "145kb",
    Downloaded: "5.78mb",
    Time_Left: "1min 25sec",
    Resume: "True",
  };

  const [nwDownload, setNewDownload] = useState(DownloadContent);

  const [selectedRowID, setSelectedRowID] = useState(null);
  const idmR = IdmReq();

  const rowEvents = {
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

      setNewDownload(item);
      setshowProgress(!showProgress);
      setSelectedRowID(rowIndex);
      SetCurrentRow(item);

      console.log(e.currentTarget);
      console.log(`clicked on row with index: ${rowIndex}`);

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
        // border: "solid 2px black",
        // color: "purple",
        // "--bs-table-bg":"#b4844d85",
        "--bs-table-color": "#ffffff",
        "--bs-table-bg": "#6b3a00e8",
      };
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
          rowStyle={rowCssStyle}
          keyField="id"
          data={filteredData}
          columns={columns}
          rowEvents={rowEvents}
          hover
        />
      </div>
    </>
  );
};

export default DataTable;
