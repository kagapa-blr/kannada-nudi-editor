export const openFile = (quill) => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".txt";
    fileInput.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const content = event.target.result;
                //const quillEditor = quill.getEditor();  // Access the Quill editor instance
                const delta = quill.clipboard.convert(content); // Convert text to Quill delta
                quill.setContents(delta);  // Set the content using Quill's API
            };
            reader.readAsText(file);
        }
    };
    fileInput.click();
};


// Function to open a .txt file and read its content
export function openText(editor) {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".txt";
    fileInput.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const content = event.target.result;
                // Set the file content to the Quill editor
                editor.root.innerHTML = content;
            };
            reader.readAsText(file);
        }
    };
    fileInput.click();
}

// Function to open a .docx file and extract its text content
export function openDocxFile(editor) {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".docx";
    fileInput.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = async (event) => {
                const arrayBuffer = event.target.result;
                const doc = await extractTextFromDocx(arrayBuffer);
                // Set the extracted text to the Quill editor
                editor.root.innerHTML = doc;
            };
            reader.readAsArrayBuffer(file);
        }
    };
    fileInput.click();
}

// Helper function to extract text from a .docx file using a library (e.g., `mammoth.js`)
async function extractTextFromDocx(arrayBuffer) {
    const mammoth = await import("mammoth");
    try {
        const { value } = await mammoth.extractRawText({ arrayBuffer });
        return value;
    } catch (error) {
        console.error("Error reading .docx file", error);
        return "";
    }
}

// Function to save the content as a .txt file
export function saveTxtFile(editor) {
    const content = editor.root.innerHTML; // Get the editor content
    const blob = new Blob([content], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "document.txt"; // Name of the saved file
    link.click();
}

// Function to save the content as a .docx file
export function saveDocxFile(editor) {
    const content = editor.root.innerHTML; // Get the editor content
    const docxContent = contentToDocx(content);
    const blob = new Blob([docxContent], { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "document.docx"; // Name of the saved file
    link.click();
}

// Helper function to convert HTML content to a .docx format (simplified for demo purposes)
function contentToDocx(content) {
    const html = `
      <html xmlns:w="urn:schemas-microsoft-com:office:word">
        <body>
          ${content}
        </body>
      </html>
    `;
    // Create a simple .docx XML structure (in reality, you'd use a library to create a valid .docx file)
    return new Blob([html], { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" });
}
