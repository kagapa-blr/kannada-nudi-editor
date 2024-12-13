import React from "react";
import { Button, IconButton } from "@mui/material";
import FormatBoldIcon from "@mui/icons-material/FormatBold";
import FormatItalicIcon from "@mui/icons-material/FormatItalic";
import FormatUnderlinedIcon from "@mui/icons-material/FormatUnderlined";
import SaveIcon from "@mui/icons-material/Save";
import FolderOpenIcon from "@mui/icons-material/FolderOpen";

export default function Toolbar({ toggleInlineStyle, saveDocument, loadDocument }) {
  return (
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
  );
}
