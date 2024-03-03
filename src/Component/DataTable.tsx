import filterFactory, { textFilter } from "react-bootstrap-table2-filter";
import BootstrapTable from "react-bootstrap-table-next";
import { useEffect, useRef, useState } from "react";
import { InputGroup, Form, Button } from "react-bootstrap";
import { io } from "socket.io-client";
import Download_Progress from "./Download_Progress";
import { useDownloadTable, useIdmRequests } from "../zustand/useAppState";
import { IdmReq } from "../Utils/DownLoad_Action";

// import paginationFactory from "react-bootstrap-table2-paginator";

const DataTable = ({ dataTable }) => {
  const [filterName, setFilterName] = useState("");
  const [filterCat, setFilterCat] = useState("");

  const { CurrentRow, SetCurrentRow } = useIdmRequests((state) => state);

  // Catg
  // Cmd_Option
  // Downloaded
  // FileName
  // File_Size
  // Resume
  // SavePath
  // Speed
  // Status
  // Time_Left
  // Url
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
    // {
    //   N: 2,
    //   fileName: "winrar-x64-623.exe",
    //   Status: true,
    //   Finished: false,
    //   Time_Left: 1241,
    //   Downloaded: 2612,
    //   Speed: 145,
    //   Extension: ".exe",
    // },
    // ... other data
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

  // let filteredData=[];
  // let downloadsArray = Object.values(downloads) ;

  // const  useDownloadTa = useDownloadTable()
  // const [tableData, settableData] = useState(dataTable);

  // const [tableData, setTableData] = useState<Download[]>([]);

  // const { downloads } = useAppState();
  // const downloadsArray = Object.values(downloads);
  // const [tableData, settableData] = useState(downloadsArray);

  // console.log({ downloads: downloads });
  // console.log({ downloadsarray: downloadsArray });

  // console.log({ tableData });

  // const filteredData = dataTable.filter(
  //   (item) =>
  //     item.FileName.includes(filterName) && item.Catg.includes(filterCat)
  // );

  // const filteredData = dataTable.filter(
  //   (item) => {
  //     const regex = new RegExp(`^${filterName}.*`, 'i');
  //     // const regCat = new RegExp(`^${filterCat}.*`, 'i');
  //     // && item.Catg.match(regCat);
  //     return item.FileName.match(regex)
  //   }
  //  );

  const filteredData = dataTable.filter(
    (item) =>
      item.FileName.toLowerCase().includes(filterName.toLowerCase()) &&
      item.Catg.toLowerCase().includes(filterCat.toLowerCase())
  );

  const [showProgress, setshowProgress] = useState(false);

  // const defaultDownload = {
  //   new_url: "url",
  //   savePath: "./",
  //   name_file: "newfile",
  //   catg: "compress",
  //   size: "0",
  //   speed_limit: "0",
  //   command_option: "new",
  //   downloaded: 0,
  //   Resume: "false",
  // };

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

  // const filteredData = tableData.filter(
  //   (item) =>
  //     item.FileName.includes(filterName) && item.Catg.includes(filterCat)
  // );

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

  // useEffect(() => {
  //   if (useDownloadTa) {
  //     settableData(useDownloadTa);
  //   }
  //   // return () => {
  //   // }
  // }, [useDownloadTa]);

  // useEffect(() => {
  //   if (downloads) {
  //     settableData(downloadsArray);
  //   }
  // }, [downloads]);

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
      SetCurrentRow(item)

      // idmR.InitItem(url);
      // idmR.ContinueItem(item);

      console.log(e.currentTarget);

      // e.currentTarget.style.backgroundColor = "red";
      // console.log({ e });
      // console.log({ row });
      console.log(`clicked on row with index: ${rowIndex}`);
      // console.log({ dta });
      // Add your function code here
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
      
      {/* {showProgress && (
        <Download_Progress
          downloadDetails={nwDownload}
          show={showProgress}
          handleClose={() => setshowProgress(false)}
        />
      )} */}

      

      <BootstrapTable
        rowStyle={rowCssStyle}
        keyField="id"
        data={filteredData}
        columns={columns}
        rowEvents={rowEvents}
        hover
        // rowStyle={ (_,ind) => ind === selectedRowID ? {backgroundColor: 'lightblue'} : {} }
        // rowStyle={(_,ind) => {backgroundColor: ind === selectedRowID ? '#dcdcdc' : null}}
        // rowStyle={{backgroundColor: rowIndex === selectedRowID ? '#dcdcdc' : null}}
        // pagination={paginationFactory()}
      />
    </div>
    </>

  );
};

export default DataTable;
