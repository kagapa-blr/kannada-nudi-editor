const { app, BrowserWindow, Menu, dialog, ipcMain } = require("electron");
const fs = require("fs");
const path = require("path");

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "./main/preload.js"),
      nodeIntegration: true, // Allow nodeIntegration if needed
    },
  });

  win.loadFile("src/renderer/index.html");

  // Define Menu Template
  const menuTemplate = [
    {
      label: "File",
      submenu: [
        {
          label: "New",
          accelerator: "CmdOrCtrl+N",
          click: () => {
            console.log("New file created");
            // Logic for new file creation
          },
        },
        {
          label: "Open",
          accelerator: "CmdOrCtrl+O",
          click: () => {
            // Open file dialog
            dialog.showOpenDialog({
              properties: ['openFile'],
              filters: [
                { name: 'Text Files', extensions: ['txt'] },
                { name: 'Word Files', extensions: ['docx'] },
                { name: 'PDF Files', extensions: ['pdf'] }
              ]
            }).then(result => {
              if (!result.canceled) {
                const filePath = result.filePaths[0];
                // Read file and send it to the renderer
                fs.readFile(filePath, 'utf-8', (err, data) => {
                  if (err) {
                    console.error("Error reading file:", err);
                  } else {
                    // Send file content to renderer
                    win.webContents.send('file-opened', data);
                  }
                });
              }
            }).catch(err => {
              console.log("Failed to open file:", err);
            });
          },
        },
        {
          label: "Save",
          accelerator: "CmdOrCtrl+S",
          click: () => {
            console.log("Save file");
            // Logic for saving file (e.g., save as docx, txt, or pdf)
          },
        },
        { type: "separator" },
        {
          label: "Exit",
          accelerator: "CmdOrCtrl+Q",
          click: () => {
            app.quit();
          },
        },
      ],
    },
    {
      label: "Edit",
      submenu: [
        {
          label: "Undo",
          accelerator: "CmdOrCtrl+Z",
          role: "undo",
        },
        {
          label: "Redo",
          accelerator: "Shift+CmdOrCtrl+Z",
          role: "redo",
        },
        { type: "separator" },
        {
          label: "Cut",
          accelerator: "CmdOrCtrl+X",
          role: "cut",
        },
        {
          label: "Copy",
          accelerator: "CmdOrCtrl+C",
          role: "copy",
        },
        {
          label: "Paste",
          accelerator: "CmdOrCtrl+V",
          role: "paste",
        },
      ],
    },
    {
      label: "Help",
      submenu: [
        {
          label: "About",
          click: () => {
            console.log("About the application");
            // Implement About dialog if needed
          },
        },
      ],
    },
  ];

  // Create Menu from Template
  const menu = Menu.buildFromTemplate(menuTemplate);
  Menu.setApplicationMenu(menu);
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
