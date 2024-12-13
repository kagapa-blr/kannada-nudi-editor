import React, { useRef, useEffect } from "react";
import { Editor } from "draft-js";
import Page from "./Page";

const PAGE_HEIGHT = 1056;
const PAGE_PADDING = 72;
const CONTENT_HEIGHT = PAGE_HEIGHT - PAGE_PADDING * 2;

export default function EditorContainer({ editorState, onChange, pages, updatePages }) {
  const editorRef = useRef(null);

  useEffect(() => {
    updatePages();
  }, [editorState]);

  return (
    <div
      className="relative bg-white mx-auto overflow-hidden shadow-md"
      style={{
        width: "816px",
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
          boxSizing: "border-box",
        }}
      >
        <Editor editorState={editorState} onChange={onChange} />
      </div>

      {pages.map((pageIndex) => (
        <Page key={pageIndex} pageIndex={pageIndex} isLast={pageIndex === pages.length - 1} />
      ))}
    </div>
  );
}
