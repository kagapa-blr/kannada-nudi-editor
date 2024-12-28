const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const fs = require('fs')
const path = require('path')
const url = require('url')


let win;

// Create a new window
function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),  // Ensure the correct path for preload.js
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // Load the index.html of the app
  win.loadFile(path.join(__dirname, 'index.html'));  // Use __dirname to load index.html from the correct path
}

// Handle opening a file
ipcMain.handle('dialog:openFile', async () => {
  const result = await dialog.showOpenDialog(win, {
    properties: ['openFile'],
  });
  return result.filePaths[0];
});

// Handle reading a file
ipcMain.handle('file:read', async (event, filePath) => {
  const data = fs.readFileSync(filePath, 'utf-8');
  return data;
});

// Handle saving a file
ipcMain.handle('file:save', async (event, filePath, content) => {
  fs.writeFileSync(filePath, content, 'utf-8');
  return true;
});

// Handle Save As (Save File Dialog)
ipcMain.handle('dialog:saveFileAs', async (event, content) => {
  const result = await dialog.showSaveDialog(win, {
    defaultPath: 'untitled.txt', // Default filename
  });
  if (result.filePath) {
    // Save the file at the specified location
    fs.writeFileSync(result.filePath, content, 'utf-8');
    return result.filePath;  // Return the file path where the content was saved
  }
  return null;  // If the user cancels the save dialog
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
