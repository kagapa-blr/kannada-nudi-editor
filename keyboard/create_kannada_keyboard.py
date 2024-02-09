from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit

class KannadaTextEdit(QTextEdit):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.textCursor().deletePreviousChar()
        elif event.text():
            english_char = event.text()
            if event.modifiers() & Qt.ShiftModifier:
                kannada_char = self.convert_to_kannada(english_char.upper())
            else:
                kannada_char = self.convert_to_kannada(english_char.lower())
            cursor = self.textCursor()
            cursor.insertText(kannada_char)
        else:
            super().keyPressEvent(event)

    def convert_to_kannada(self, english_char):
        # Mapping of English letters to Kannada letters and combinations
        kannada_letters = {
            'a': 'ಅ', 'b': 'ಬ', 'c': 'ಚ', 'd': 'ದ', 'e': 'ಎ',
            'f': 'ಫ', 'g': 'ಗ', 'h': 'ಹ', 'i': 'ಇ', 'j': 'ಜ',
            'k': 'ಕ', 'l': 'ಲ', 'm': 'ಮ', 'n': 'ನ', 'o': 'ಒ',
            'p': 'ಪ', 'q': 'ಟ', 'r': 'ರ', 's': 'ಸ', 't': 'ತ',
            'u': 'ಉ', 'v': 'ವ', 'w': 'ಡ', 'x': 'ಷ', 'y': 'ಯ',
            'z': 'ಞ',

            'A': 'ಆ', 'B': 'ಭ', 'C': 'ಛ', 'D': 'ಡ',
            'E': 'ೇ', 'F': '್', 'G': 'ಘ', 'H': 'ಃ', 'I': 'ಈ',
            'J': 'ಝ', 'K': 'ಖ', 'L': 'ಳ', 'M': 'ಂ', 'N': 'ಣ',
            'O': 'ಓ', 'P': 'ಫ', 'Q': 'ಠ', 'R': 'ಋ', 'S': 'ಶ',
            'T': 'ಥ', 'U': 'ಊ', 'V': 'ವ', 'W': 'ಢ', 'X': 'ಕ್ಷ',
            'Y': 'ಐ', 'Z': 'ಜ್ಞ'
        }

        # Convert English character to Kannada
        kannada_char = kannada_letters.get(english_char.lower(), english_char)


        if english_char.lower() == 'i' and self.previous_char.lower() in kannada_letters:
            kannada_char = 'ಿ'  # Add diacritic for 'ಿ' when combined with Kannada consonants

        # Update previous character
        if english_char.isalpha():
            self.previous_char = english_char

        return kannada_char
