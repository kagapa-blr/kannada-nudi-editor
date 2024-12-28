const { contextBridge, ipcRenderer } = require('electron');

// Expose safe APIs to the renderer
contextBridge.exposeInMainWorld('electron', {
  openFile: () => ipcRenderer.invoke('dialog:openFile'),
  saveFileAs: (content) => ipcRenderer.invoke('dialog:saveFileAs', content),
  saveFile: (filePath, content) => ipcRenderer.invoke('dialog:saveFile', filePath, content),
  readFile: (filePath) => ipcRenderer.invoke('file:readFile', filePath),
  appendContent: (filePath, content) => ipcRenderer.invoke('file:appendContent', filePath, content), // New append method
});
