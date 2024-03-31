import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit

from logger import setup_logger

# class KannadaTextEdit(QTextEdit):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.previous_char = ''
#
#     def is_space(self, key):
#         if key:
#             self.previous_char = " "
#
#     def keyPressEvent(self, event):
#
#         if event.key() == Qt.Key_Backspace:
#             self.textCursor().deletePreviousChar()
#             self.previous_char=" "
#         elif event.text():
#             english_char = event.text()
#             if event.modifiers() & Qt.ShiftModifier:
#                 kannada_char = self.convert_to_kannada(english_char)
#             else:
#                 kannada_char = self.convert_to_kannada(english_char.lower())
#             cursor = self.textCursor()
#             cursor.insertText(kannada_char)
#
#         else:
#             super().keyPressEvent(event)
#
#     def convert_to_kannada(self, english_char):
#         vowels = {
#             'a': 'ಅ', 'A': 'ಆ', 'i': 'ಇ', 'I': 'ಈ', 'u': 'ಉ', 'U': 'ಊ', 'R': 'ಋ',
#             'e': 'ಎ', 'E': 'ಏ', 'Y': 'ಐ', 'o': 'ಒ', 'O': 'ಓ', 'V': 'ಔ'
#         }
#         consonants = {
#             'k': 'ಕ', 'K': 'ಖ', 'g': 'ಗ', 'G': 'ಘ', 'Z': 'ಙ',
#             'c': 'ಚ', 'C': 'ಛ', 'j': 'ಜ', 'J': 'ಝ', 'z': 'ಞ',
#             'q': 'ಟ', 'Q': 'ಠ', 'w': 'ಡ', 'W': 'ಢ', 'N': 'ಣ',
#             't': 'ತ', 'T': 'ಥ', 'd': 'ದ', 'D': 'ಧ', 'n': 'ನ',
#             'p': 'ಪ', 'P': 'ಫ', 'b': 'ಬ', 'B': 'ಭ', 'm': 'ಮ',
#             'y': 'ಯ', 'r': 'ರ', 'l': 'ಲ', 'v': 'ವ',
#             'S': 'ಶ', 'x': 'ಷ', 's': 'ಸ', 'h': 'ಹ', 'L': 'ಳ',
#             'f': '್','M': 'ಂ',
#         }
#         diacritics_dict = {
#             'A': 'ಾ',
#             'i': 'ಿ',
#             'I': 'ೀ',
#             'e': 'ೆ',
#             'E': 'ೇ',
#             'u': 'ು',
#             'U': 'ೂ',
#             'Y': 'ೈ',
#             'o': 'ೊ',
#             'O': 'ೋ',
#             'V': 'ೌ',
#             'H': 'ಃ',
#             'f': '್',
#             'X': '಼'
#         }
#         numbers = {
#             '0': '೦',
#             '1': '೧',
#             '2': '೨',
#             '3': '೩',
#             '4': '೪',
#             '5': '೫',
#             '6': '೬',
#             '7': '೭',
#             '8': '೮',
#             '9': '೯',
#             '10': '೧೦',
#             # Add more numbers as needed
#         }
#
#         all_letters = {}
#         all_letters.update(vowels)
#         all_letters.update(consonants)
#
#         print("previous characters", self.previous_char)
#         print("english char: ", english_char)
#
#         if english_char == '\b':  # Check if backspace is pressed
#             if self.previous_char is not None:
#                 # If there's a character to the left of the cursor, move cursor left
#                 self.previous_char = " "
#             return None
#
#         kannada_char = all_letters.get(english_char, english_char)
#
#         if self.previous_char in vowels and english_char == 'f':
#             return None
#         if self.previous_char == " " and english_char == 'f':
#             return None
#         if self.previous_char in diacritics_dict and english_char == 'f':
#             return None
#
#         if self.previous_char == ' ' and english_char in diacritics_dict and english_char in vowels:
#             # If the previous character is a space and the current character is a diacritic, do nothing
#             kannada_char = vowels.get(english_char)
#             return kannada_char
#
#         if english_char.isdigit():  # Check if the character is a digit
#             kannada_char = numbers.get(english_char)
#             return kannada_char
#
#         # If the previous character is a consonant and the current character is a diacritic
#         if self.previous_char in consonants and english_char in diacritics_dict:
#             # Combine the consonant with the current diacritic
#             kannada_char = diacritics_dict[english_char]
#             return kannada_char
#
#         # Update previous character
#         if english_char.isalpha():
#             self.previous_char = english_char
#
#         return kannada_char


# class KannadaTextEdit(QTextEdit):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.previous_char = ''
#
#     def is_space(self, key):
#         if key:
#             self.previous_char = " "
#
#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_Backspace:
#             self.textCursor().deletePreviousChar()
#             self.previous_char = " "
#         elif event.text():
#             english_char = event.text()
#             if event.modifiers() & Qt.ShiftModifier:
#                 kannada_char = self.convert_to_kannada(english_char)
#             else:
#                 kannada_char = self.convert_to_kannada(english_char.lower())
#             cursor = self.textCursor()
#             cursor.insertText(kannada_char)
#         else:
#             super().keyPressEvent(event)
#
#     def convert_to_kannada(self, english_char):
#         vowels = {
#             'a': '\u0C85', 'A': '\u0C86', 'i': '\u0C87', 'I': '\u0C88', 'u': '\u0C89', 'U': '\u0C8A', 'R': '\u0C8B',
#             'e': '\u0C8E', 'E': '\u0C8F', 'Y': '\u0C90', 'o': '\u0C92', 'O': '\u0C93', 'V': '\u0C94'
#         }
#         consonants = {
#             'k': '\u0C95', 'K': '\u0C96', 'g': '\u0C97', 'G': '\u0C98', 'Z': '\u0C99',
#             'c': '\u0C9A', 'C': '\u0C9B', 'j': '\u0C9C', 'J': '\u0C9D', 'z': '\u0C9E',
#             'q': '\u0CA1', 'Q': '\u0CA2', 'w': '\u0CA3', 'W': '\u0CA4', 'N': '\u0CA3',
#             't': '\u0CA4', 'T': '\u0CA5', 'd': '\u0CA6', 'D': '\u0CA7', 'n': '\u0CA8',
#             'p': '\u0CAA', 'P': '\u0CAB', 'b': '\u0CAC', 'B': '\u0CAD', 'm': '\u0CAE',
#             'y': '\u0CAF', 'r': '\u0CB0', 'l': '\u0CB2', 'v': '\u0CB5',
#             'S': '\u0CB6', 'x': '\u0CB7', 's': '\u0CB8', 'h': '\u0CB9', 'L': '\u0CB3',
#             'f': '\u0CCD','M': '\u0C82',
#         }
#         diacritics_dict = {
#             'A': '\u0CBE',
#             'i': '\u0CBF',
#             'I': '\u0CC0',
#             'e': '\u0CC6',
#             'E': '\u0CC7',
#             'u': '\u0CC1',
#             'U': '\u0CC2',
#             'Y': '\u0CC8',
#             'o': '\u0CCA',
#             'O': '\u0CCB',
#             'V': '\u0CCC',
#             'H': '\u0C83',
#             'f': '\u0CCD',
#             'X': '\u0CBC'
#         }
#         numbers = {
#             '0': '\u0CE6',
#             '1': '\u0CE7',
#             '2': '\u0CE8',
#             '3': '\u0CE9',
#             '4': '\u0CEA',
#             '5': '\u0CEB',
#             '6': '\u0CEC',
#             '7': '\u0CED',
#             '8': '\u0CEE',
#             '9': '\u0CEF',
#             '10': '\u0CE6\u0CE7',
#             # Add more numbers as needed
#         }
#
#         all_letters = {}
#         all_letters.update(vowels)
#         all_letters.update(consonants)
#
#         # print("previous characters", self.previous_char)
#         # print("english char: ", english_char)
#
#         if english_char == '\b':  # Check if backspace is pressed
#             if self.previous_char is not None:
#                 # If there's a character to the left of the cursor, move cursor left
#                 self.previous_char = " "
#             return None
#
#         kannada_char = all_letters.get(english_char, english_char)
#
#         if self.previous_char in vowels and english_char == 'f':
#             return None
#         if self.previous_char == " " and english_char == 'f':
#             return None
#         if self.previous_char in diacritics_dict and english_char == 'f':
#             return None
#
#         if self.previous_char == ' ' and english_char in diacritics_dict and english_char in vowels:
#             # If the previous character is a space and the current character is a diacritic, do nothing
#             kannada_char = vowels.get(english_char)
#             return kannada_char
#
#         if english_char.isdigit():  # Check if the character is a digit
#             kannada_char = numbers.get(english_char)
#             return kannada_char
#
#         # If the previous character is a consonant and the current character is a diacritic
#         if self.previous_char in consonants and english_char in diacritics_dict:
#             # Combine the consonant with the current diacritic
#             kannada_char = diacritics_dict[english_char]
#             return kannada_char
#
#         # Update previous character
#         if english_char.isalpha():
#             self.previous_char = english_char
#
#         return kannada_char
#


# Get the filename of the current file
filename = os.path.splitext(os.path.basename(__file__))[0]

# Set up logger
logger = setup_logger(filename)


class KannadaTextEdit(QTextEdit):
    logger.info("Kannada keyboard started..")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.previous_char = ''

    def is_space(self, key):
        if key:
            self.previous_char = " "

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.textCursor().deletePreviousChar()
            self.previous_char = " "
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
            'a': '\u0C85',  # ಅ
            'A': '\u0C86',  # ಆ
            'i': '\u0C87',  # ಇ
            'I': '\u0C88',  # ಈ
            'u': '\u0C89',  # ಉ
            'U': '\u0C8A',  # ಊ
            'R': '\u0C8B',  # ಋ
            'e': '\u0C8E',  # ಎ
            'E': '\u0C8F',  # ಏ
            'Y': '\u0C90',  # ಐ
            'o': '\u0C92',  # ಒ
            'O': '\u0C93',  # ಓ
            'V': '\u0C94'  # ಔ
        }
        consonants = {
            'k': '\u0C95',  # ಕ
            'K': '\u0C96',  # ಖ
            'g': '\u0C97',  # ಗ
            'G': '\u0C98',  # ಘ
            'Z': '\u0C99',  # ಙ
            'c': '\u0C9A',  # ಚ
            'C': '\u0C9B',  # ಛ
            'j': '\u0C9C',  # ಜ
            'J': '\u0C9D',  # ಝ
            'z': '\u0C9E',  # ಞ
            'q': '\u0CA1',  # ಟ
            'Q': '\u0CA2',  # ಠ
            'w': '\u0CA3',  # ಡ
            'W': '\u0CA4',  # ಢ
            'N': '\u0CA3',  # ಣ
            't': '\u0CA4',  # ತ
            'T': '\u0CA5',  # ಥ
            'd': '\u0CA6',  # ದ
            'D': '\u0CA7',  # ಧ
            'n': '\u0CA8',  # ನ
            'p': '\u0CAA',  # ಪ
            'P': '\u0CAB',  # ಫ
            'b': '\u0CAC',  # ಬ
            'B': '\u0CAD',  # ಭ
            'm': '\u0CAE',  # ಮ
            'y': '\u0CAF',  # ಯ
            'r': '\u0CB0',  # ರ
            'l': '\u0CB2',  # ಲ
            'v': '\u0CB5',  # ವ
            'S': '\u0CB6',  # ಶ
            'x': '\u0CB7',  # ಷ
            's': '\u0CB8',  # ಸ
            'h': '\u0CB9',  # ಹ
            'L': '\u0CB3',  # ಳ
            'f': '\u0CCD',  # ್
            'M': '\u0C82',  # ಂ
            'H': '\u0C83',  # ಃ
        }
        diacritics_dict = {
            'A': '\u0CBE',  # ಾ
            'i': '\u0CBF',  # ಿ
            'I': '\u0CC0',  # ೀ
            'e': '\u0CC6',  # ೆ
            'E': '\u0CC7',  # ೇ
            'u': '\u0CC1',  # ು
            'U': '\u0CC2',  # ೂ
            'Y': '\u0CC8',  # ೈ
            'o': '\u0CCA',  # ೊ
            'O': '\u0CCB',  # ೋ
            'V': '\u0CCC',  # ೌ
            'f': '\u0CCD',  # ್
            'X': '\u0CBC'  # ಼ '಼'
        }
        numbers = {
            '0': '\u0CE6',  # ೦
            '1': '\u0CE7',  # ೧
            '2': '\u0CE8',  # ೨
            '3': '\u0CE9',  # ೩
            '4': '\u0CEA',  # ೪
            '5': '\u0CEB',  # ೫
            '6': '\u0CEC',  # ೬
            '7': '\u0CED',  # ೭
            '8': '\u0CEE',  # ೮
            '9': '\u0CEF',  # ೯
            # Add more numbers as needed
        }

        all_letters = {}
        all_letters.update(vowels)
        all_letters.update(consonants)

        # print("previous char: ", self.previous_char)
        # print("current char:", english_char)

        if english_char == '\b':  # Check if backspace is pressed
            if self.previous_char is not None:
                # If there's a character to the left of the cursor, move cursor left
                self.previous_char = " "
            return None

        kannada_char = all_letters.get(english_char, english_char)

        # case 1
        if self.previous_char in diacritics_dict and english_char == 'f':
            print("case 1 ", self.previous_char)
            return None

        # case 2
        if self.previous_char in vowels and english_char == 'f':
            print("case 2 ", self.previous_char)
            return None

        # case 3
        if self.previous_char == " " and english_char == 'f':
            print("case 3 ", self.previous_char)
            return None

        # case 4
        if self.previous_char == ' ' and english_char in diacritics_dict and english_char in vowels:
            # If the previous character is a space and the current character is a diacritic, do nothing
            kannada_char = vowels.get(english_char)
            print("case 4 ", self.previous_char)
            return kannada_char
        # case 5
        if english_char.isdigit():  # Check if the character is a digit
            kannada_char = numbers.get(english_char)
            print("case 5 ", self.previous_char)
            return kannada_char

        # case 6
        # If the previous character is a consonant and the current character is a diacritic
        if self.previous_char in consonants and english_char in diacritics_dict:
            # Combine the consonant with the current diacritic
            kannada_char = diacritics_dict[english_char]
            print("case 6 ", self.previous_char)
            return kannada_char

        # case 7
        if self.previous_char in vowels and english_char in consonants:
            kannada_char = consonants[english_char]
            print("case 7 ", self.previous_char)
            return kannada_char

        # Update previous character
        if english_char.isalpha():
            self.previous_char = english_char

        return kannada_char
