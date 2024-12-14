import React, { useRef, useEffect, useState } from "react";
import ReactQuill from "react-quill-new";
import "react-quill-new/dist/quill.snow.css";
import Page from "./Page";

const PAGE_HEIGHT = 1056; // 11 inches at 96 DPI
const PAGE_PADDING = 72;  // Padding for the content inside the page
const CONTENT_HEIGHT = PAGE_HEIGHT - PAGE_PADDING * 2;

const modules = {
  toolbar: [
    [{ header: [1, 2, 3, false] }],
    ["bold", "italic", "underline", "strike"],
    [{ list: "ordered" }, { list: "bullet" }],
    [{ indent: "-1" }, { indent: "+1" }],
    ["link", "image"],
    ["clean"],
  ],
};

const formats = [
  "header",
  "bold",
  "italic",
  "underline",
  "strike",
  "list",
  "bullet",
  "indent",
  "link",
  "image",
];

const QuillEditor = () => {
  const [content, setContent] = useState("");
  const [pages, setPages] = useState([0]);
  const editorRef = useRef(null);

  useEffect(() => {
    updatePages();
  }, [content]);

  const handleChange = (value) => {
    setContent(value);
  };

  const updatePages = () => {
    const editorElement = document.querySelector(".ql-editor");
    if (!editorElement) return;

    const contentHeight = editorElement.scrollHeight;
    const totalPages = Math.ceil(contentHeight / CONTENT_HEIGHT);

    setPages([...Array(totalPages).keys()]);
  };

  return (
    <div
      className="relative bg-white mx-auto overflow-hidden shadow-md"
      style={{
        width: "816px",
        height: `${PAGE_HEIGHT * pages.length}px`,
      }}
    >
      {/* Quill Editor */}
      <div className="sticky top-0 z-10 bg-white">
        <ReactQuill
          value={content}
          onChange={handleChange}
          placeholder="Start writing..."
          theme="snow"
          modules={modules}
          formats={formats}
        />
      </div>

      {/* Pages */}
      {pages.map((pageIndex) => (
        <Page key={pageIndex} pageIndex={pageIndex} isLast={pageIndex === pages.length - 1} />
      ))}
    </div>
  );
};

export default QuillEditor;
