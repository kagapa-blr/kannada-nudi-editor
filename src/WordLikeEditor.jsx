"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  Editor,
  EditorState,
  RichUtils,
  convertToRaw,
  convertFromRaw,
} from "draft-js";
import "draft-js/dist/Draft.css";
import { Button, IconButton } from "@mui/material";
import FormatBoldIcon from "@mui/icons-material/FormatBold";
import FormatItalicIcon from "@mui/icons-material/FormatItalic";
import FormatUnderlinedIcon from "@mui/icons-material/FormatUnderlined";
import SaveIcon from "@mui/icons-material/Save";
import FolderOpenIcon from "@mui/icons-material/FolderOpen";

const PAGE_HEIGHT = 1056; // 11 inches at 96 DPI
const PAGE_WIDTH = 816; // 8.5 inches at 96 DPI
const PAGE_PADDING = 72; // Padding for better alignment
const CONTENT_HEIGHT = PAGE_HEIGHT - PAGE_PADDING * 2;

export default function WordLikeEditor() {
  const [editorState, setEditorState] = useState(() =>
    EditorState.createEmpty()
  );
  const [pages, setPages] = useState([0]);
  const editorRef = useRef(null);

  useEffect(() => {
    updatePages();
  }, [editorState]);

  const updatePages = () => {
    if (editorRef.current) {
      const contentBlocks = editorRef.current.querySelectorAll(
        ".public-DraftStyleDefault-block"
      );
      let totalHeight = 0;

      contentBlocks.forEach((block) => {
        totalHeight += block.offsetHeight;
      });

      const pageCount = Math.ceil(totalHeight / CONTENT_HEIGHT);

      // Ensure there's at least one page and no extra empty pages
      setPages(Array.from({ length: Math.max(1, pageCount) }, (_, i) => i));
    }
  };

  const handleEditorChange = (state) => {
    setEditorState(state);
  };

  const handleKeyCommand = (command, editorState) => {
    const newState = RichUtils.handleKeyCommand(editorState, command);
    if (newState) {
      handleEditorChange(newState);
      return "handled";
    }
    return "not-handled";
  };

  const toggleInlineStyle = (style) => {
    handleEditorChange(RichUtils.toggleInlineStyle(editorState, style));
  };

  const saveDocument = () => {
    const content = JSON.stringify(
      convertToRaw(editorState.getCurrentContent())
    );
    localStorage.setItem("document", content);
    alert("Document saved!");
  };

  const loadDocument = () => {
    const content = localStorage.getItem("document");
    if (content) {
      const contentState = convertFromRaw(JSON.parse(content));
      handleEditorChange(EditorState.createWithContent(contentState));
    }
  };

  return (
    <div className="max-w-5xl mx-auto mt-8">
      <div className="mb-4 flex space-x-2 bg-gray-100 p-2 rounded-lg">
        <IconButton onClick={() => toggleInlineStyle("BOLD")} size="small">
          <FormatBoldIcon />
        </IconButton>
        <IconButton onClick={() => toggleInlineStyle("ITALIC")} size="small">
          <FormatItalicIcon />
        </IconButton>
        <IconButton onClick={() => toggleInlineStyle("UNDERLINE")} size="small">
          <FormatUnderlinedIcon />
        </IconButton>
        <div className="flex-grow"></div>
        <Button
          variant="contained"
          startIcon={<SaveIcon />}
          onClick={saveDocument}
          size="small"
        >
          Save
        </Button>
        <Button
          variant="outlined"
          startIcon={<FolderOpenIcon />}
          onClick={loadDocument}
          size="small"
        >
          Load
        </Button>
      </div>
      <div className="border rounded-lg shadow-lg bg-gray-200 p-5">
        <div
          className="relative bg-white mx-auto overflow-hidden shadow-md"
          style={{
            width: `${PAGE_WIDTH}px`,
            height: `${PAGE_HEIGHT * pages.length}px`,
          }}
        >
          <div
            ref={editorRef}
            className="absolute top-0 left-0 right-0 bottom-0"
            style={{
              padding: `${PAGE_PADDING}px`,
              height: `${CONTENT_HEIGHT * pages.length}px`,
              overflow: "hidden",
              boxSizing: "border-box", // Ensure padding is included in the height calculation
            }}
          >
            <Editor
              editorState={editorState}
              onChange={handleEditorChange}
              handleKeyCommand={handleKeyCommand}
            />
          </div>

          {pages.map((pageIndex) => (
            <React.Fragment key={pageIndex}>
              <div
                className="absolute left-0 right-0 bg-white shadow-md border border-gray-300"
                style={{
                  top: `${pageIndex * PAGE_HEIGHT}px`,
                  width: `${PAGE_WIDTH}px`,
                  height: `${PAGE_HEIGHT}px`,
                }}
              >
                <div className="absolute bottom-4 right-4 text-gray-400">
                  Page {pageIndex + 1}
                </div>
              </div>

              {/* Separation line between pages */}
              {pageIndex < pages.length - 1 && (
                <div
                  className="absolute left-0 right-0 border-t border-gray-400"
                  style={{
                    top: `${(pageIndex + 1) * PAGE_HEIGHT - 1}px`,
                  }}
                />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
}
