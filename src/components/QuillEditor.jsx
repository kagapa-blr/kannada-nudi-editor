import React, { useState, useRef, useEffect } from "react";
import ReactQuill from "react-quill-new";
import "react-quill-new/dist/quill.snow.css";
import Page from "./Page";
import EditorToolbar, { modules, formats } from "./QuillToolbar";

const PAGE_HEIGHT = 1056; // 11 inches at 96 DPI
const PAGE_WIDTH = 816; // 8.5 inches at 96 DPI

export const QuillEditor = () => {
  const [content, setContent] = useState("");
  const [pages, setPages] = useState([0]);
  const editorRef = useRef(null);

  useEffect(() => {
    paginateContent();
  }, [content]);

  const handleChange = (value) => {
    setContent(value);
  };

  const paginateContent = () => {
    const editor = editorRef.current.getEditor();
    const editorContent = editor.root;

    const contentHeight = editorContent.scrollHeight;
    const requiredPages = Math.ceil(contentHeight / PAGE_HEIGHT);

    setPages(Array.from({ length: requiredPages }, (_, i) => i));
  };

  return (
    <div className="editor-container">
      <div className="editor-toolbar-container">
        <EditorToolbar />
      </div>
      <div className="editor-wrapper">
        <div className="relative">
          {pages.map((pageIndex, idx) => (
            <Page
              key={pageIndex}
              pageIndex={pageIndex}
              isLast={idx === pages.length - 1}
            />
          ))}
        </div>
        <ReactQuill
          ref={editorRef}
          theme="snow"
          value={content}
          onChange={handleChange}
          modules={modules}
          formats={formats}
          style={{ width: `${PAGE_WIDTH}px`, minHeight: `${PAGE_HEIGHT}px` }}
          className="quill-editor"
        />
      </div>
    </div>
  );
};

export default QuillEditor;
