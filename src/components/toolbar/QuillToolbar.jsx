import React, { useState } from "react";
import { PAGE_SIZES } from "../../constants/pageSizes";
import { Select, MenuItem, InputLabel, FormControl } from "@mui/material";
import UndoIcon from "@mui/icons-material/Undo";
import RedoIcon from "@mui/icons-material/Redo";
import FolderOpenIcon from "@mui/icons-material/FolderOpen";
import SaveAltIcon from "@mui/icons-material/SaveAlt";
import { Quill } from "react-quill-new";
import { FONT_SIZES, FONTS } from "../../constants/Nudifonts";
import CustomSizeDialog from "./CustomSizeDialog";
import QuillResizeImage from "quill-resize-image";
import RefreshIcon from "@mui/icons-material/Refresh";
import { useBloomFilter } from "../../Context/bloom"; // Import the custom hook
import { getWrongWords } from "../../spellcheck/bloomFilter";
import { underlineWordInEditor } from "../../services/editorService";

const Size = Quill.import("formats/size");
Size.whitelist = FONT_SIZES;
Quill.register(Size, true);
import { ICON_LABELS_KANNADA } from "../../constants/formats";

export const Font = Quill.import("formats/font");
Font.whitelist = FONTS;
Quill.register(Font, true);

Quill.register("modules/resize", QuillResizeImage);

export const QuillToolbar = ({ quillRef, setPageSize }) => {
  const [pageSizeOption, setPageSizeOption] = useState("A4");
  const [prevPageSize, setPrevPageSize] = useState("A4");
  const [openModal, setOpenModal] = useState(false);
  const [fontOption, setFontOption] = useState(FONTS[0]);
  const [sizeOption, setSizeOption] = useState(FONT_SIZES[2]);
  const { bloomFilter, loading, error } = useBloomFilter(); // Use the BloomFilter context

  const handlePageSizeChange = (e) => {
    const selectedSize = e.target.value;
    setPageSizeOption(selectedSize);
    if (selectedSize === "Custom") {
      setPrevPageSize(pageSizeOption);
      setOpenModal(true);
    } else {
      const size = PAGE_SIZES[selectedSize];
      setPageSize(size);
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
      setOpenModal(false);
    }
  };

  const refreshButtonhandle = async () => {
    if (!bloomFilter) {
      console.error("BloomFilter not initialized");
      return;
    }

    try {
      const quill = quillRef.current?.getEditor();
      const wrongWords = await getWrongWords(quill, bloomFilter);
      if (wrongWords.length == 0) {
        console.log("No Wrong Words to correct");
        return;
      }
      if (wrongWords) {
        // Underline the wrong words in the editor
        wrongWords.forEach((word) => underlineWordInEditor(quill, word));
      }
    } catch (error) {
      console.error("Error during refresh:", error);
    }
  };

  const handleCloseModal = () => {
    setPageSizeOption(prevPageSize);
    setOpenModal(false);
  };

  return (
    <div id="toolbar" className="flex flex-wrap gap-4 p-4">
      <span className="ql-formats">
        <button className="ql-open" title={ICON_LABELS_KANNADA.open}>
          <FolderOpenIcon />
        </button>
        <button className="ql-save" title={ICON_LABELS_KANNADA.save}>
          <SaveAltIcon />
        </button>
      </span>

      <span className="ql-formats">
        <select
          className="ql-font"
          value={fontOption}
          onChange={handleFontChange}
          title={ICON_LABELS_KANNADA.font}
        >
          {FONTS.map((font, index) => (
            <option key={index} value={font}>
              {font}
            </option>
          ))}
        </select>

        <select
          className="ql-size"
          value={sizeOption}
          onChange={handleSizeChange}
          title={ICON_LABELS_KANNADA.fontSize}
        >
          {FONT_SIZES.map((size, index) => (
            <option key={index} value={size}>
              {size}
            </option>
          ))}
        </select>

        <select
          className="ql-header"
          defaultValue="3"
          title={ICON_LABELS_KANNADA.headline}
        >
          <option value="1">Heading</option>
          <option value="2">Subheading</option>
          <option value="3">Normal</option>
        </select>
      </span>
      <span className="ql-formats">
        <button className="ql-bold" title={ICON_LABELS_KANNADA.bold} />
        <button className="ql-italic" title={ICON_LABELS_KANNADA.italic} />
        <button
          className="ql-underline"
          title={ICON_LABELS_KANNADA.underline}
        />
        <button className="ql-strike" title={ICON_LABELS_KANNADA.strike} />
      </span>
      <span className="ql-formats">
        <button
          className="ql-list"
          value="ordered"
          title={ICON_LABELS_KANNADA.listOrdered}
        />
        <button
          className="ql-list"
          value="bullet"
          title={ICON_LABELS_KANNADA.listBullet}
        />
        <button
          className="ql-indent"
          value="-1"
          title={ICON_LABELS_KANNADA.indentDecrease}
        />
        <button
          className="ql-indent"
          value="+1"
          title={ICON_LABELS_KANNADA.indentIncrease}
        />
      </span>
      <span className="ql-formats">
        <button
          className="ql-script"
          value="super"
          title={ICON_LABELS_KANNADA.superscript}
        />
        <button
          className="ql-script"
          value="sub"
          title={ICON_LABELS_KANNADA.subscript}
        />
        <button
          className="ql-blockquote"
          title={ICON_LABELS_KANNADA.blockquote}
        />
        <button
          className="ql-direction"
          title={ICON_LABELS_KANNADA.direction}
        />
      </span>
      <span className="ql-formats">
        <select className="ql-align" title={ICON_LABELS_KANNADA.align} />
        <select className="ql-color" title={ICON_LABELS_KANNADA.color} />
        <select
          className="ql-background"
          title={ICON_LABELS_KANNADA.background}
        />
      </span>
      <span className="ql-formats">
        <button className="ql-link" title={ICON_LABELS_KANNADA.link} />
        <button className="ql-image" title={ICON_LABELS_KANNADA.image} />
        <button className="ql-video" title={ICON_LABELS_KANNADA.video} />
      </span>
      <span className="ql-formats">
        <button className="ql-formula" title={ICON_LABELS_KANNADA.formula} />
        <button className="ql-code-block" title={ICON_LABELS_KANNADA.block} />
        <button className="ql-clean" title={ICON_LABELS_KANNADA.clean} />
      </span>
      <span className="ql-formats">
        <button className="ql-undo" title={ICON_LABELS_KANNADA.undo}>
          <UndoIcon />
        </button>
        <button className="ql-redo" title={ICON_LABELS_KANNADA.redo}>
          <RedoIcon />
        </button>
      </span>

      <span className="ql-formats">
        <FormControl>
          <InputLabel>ಪುಟದ ಗಾತ್ರ</InputLabel>
          <Select
            label="ಪುಟದ ಗಾತ್ರ"
            className="ql-page-size"
            value={pageSizeOption}
            onChange={handlePageSizeChange}
          >
            {Object.keys(PAGE_SIZES).map((key) => (
              <MenuItem key={key} value={key}>
                {key}
              </MenuItem>
            ))}
            <MenuItem value="Custom">Custom</MenuItem>
          </Select>
        </FormControl>
      </span>

      <span className="ql-formats">
        <button onClick={refreshButtonhandle} className="ql-refresh-button">
          <RefreshIcon />
        </button>
      </span>

      <CustomSizeDialog
        open={openModal}
        onClose={handleCloseModal}
        onApply={applyCustomSize}
      />
    </div>
  );
};

export default QuillToolbar;
