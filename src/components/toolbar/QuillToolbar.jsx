import React, { useState, useEffect } from "react";
import { PAGE_SIZES } from "../../constants/pageSizes";
import {
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  TextField,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from "@mui/material";
import UndoIcon from "@mui/icons-material/Undo";
import RedoIcon from "@mui/icons-material/Redo";
import { Quill } from "react-quill-new"; // Import Quill for font and size handling
import { FONT_SIZES, FONTS } from "../../constants/Nudifonts"; // Import font sizes and font names

// Add sizes to whitelist and register them
const Size = Quill.import("formats/size");
Size.whitelist = FONT_SIZES;
Quill.register(Size, true);

// Add fonts to whitelist and register them
export const Font = Quill.import("formats/font");
Font.whitelist = FONTS;
Quill.register(Font, true);

// Undo and redo functions for Custom Toolbar
function undoChange() {
  this.quill.history.undo();
}
function redoChange() {
  this.quill.history.redo();
}

// Modules object for setting up the Quill editor
export const modules = {
  toolbar: {
    container: "#toolbar",
    handlers: {
      undo: undoChange,
      redo: redoChange,
      // Custom handler for page size
      "page-size": function (value) {
        const selectedSize = PAGE_SIZES[value];
        if (selectedSize) {
          this.quill.root.style.width = `${selectedSize.width}px`;
          this.quill.root.style.minHeight = `${selectedSize.height}px`;
        }
      },
      // Add custom handlers for font and size
      font: function (value) {
        if (value) {
          this.quill.format("font", value);
        }
      },
      size: function (value) {
        if (value) {
          this.quill.format("size", value);
        }
      },
    },
  },
  history: {
    delay: 500,
    maxStack: 100,
    userOnly: true,
  },
};

// Quill Toolbar component with Material-UI integration
export const QuillToolbar = ({ setPageSize }) => {
  const [customSize, setCustomSize] = useState({ width: "", height: "" });
  const [pageSizeOption, setPageSizeOption] = useState("A4"); // Default page size
  const [openModal, setOpenModal] = useState(false); // Control the modal visibility
  const [fontOption, setFontOption] = useState(FONTS[0]); // Font option state
  const [sizeOption, setSizeOption] = useState(FONT_SIZES[2]); // Size option state

  const handlePageSizeChange = (e) => {
    const selectedSize = e.target.value;
    setPageSizeOption(selectedSize); // Update the selected page size option
    if (selectedSize === "Custom") {
      setOpenModal(true); // Open the modal when "Custom" is selected
    } else {
      const size = PAGE_SIZES[selectedSize];
      setPageSize(size); // Apply the selected predefined page size
    }
  };

  const handleCustomWidthChange = (e) => {
    setCustomSize((prev) => ({ ...prev, width: e.target.value }));
  };

  const handleCustomHeightChange = (e) => {
    setCustomSize((prev) => ({ ...prev, height: e.target.value }));
  };

  const applyCustomSize = () => {
    if (customSize.width && customSize.height) {
      setPageSize({
        width: parseInt(customSize.width),
        height: parseInt(customSize.height),
      });
      setOpenModal(false); // Close the modal after applying custom size
    }
  };

  const handleCloseModal = () => {
    setOpenModal(false); // Close the modal without applying changes
  };

  const handleFontChange = (e) => {
    const selectedFont = e.target.value;
    setFontOption(selectedFont);
    if (this.quill) {
      this.quill.format("font", selectedFont);
    }
  };

  const handleSizeChange = (e) => {
    const selectedSize = e.target.value;
    setSizeOption(selectedSize);
    if (this.quill) {
      this.quill.format("size", selectedSize);
    }
  };

  return (
    <div id="toolbar" className="flex flex-wrap gap-4 p-4">
      <span className="ql-formats">
        {/* Font selection */}
        <select
          className="ql-font"
          value={fontOption}
          onChange={handleFontChange}
        >
          {FONTS.map((font, index) => (
            <option key={index} value={font}>
              {font}
            </option>
          ))}
        </select>

        {/* Size selection */}
        <select
          className="ql-size"
          value={sizeOption}
          onChange={handleSizeChange}
        >
          {FONT_SIZES.map((size, index) => (
            <option key={index} value={size}>
              {size}
            </option>
          ))}
        </select>

        <select className="ql-header" defaultValue="3">
          <option value="1">Heading</option>
          <option value="2">Subheading</option>
          <option value="3">Normal</option>
        </select>
      </span>
      <span className="ql-formats">
        <button className="ql-bold" />
        <button className="ql-italic" />
        <button className="ql-underline" />
        <button className="ql-strike" />
      </span>
      <span className="ql-formats">
        <button className="ql-list" value="ordered" />
        <button className="ql-list" value="bullet" />
        <button className="ql-indent" value="-1" />
        <button className="ql-indent" value="+1" />
      </span>
      <span className="ql-formats">
        <button className="ql-script" value="super" />
        <button className="ql-script" value="sub" />
        <button className="ql-blockquote" />
        <button className="ql-direction" />
      </span>
      <span className="ql-formats">
        <select className="ql-align" />
        <select className="ql-color" />
        <select className="ql-background" />
      </span>
      <span className="ql-formats">
        <button className="ql-link" />
        <button className="ql-image" />
        <button className="ql-video" />
      </span>
      <span className="ql-formats">
        <button className="ql-formula" />
        <button className="ql-code-block" />
        <button className="ql-clean" />
      </span>
      <span className="ql-formats">
        <button className="ql-undo">
          <UndoIcon />
        </button>
        <button className="ql-redo">
          <RedoIcon />
        </button>
      </span>

      {/* Page Size Dropdown using Material-UI */}
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

      {/* Modal for Custom Size */}
      <Dialog open={openModal} onClose={handleCloseModal}>
        <DialogTitle>Enter Custom Page Size</DialogTitle>
        <DialogContent>
          <TextField
            label="Width (px)"
            type="number"
            fullWidth
            value={customSize.width}
            onChange={handleCustomWidthChange}
            margin="normal"
          />
          <TextField
            label="Height (px)"
            type="number"
            fullWidth
            value={customSize.height}
            onChange={handleCustomHeightChange}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseModal} color="secondary">
            Cancel
          </Button>
          <Button onClick={applyCustomSize} color="primary">
            Apply
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default QuillToolbar;
