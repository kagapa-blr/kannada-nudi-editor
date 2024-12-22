// src/services/editorUtils.js

export const getWordAtPosition = (text, position) => {
    const specialChars = "!@#$%^&*()_+[]{}|;:',.<>/?~-=\\\"";
    let start = position;
    let end = position;

    while (start > 0 && !/\s/.test(text[start - 1]) && !specialChars.includes(text[start - 1])) {
        start--;
    }

    while (end < text.length && !/\s/.test(text[end]) && !specialChars.includes(text[end])) {
        end++;
    }

    return text.substring(start, end);
};

export const underlineWordInEditor = (quill, word) => {
    const index = quill.getText().indexOf(word);
    if (index !== -1) {
        quill.formatText(index, word.length, { underline: true, color: 'red', bold: true });
    }
};

export const replaceWord = (quill, clickedWord, replacement) => {
    const index = quill.getText().indexOf(clickedWord);
    if (index !== -1) {
        quill.formatText(index, clickedWord.length, { underline: false, color: '' });
        quill.deleteText(index, clickedWord.length);
        quill.insertText(index, replacement);
        quill.setSelection(index + replacement.length, 0);
    }
};

export const addDictionary = async (clickedWord) => {
    // Add your implementation for adding the word to the dictionary here
};

export const ignoreAll = (quill, clickedWord) => {
    const fullText = quill.getText();
    let index = fullText.indexOf(clickedWord);
    if (index !== -1) {
        while (index !== -1) {
            quill.formatText(index, clickedWord.length, { underline: false, color: '' });
            index = fullText.indexOf(clickedWord, index + clickedWord.length);
        }
    }
};

// Define valid consonants (ವ್ಯಂಜನ) and vowels (ಸ್ವರಗಳು)
const validConsonants = new Set([
    "ಕ", "ಖ", "ಗ", "ಘ", "ಙ", "ಚ", "ಛ", "ಜ", "ಝ", "ಞ", "ಟ", "ಠ", "ಡ", "ಢ", "ಣ", "ತ", "ಥ", "ದ", "ಧ", "ನ",
    "ಪ", "ಫ", "ಬ", "ಭ", "ಮ", "ಯ", "ರ", "ಲ", "ವ", "ಶ", "ಷ", "ಸ", "ಹ", "ಳ", "ಕ್ಷ", "ಜ್ಞ"
]);

const validVowels = new Set([
    "ಅ", "ಆ", "ಇ", "ಈ", "ಉ", "ಊ", "ಋ", "ಎ", "ಏ", "ಐ", "ಒ", "ಓ", "ಔ", "ಂ", "ಃ"
]);

function isKannadaCharacter(char) {
    // Check if the character is in the Kannada Unicode range
    return char >= '\u0C80' && char <= '\u0CFF';
}

export function isSingleCharacter(word) {
    // Normalize the input to handle any leading/trailing whitespace
    word = word.trim();
    
    // Validate that the word contains only Kannada characters
    if ([...word].every(isKannadaCharacter)) {
        
        // Directly check if the word is a valid consonant or vowel
        if (validConsonants.has(word) || validVowels.has(word)) {
            return true;
        }

        // Split the word using the Halant (್) as the delimiter
        const parts = word.split("");

        // Count all valid Kannada characters (consonants and vowels)
        const characterCount = parts.reduce((count, part) => {
            return count + [...part].filter(char => validConsonants.has(char) || validVowels.has(char)).length;
        }, 0);

        // Return true if the total character count is 1, false otherwise
        return characterCount === 1;
    }
}

export function ignoreSingleChars(words) {
    // Convert a single string to an array
    if (typeof words === 'string') {
        words = [words];
    }

    return words.filter(word => {
        try {
            return !isSingleCharacter(word); // Return true for words that are not single characters
        } catch (error) {
            console.error(error.message);
            return true; // Include invalid words in the results
        }
    });
}