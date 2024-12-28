import React, { useState } from 'react';

const FileManager = () => {
  const [editorContent, setEditorContent] = useState('');
  const [currentFilePath, setCurrentFilePath] = useState('');

  // Open file handler
  const openFile = async () => {
    const filePath = await window.electron.openFile();
    if (filePath) {
      setCurrentFilePath(filePath);
      const content = await window.electron.readFile(filePath);
      setEditorContent(content);
    }
  };

  // Save file handler
  const saveFile = async () => {
    if (currentFilePath) {
      await window.electron.saveFile(currentFilePath, editorContent);
      alert('File saved successfully!');
    } else {
      const filePath = await window.electron.saveFileAs(editorContent);
      if (filePath) {
        setCurrentFilePath(filePath);
        alert('File saved successfully!');
      }
    }
  };

  return (
    <div>
      <h1>File Editor</h1>
      <textarea
        value={editorContent}
        onChange={(e) => setEditorContent(e.target.value)}
        placeholder="Open or create a file to start editing..."
        style={{ width: '100%', height: '300px', marginTop: '10px' }}
      />
      <div>
        <button onClick={openFile}>Open File</button>
        <button onClick={saveFile}>Save File</button>
      </div>
    </div>
  );
};

export default FileManager;
