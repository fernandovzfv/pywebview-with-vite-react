import { useState, useRef } from "react";
import { DataTable } from "./DataTable";
import { Box, Flex, TextField } from "@radix-ui/themes";

export default function Tracker() {
  const [command, setCommand] = useState("");
  const [tableData, setTableData] = useState([]);
  const inputRef = useRef(null);

  const handleCommandSubmit = async (e) => {
    e.preventDefault();
    const result = await window.pywebview.api.execute_command(command);

    if (Array.isArray(result)) {
      setTableData(result);
    } else {
      console.error("Unexpected result format");
      setTableData([]);
    }

    setCommand("");
  };

  return (
    <>
      <form onSubmit={handleCommandSubmit}>
        <Flex direction="column" gap="2">
            <TextField.Root
              id="command-input"
              ref={inputRef}
              type="text"
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              placeholder="Type a command and press Enter (i.e. /all, /id <id>)"
            />
        </Flex>
      </form>

      <Box>
        <DataTable data={tableData} />
      </Box>
    </>
  );
}
