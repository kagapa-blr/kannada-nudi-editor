import fs from 'fs';
import path from 'path';
import { dialog } from 'electron';
// Function to open a file dialog and get the file path
export const openFile = () => {
  return new Promise((resolve, reject) => {

    dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [{ name: 'Text Files', extensions: ['txt'] }],
    }).then(result => {
      if (result.canceled) {
        resolve(null);
      } else {
        resolve(result.filePaths[0]);
      }
    }).catch(reject);
  });
};

// Function to read the file content
export const readFile = (filePath) => {
  return new Promise((resolve, reject) => {
    fs.readFile(filePath, 'utf-8', (err, data) => {
      if (err) {
        reject(err);
      } else {
        resolve(data);
      }
    });
  });
};

// Function to save file content
export const saveFile = (filePath, content) => {
  return new Promise((resolve, reject) => {
    fs.writeFile(filePath, content, 'utf-8', (err) => {
      if (err) {
        reject(err);
      } else {
        resolve(true);
      }
    });
  });
};
