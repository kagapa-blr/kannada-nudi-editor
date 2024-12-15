//src/services/editorService.js

const specialChars = ['.', ',', '!', '?', ';', ':']; // Define any special characters you want to exclude

// Function to get the word at a given position in the text
const getWordAtPosition = (text, position) => {
    let start = position;
    let end = position;

    while (
        start > 0 &&
        !/\s/.test(text[start - 1]) &&
        !specialChars.includes(text[start - 1])
    ) {
        start--;
    }

    while (
        end < text.length &&
        !/\s/.test(text[end]) &&
        !specialChars.includes(text[end])
    ) {
        end++;
    }

    return text.substring(start, end);
};

const underlineWordInEditor = (quill, word) => {
    const text = quill.getText();
    // This regex matches the word and allows for punctuation or whitespace around it
    const regex = new RegExp(`([^\\w]|^)(${word})([^\\w]|$)`, "g");
    let match;

    // Apply underline formatting for each occurrence of the word
    while ((match = regex.exec(text)) !== null) {
        const index = match.index + match[1].length; // Start at the word index (after any non-word character)
        const length = match[2].length; // Length of the actual word

        // Apply the underline formatting
        quill.formatText(index, length, {
            underline: true,
        });
    }

    // Add the red underline class if needed
    const spans = document.querySelectorAll('.ql-editor u');
    spans.forEach((span) => {
        if (span.innerText.trim() === word) {
            span.classList.add('red-underline'); // Add the red underline class
        }
    });
};

// Add custom CSS for the red underline, keeping the text color unchanged
const style = document.createElement('style');
style.innerHTML = `
  .red-underline {
    text-decoration: underline;
    text-decoration-color: red;  /* Only the underline will be red */
    text-decoration-thickness: 3px;  /* Adjust underline thickness if needed */
  }
`;
document.head.appendChild(style);


// Function to remove special characters from the word
const cleanWord = (word) => {
    // Define a regex that matches special characters
    const specialCharRegex = /[^\w\u0C80-\u0CFF]+/g; // Includes Kannada unicode range and allows alphanumeric characters
    return word.replace(specialCharRegex, "");
};


export {
    getWordAtPosition,
    cleanWord,
    underlineWordInEditor,
};