const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const fs = require('fs');
const path = require('path');

let win;

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // Preload script
      nodeIntegration: false, // Disable Node.js integration in renderer
      contextIsolation: true, // Isolate context for security
    },
  });

  win.loadFile(path.join(__dirname, 'index.html'));
}

// Open file dialog
ipcMain.handle('dialog:openFile', async () => {
  const result = await dialog.showOpenDialog({
    properties: ['openFile'],
  });
  if (result.filePaths.length > 0) {
    return result.filePaths[0]; // Return the file path
  }
  return null;
});

// Save file dialog
ipcMain.handle('dialog:saveFileAs', async (event, content) => {
  const result = await dialog.showSaveDialog({
    filters: [{ name: 'Text Files', extensions: ['txt'] }],
  });
  if (result.filePath) {
    fs.writeFileSync(result.filePath, content); // Write content to file
    return result.filePath;
  }
  return null;
});

// Save existing file
ipcMain.handle('dialog:saveFile', (event, filePath, content) => {
  fs.writeFileSync(filePath, content); // Save content to the given file
  return true;
});

// Read file content
ipcMain.handle('file:readFile', (event, filePath) => {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return content;
  } catch (error) {
    console.error('Error reading file:', error);
    return null;
  }
});





// Append content to a file (with directory check)
ipcMain.handle('file:appendContent', (event, filePath, content) => {
  try {
    // Resolve the absolute path for the dictionary file
    const absolutePath = path.resolve(filePath);

    // Ensure the directory exists before appending to the file
    const dir = path.dirname(absolutePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true }); // Create the directory if it doesn't exist
    }

    // Append content to the file
    fs.appendFileSync(absolutePath, content);
    return true; // Indicate success
  } catch (error) {
    console.error('Error appending to file:', error);
    return false; // Indicate failure
  }
});





app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
