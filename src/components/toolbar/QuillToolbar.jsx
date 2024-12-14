import React, { useState } from "react";
import { PAGE_SIZES } from "../../constants/pageSizes";
import { Select, MenuItem, InputLabel, FormControl } from "@mui/material";
import UndoIcon from "@mui/icons-material/Undo";
import RedoIcon from "@mui/icons-material/Redo";
import FolderOpenIcon from "@mui/icons-material/FolderOpen";
import SaveAltIcon from "@mui/icons-material/SaveAlt";
import { Quill } from "react-quill-new"; // Import Quill for font and size handling
import { FONT_SIZES, FONTS } from "../../constants/Nudifonts"; // Import font sizes and font names
import CustomSizeDialog from "./CustomSizeDialog"; // Import the custom size dialog component

// Add sizes to whitelist and register them
const Size = Quill.import("formats/size");
Size.whitelist = FONT_SIZES;
Quill.register(Size, true);

// Add fonts to whitelist and register them
export const Font = Quill.import("formats/font");
Font.whitelist = FONTS;
Quill.register(Font, true);

// Quill Toolbar component with Material-UI integration
export const QuillToolbar = ({ quillRef, setPageSize }) => {
  const [pageSizeOption, setPageSizeOption] = useState("A4"); // Default page size
  const [prevPageSize, setPrevPageSize] = useState("A4"); // Store previous page size
  const [openModal, setOpenModal] = useState(false); // Control the modal visibility
  const [fontOption, setFontOption] = useState(FONTS[0]); // Font option state
  const [sizeOption, setSizeOption] = useState(FONT_SIZES[2]); // Size option state

  const handlePageSizeChange = (e) => {
    const selectedSize = e.target.value;
    setPageSizeOption(selectedSize); // Update the selected page size option
    if (selectedSize === "Custom") {
      setPrevPageSize(pageSizeOption); // Store the previous page size
      setOpenModal(true); // Open the modal when "Custom" is selected
    } else {
      const size = PAGE_SIZES[selectedSize];
      setPageSize(size); // Apply the selected predefined page size
    }
  };

  const handleFontChange = (e) => {
    const selectedFont = e.target.value;
    setFontOption(selectedFont);
    const editor = quillRef?.current.getEditor();
    if (editor) {
      editor.format("font", selectedFont);
    }
  };

  const handleSizeChange = (e) => {
    const selectedSize = e.target.value;
    setSizeOption(selectedSize);
    const editor = quillRef?.current?.getEditor();
    if (editor) {
      editor.format("size", selectedSize);
    }
  };

  const applyCustomSize = (customSize) => {
    if (customSize.width && customSize.height) {
      setPageSize({
        width: customSize.width,
        height: customSize.height,
      });
      setOpenModal(false); // Close the modal after applying custom size
    }
  };

  const handleCloseModal = () => {
    setPageSizeOption(prevPageSize); // Restore the previous page size if canceled
    setOpenModal(false); // Close the modal without applying changes
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
        {/* Open File Button */}
        <button className="ql-open">
          <FolderOpenIcon />
        </button>
        {/* Save File Button */}
        <button className="ql-save">
          <SaveAltIcon />
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
            {/* Dynamically render the page sizes from the PAGE_SIZES object */}
            {Object.keys(PAGE_SIZES).map((key) => (
              <MenuItem key={key} value={key}>
                {key}
              </MenuItem>
            ))}
            <MenuItem value="Custom">Custom</MenuItem>
          </Select>
        </FormControl>
      </span>

      {/* Custom Size Dialog */}
      <CustomSizeDialog
        open={openModal}
        onClose={handleCloseModal}
        onApply={applyCustomSize}
      />
    </div>
  );
};

export default QuillToolbar;
