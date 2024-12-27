import { existsSync, readFileSync, writeFileSync } from 'fs';

/**
 * Read and append content to a file.
 * @param {string} filePath - The file path.
 * @param {string} contentToAppend - Content to append.
 * @returns {string} Success message.
 */
export function readAndAppendFile(filePath, contentToAppend) {
  try {
    const existingContent = existsSync(filePath) ? readFileSync(filePath, 'utf8') : '';
    const updatedContent = existingContent + contentToAppend;
    writeFileSync(filePath, updatedContent, 'utf8');
    return 'File updated successfully!';
  } catch (error) {
    throw new Error(`Failed to update the file: ${error.message}`);
  }
}
