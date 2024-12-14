// UndoRedoButtons.js
import React from "react";

// Custom Undo button icon component
const CustomUndo = () => (
  <svg viewBox="0 0 18 18">
    <polygon className="ql-fill ql-stroke" points="6 10 4 12 2 10 6 10" />
    <path
      className="ql-stroke"
      d="M8.09,13.91A4.6,4.6,0,0,0,9,14,5,5,0,1,0,4,9"
    />
  </svg>
);

// Redo button icon component
const CustomRedo = () => (
  <svg viewBox="0 0 18 18">
    <polygon className="ql-fill ql-stroke" points="12 10 14 12 16 10 12 10" />
    <path
      className="ql-stroke"
      d="M9.91,13.91A4.6,4.6,0,0,1,9,14a5,5,0,1,1,5-5"
    />
  </svg>
);

const UndoRedoButtons = () => (
  <span className="ql-formats">
    <button className="ql-undo">
      <CustomUndo />
    </button>
    <button className="ql-redo">
      <CustomRedo />
    </button>
  </span>
);

export default UndoRedoButtons;
