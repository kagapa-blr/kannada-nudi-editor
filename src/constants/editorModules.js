import { PAGE_SIZES } from "./pageSizes";
import { getWrongWords } from "../spellcheck/bloomFilter";
import {
    underlineWordInEditor,

} from "../services/editorService";


// Undo and redo functions for Custom Toolbar
function undoChange() {
    this.quill.history.undo();
}

function redoChange() {
    this.quill.history.redo();
}


export const openFile = () => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".txt";
    fileInput.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const content = event.target.result;
                const quill = document.querySelector(".ql-editor"); // Get the Quill editor instance
                quill.innerHTML = content; // Set the file content to the editor
            };
            reader.readAsText(file);
        }
    };
    fileInput.click();
};

const saveFile = () => {
    const content = document.querySelector(".ql-editor").innerHTML; // Get the editor content
    const blob = new Blob([content], { type: "text/html" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "document.txt"; // Name of the saved file
    link.click();
};

const refreshButton = () => {
    console.log('handle function defined separately');
}

// Modules object for setting up the Quill editor
export const modules = {
    toolbar: {
        container: "#toolbar",
        handlers: {
            undo: undoChange,
            redo: redoChange,
            // Custom handler for page size
            "page-size": function (value) {
                const selectedSize = PAGE_SIZES[value];
                if (selectedSize) {
                    this.quill.root.style.width = `${selectedSize.width}px`;
                    this.quill.root.style.minHeight = `${selectedSize.height}px`;
                }
            },
            "refresh-button": refreshButton,
            // Add custom handlers for font and size
            font: function (value) {
                if (value) {
                    this.quill.format("font", value);
                }
            },
            size: function (value) {
                if (value) {
                    this.quill.format("size", value);
                }
            },
            // Open file handler
            open: openFile,
            // Save file handler
            save: saveFile,


        },
    },
    history: {
        delay: 500,
        maxStack: 100,
        userOnly: true,
    },
    // Add the resize module here
    resize: {},
};
