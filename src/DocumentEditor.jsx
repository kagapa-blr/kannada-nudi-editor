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
import { Button } from "@/components/ui/button";

const PAGE_HEIGHT = 1056; // 11 inches at 96 DPI
const PAGE_WIDTH = 816; // 8.5 inches at 96 DPI
const PAGE_PADDING = 72; // Padding for better alignment
const CONTENT_HEIGHT = PAGE_HEIGHT - PAGE_PADDING * 2;

export default function DocumentEditor() {
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
      const contentHeight = editorRef.current.clientHeight;
      const pageCount = Math.max(1, Math.ceil(contentHeight / CONTENT_HEIGHT));
      setPages(Array.from({ length: pageCount }, (_, i) => i));
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
      <div className="mb-4 space-x-2">
        <Button onClick={() => toggleInlineStyle("BOLD")}>Bold</Button>
        <Button onClick={() => toggleInlineStyle("ITALIC")}>Italic</Button>
        <Button onClick={() => toggleInlineStyle("UNDERLINE")}>
          Underline
        </Button>
        <Button onClick={saveDocument}>Save</Button>
        <Button onClick={loadDocument}>Load</Button>
      </div>
      <div className="border rounded-lg shadow-lg bg-gray-200 p-8">
        <div
          className="relative bg-white mx-auto overflow-hidden shadow-md"
          style={{
            width: `${PAGE_WIDTH}px`,
            height: `${PAGE_HEIGHT * pages.length}px`,
            overflow: "hidden",
          }}
        >
          <div
            ref={editorRef}
            className="absolute top-0 left-0 right-0"
            style={{
              padding: `${PAGE_PADDING}px`,
              height: `${CONTENT_HEIGHT * pages.length}px`,
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
                className="absolute left-0 right-0"
                style={{
                  top: `${pageIndex * PAGE_HEIGHT}px`,
                  height: `${PAGE_HEIGHT}px`,
                  borderBottom: "2px solid #ccc",
                }}
              >
                <div className="absolute bottom-4 right-4 text-gray-400">
                  Page {pageIndex + 1}
                </div>
              </div>
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
}
