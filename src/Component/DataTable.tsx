import filterFactory, { textFilter } from "react-bootstrap-table2-filter";
import BootstrapTable from "react-bootstrap-table-next";
import { useState } from "react";
import { InputGroup, Form } from "react-bootstrap";

// import paginationFactory from "react-bootstrap-table2-paginator";

const DataTable = () => {
  const [filterName, setFilterName] = useState("");
  const [filterExt, setFilterExt] = useState("");

  const data = [
    { id: 1, fileName: "File 1", extension: ".zip" },
    { id: 2, fileName: "File 2", extension: ".exe" },
    // ... other data
  ];

  const columns = [
    { dataField: "id", text: "ID", sort: true },
    { dataField: "fileName", text: "fileName", sort: true },
    { dataField: "extension", text: "Extension", sort: true },
  ];

  const filteredData = data.filter(
    (item) =>
      item.fileName.includes(filterName) && item.extension.includes(filterExt)
  );

  // const paginationOption = {
  //   custom: true,
  //   totalSize: data.length,
  //   sizePerPage: 5,
  //   hideSizePerPage: true,
  //   hidePageListOnlyOnePage: true
  // };

  return (
    <>
      <div className="d-flex justify-content-center" >
        <InputGroup size="sm" className="mb-3" style={{width:'fit-content'}}>
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
        // pagination={paginationFactory()}
      />
    </>
  );
};

export default DataTable;
