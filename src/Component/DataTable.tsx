import filterFactory, { textFilter } from "react-bootstrap-table2-filter";
import BootstrapTable from "react-bootstrap-table-next";
import { useEffect, useRef, useState } from "react";
import { InputGroup, Form, Button } from "react-bootstrap";
import { io } from "socket.io-client";
import Download_Progress from "./Download_Progress";

// import paginationFactory from "react-bootstrap-table2-paginator";

const DataTable = ({ dataTable }) => {
  const [filterName, setFilterName] = useState("");
  const [filterExt, setFilterExt] = useState("");
  const data = [
    {
      N: 1,
      fileName: "winrar.exe",
      Status: "downloading",
      Finished: false,
      Time_Left: 15241,
      Downloaded: 253612,
      Speed: 14525,
      Extension: ".exe",
    },
    {
      N: 2,
      fileName: "winrar-x64-623.exe",
      Status: "stop",
      Finished: false,
      Time_Left: 1241,
      Downloaded: 2612,
      Speed: 145,
      Extension: ".exe",
    },
    // ... other data
  ];

  const columns = [
    { dataField: "N", text: "N", sort: true },
    { dataField: "fileName", text: "FileName", sort: true },
    { dataField: "Status", text: "Status", sort: true },
    { dataField: "Finished", text: "Finished", sort: true },
    { dataField: "Time_Left", text: "Time_Left", sort: true },
    { dataField: "Speed", text: "Speed", sort: true },
    { dataField: "Downloaded", text: "Downloaded", sort: true },
    // { dataField: "Extension", text: "Extension", sort: true },
  ];

  const [tableData, settableData] = useState(data);

  const [showProgress, setshowProgress] = useState(false);

  const defaultDownload = {
    new_url: "url",
    savePath: "./",
    name_file: "newfile",
    catg: "compress",
    size: "0",
    speed_limit: "0",
    command_option: "new",
    downloaded: 0,
    Resume: "false",
  };

  var DownloadContent = {
    Status: "Get",
    File_Size: "10mb",
    Speed: "145kb",
    Downloaded: "5.78mb",
    Time_Left: "1min 25sec",
    Resume: "True",
  };

  const [nwDownload, setNewDownload] = useState(DownloadContent);

  const filteredData = tableData.filter(
    (item) =>
      item.fileName.includes(filterName) && item.Extension.includes(filterExt)
  );

  // const paginationOption = {
  //   custom: true,
  //   totalSize: data.length,
  //   sizePerPage: 5,
  //   hideSizePerPage: true,
  //   hidePageListOnlyOnePage: true
  // };

  //   .sortable tr {
  //     cursor: pointer;
  // }
  

  useEffect(() => {

    if (dataTable) {
      settableData(dataTable);
    }

    // return () => {
    // }
  }, [dataTable]);

  const rowEvents = {
    onClick: (e, row, rowIndex) => {
      let dta = {
        FileName: row.fileName,
        Status: row.Status,
        Speed: row.Speed,
        finished:row.Finished,
        File_Size:row.FileSize,
        Downloaded: row.Downloaded,
        Time_Left: row.Time_Left,
        Resume: row.Resume,
        Url: row.Url,
      };

      setNewDownload(dta);
      setshowProgress(!showProgress);

      console.log({ e });
      console.log({ row });
      console.log({ dta });
      console.log(`clicked on row with index: ${rowIndex}`);
      // Add your function code here
    },
  };



  return (
    <>
      {/* {showProgress && (
        <Download_Progress
          downloadDetails={nwDownload}
          show={showProgress}
          handleClose={() => setshowProgress(false)}
        />
      )} */}
      <div className="d-flex justify-content-center">
        <InputGroup size="sm" className="mb-3" style={{ width: "fit-content" }}>
          <Form.Control
            type="text"
            value={filterExt}
            onChange={(e) => setFilterExt(e.target.value)}
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

      <BootstrapTable
        keyField="id"
        data={filteredData}
        columns={columns}
        rowEvents={rowEvents}
        hover
        // pagination={paginationFactory()}
      />
    </>
  );
};

export default DataTable;
