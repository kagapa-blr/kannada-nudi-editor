import { useState, useRef, useEffect } from "react";
import ReactQuill from "react-quill-new";
import "react-quill-new/dist/quill.snow.css";
import Page from "./Page";
import EditorToolbar from "./toolbar/QuillToolbar";
import { formats } from "../constants/formats";
import { modules } from "../constants/editorModules";

const QuillEditor = () => {
  const [content, setContent] = useState("");
  const [pages, setPages] = useState([0]);
  const [pageSize, setPageSize] = useState({ width: 816, height: 1056 }); // Default A4 size
  const quillRef = useRef(null);

  useEffect(() => {
    paginateContent();
  }, [content, pageSize]);
  useEffect(() => {
    if (quillRef.current) {
      quillRef.current.getEditor().root.setAttribute("spellcheck", "false");
    }
  }, []);
  const handleChange = (value) => {
    setContent(value);
  };

  const paginateContent = () => {
    const editor = quillRef?.current?.getEditor();
    const editorContent = editor.root;
    const contentHeight = editorContent.scrollHeight;
    const requiredPages = Math.ceil(contentHeight / pageSize.height);

    setPages(Array.from({ length: requiredPages }, (_, i) => i));
  };

  return (
    <div className="editor-container">
      <div className="editor-toolbar-container">
        <EditorToolbar
          quillRef={quillRef} // Pass the quill reference to the toolbar
          setPageSize={setPageSize}
        />
      </div>
      <div className="editor-wrapper">
        <div className="relative">
          {pages.map((pageIndex, idx) => (
            <Page
              key={pageIndex}
              pageIndex={pageIndex}
              isLast={idx === pages.length - 1}
              pageSize={pageSize}
            />
          ))}
        </div>
        <ReactQuill
          ref={quillRef}
          theme="snow"
          value={content}
          onChange={handleChange}
          modules={modules}
          formats={formats}
          style={{
            width: `${pageSize.width}px`,
            minHeight: `${pageSize.height}px`,
          }}
          className="quill-editor"
        />
      </div>
    </div>
  );
};

export default QuillEditor;
