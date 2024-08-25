/* eslint-disable react/prop-types */
import { useState, useEffect } from "react";
import { Table, Text, Button, Flex } from "@radix-ui/themes";


export const DataTable = ({ data, itemsPerPage = 5 }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedRows, setSelectedRows] = useState([]);

  useEffect(() => {
    setCurrentPage(1);
    setSelectedRows([]); // Clear selection when data changes
  }, [data]);

  if (!data || data.length === 0) {
    return <p style={{ fontSize: "16px" }}>No data available</p>;
  }

  const headers = Object.keys(data[0]);
  const totalPages = Math.ceil(data.length / itemsPerPage);

  // Calculate the current page's data
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = data.slice(indexOfFirstItem, indexOfLastItem);

  const changePage = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const toggleRowSelection = (index) => {
    setSelectedRows((prev) => {
      const newSelection = prev.includes(index)
        ? prev.filter((i) => i !== index)
        : [...prev, index];

      // Copy the new selection to clipboard
      const selectionString = newSelection
        .map((i) => JSON.stringify(data[i]))
        .join("\n");
      navigator.clipboard
        .writeText(selectionString)
        .catch((err) => console.error("Failed to copy:", err));

      return newSelection;
    });
  };

  return (
    <Flex direction="column" gap="3">
      <Text>
        Showing {currentItems.length} of {data.length} entries
      </Text>
      <Table.Root>
        <Table.Header>
          <Table.Row>
            {headers.map((header) => (
              <Table.ColumnHeaderCell key={header}>
                {header}
              </Table.ColumnHeaderCell>
            ))}
          </Table.Row>
        </Table.Header>
        <Table.Body style={{ 
          margin: '0',
          height: "100%",
          overflow: 'visible'
        }}>
          {currentItems.map((row, index) => (
            <Table.Row
              key={index}
              onClick={() => toggleRowSelection(index)}
              className={selectedRows.includes(index) ? "selected" : ""}
            >
              {headers.map((header) => (
                <Table.Cell key={`${index}-${header}`}>
                  {row[header]}
                </Table.Cell>
              ))}
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
      <Flex justify="between" align="center">
        <Button
          onClick={() => changePage(currentPage - 1)}
          disabled={currentPage === 1}
        >
          Previous
        </Button>
        <Text>{`Page ${currentPage} of ${totalPages}`}</Text>
        <Button
          onClick={() => changePage(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          Next
        </Button>
      </Flex>
    </Flex>
  );
};
