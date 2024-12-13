"use client";

import React, { useState } from "react";
import { EditorState, RichUtils, convertToRaw, convertFromRaw } from "draft-js";
import "draft-js/dist/Draft.css";
import Toolbar from "./components/Toolbar";
import EditorContainer from "./components/EditorContainer";

export default function WordLikeEditor() {
  const [editorState, setEditorState] = useState(() =>
    EditorState.createEmpty()
  );
  const [pages, setPages] = useState([0]);

  const updatePages = () => {
    const contentBlocks = document.querySelectorAll(
      ".public-DraftStyleDefault-block"
    );
    let totalHeight = 0;

    contentBlocks.forEach((block) => {
      totalHeight += block.offsetHeight;
    });

    const pageCount = Math.ceil(totalHeight / 912);
    setPages(Array.from({ length: Math.max(1, pageCount) }, (_, i) => i));
  };

  const handleEditorChange = (state) => {
    setEditorState(state);
  };

  const handleKeyCommand = (command) => {
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
      <Toolbar
        toggleInlineStyle={toggleInlineStyle}
        saveDocument={saveDocument}
        loadDocument={loadDocument}
      />
      <div className="border rounded-lg shadow-lg bg-gray-200 p-5">
        <EditorContainer
          editorState={editorState}
          onChange={handleEditorChange}
          pages={pages}
          updatePages={updatePages}
        />
      </div>
    </div>
  );
}
