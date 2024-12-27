import { app, BrowserWindow } from 'electron';
import { join } from 'path';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: join(__dirname, 'preload.js'), // Ensure preload script path is correct
    },
  });

  // Determine the path to the index.html
  const isDev = !app.isPackaged; // Check if the app is running in development mode
  let indexPath;

  if (isDev) {
    // Development mode: use the direct file path
    indexPath = join(__dirname, '../dist/index.html');
  } else {
    // Production mode: use the ASAR archive and resources path
    indexPath = join(process.resourcesPath, 'app.asar', 'dist', 'index.html');
  }

  console.log('Index path:', indexPath);

  // Load the index.html file
  mainWindow.loadURL(`file://${indexPath}`);

  // Uncomment to open Developer Tools in development mode
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }
};

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
