from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QTextEdit

class KannadaTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.previous_char = ''

    def is_space(self, key):
        if key ==True:
            self.previous_char = " "

        #return None


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.textCursor().deletePreviousChar()
        elif event.text():
            english_char = event.text()
            if event.modifiers() & Qt.ShiftModifier:
                kannada_char = self.convert_to_kannada(english_char)
            else:
                kannada_char = self.convert_to_kannada(english_char.lower())
            cursor = self.textCursor()
            cursor.insertText(kannada_char)

        else:
            super().keyPressEvent(event)

    def convert_to_kannada(self, english_char):
        vowels = {
            'a': 'ಅ', 'A': 'ಆ', 'i': 'ಇ', 'I': 'ಈ', 'u': 'ಉ', 'U': 'ಊ', 'R': 'ಋ',
            'e': 'ಎ', 'E': 'ಏ', 'Y': 'ಐ', 'o': 'ಒ', 'O': 'ಓ', 'V': 'ಔ'
        }

        consonants = {
            'k': 'ಕ', 'K': 'ಖ', 'g': 'ಗ', 'G': 'ಘ', 'Z': 'ಙ',
            'c': 'ಚ', 'C': 'ಛ', 'j': 'ಜ', 'J': 'ಝ', 'z': 'ಞ',
            'q': 'ಟ', 'Q': 'ಠ', 'w': 'ಡ', 'W': 'ಢ', 'N': 'ಣ',
            't': 'ತ', 'T': 'ಥ', 'd': 'ದ', 'D': 'ಧ', 'n': 'ನ',
            'p': 'ಪ', 'P': 'ಫ', 'b': 'ಬ', 'B': 'ಭ', 'm': 'ಮ',
            'y': 'ಯ', 'r': 'ರ', 'l': 'ಲ', 'v': 'ವ',
            'S': 'ಶ', 'x': 'ಷ', 's': 'ಸ', 'h': 'ಹ', 'L': 'ಳ',
            'f': '್'
        }

        diacritics_dict = {
            'A': 'ಾ',
            'i': 'ಿ',
            'I': 'ೀ',
            'e': 'ಿ',
            'E': 'ೀ',
            'u': 'ು',
            'U': 'ೂ',
            'e': 'ೆ',
            'E': 'ೇ',
            'Y': 'ೈ',
            'o': 'ೊ',
            'O': 'ೋ',
            'V': 'ೌ',
            'M': 'ಂ',
            'H': 'ಃ',
            'f': '್',
            'X':'಼'


        }
        numbers = {
            '0': '೦',
            '1': '೧',
            '2': '೨',
            '3': '೩',
            '4': '೪',
            '5': '೫',
            '6': '೬',
            '7': '೭',
            '8': '೮',
            '9': '೯',
            '10': '೧೦',
            # Add more numbers as needed
        }

        all_letters = {}
        all_letters.update(vowels)
        all_letters.update(consonants)


        kannada_char = all_letters.get(english_char, english_char)


        if self.previous_char in vowels and english_char =='f':
            return None
        if self.previous_char ==" "  and english_char =='f':
            return None

        if self.previous_char == ' ' and english_char in diacritics_dict and english_char in vowels:
            # If the previous character is a space and the current character is a diacritic, do nothing
            kannada_char = vowels.get(english_char)
            return kannada_char

        if english_char.isdigit():  # Check if the character is a digit
            kannada_char = numbers.get(english_char)
            return kannada_char

        # If the previous character is a consonant and the current character is a diacritic
        if self.previous_char in consonants and english_char in diacritics_dict:
            # Combine the consonant with the current diacritic
            kannada_char = diacritics_dict[english_char]
            return kannada_char

        # Update previous character
        if english_char.isalpha():
            self.previous_char = english_char

        return kannada_char
