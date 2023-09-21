import { useState } from "react";
import Pagination from "react-bootstrap/Pagination";

const MyPagination = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = 5;

  const handlePrevClick = () => {
    setCurrentPage((prevPage) => prevPage - 1);
  };

  const handleNextClick = () => {
    setCurrentPage((prevPage) => prevPage + 1);
  };

  return (
    <Pagination size="sm">
      <Pagination.Prev onClick={handlePrevClick} disabled={currentPage === 1} />
      <Pagination.Item active>{currentPage}</Pagination.Item>
      <Pagination.Next
        onClick={handleNextClick}
        disabled={currentPage === totalPages}
      />
    </Pagination>
  );

};

export default MyPagination;
