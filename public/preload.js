const { contextBridge, ipcRenderer } = require('electron');

// Expose file operations to the renderer process
contextBridge.exposeInMainWorld('electron', {
  openFile: () => ipcRenderer.invoke('dialog:openFile'),
  readFile: (filePath) => ipcRenderer.invoke('file:read', filePath),
  saveFile: (filePath, content) => ipcRenderer.invoke('file:save', filePath, content),
  saveFileAs: (content) => ipcRenderer.invoke('dialog:saveFileAs', content), // New function to handle Save As
});
