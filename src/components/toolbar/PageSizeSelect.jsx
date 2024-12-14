// PageSizeSelect.js
import React from "react";
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";

const PageSizeSelect = ({ pageSizeOption, handlePageSizeChange }) => (
  <span className="ql-formats">
    <FormControl>
      <InputLabel>Page Size</InputLabel>
      <Select
        label="Page Size"
        className="ql-page-size"
        value={pageSizeOption}
        onChange={handlePageSizeChange}
      >
        <MenuItem value="A4">A4</MenuItem>
        <MenuItem value="Letter">Letter</MenuItem>
        <MenuItem value="Legal">Legal</MenuItem>
        <MenuItem value="Custom">Custom</MenuItem>
      </Select>
    </FormControl>
  </span>
);

export default PageSizeSelect;
