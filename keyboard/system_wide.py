import ctypes
import time
import pythoncom
import pyWinhook as pyHook

# Define required constants
KEYEVENTF_UNICODE = 0x0004


class KannadaConverter:
    def __init__(self):
        self.previous_char = None


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


    def send_input(self, char):
        # Prepare the input event for the character
        key_event = pyHook.KeyboardEvent(0, ord(char), KEYEVENTF_UNICODE, 0, 0, 0, "WindowName")

        # Send the input event
        pyHook.HookManager.PulseEvent(key_event)

    def on_keyboard_event(self, event):
        # Check if the event is a key press event and not a system key event
        if event.MessageName == 'key down' and event.Ascii >= 32 and event.Ascii <= 126:
            # Convert the ASCII code to character
            english_char = chr(event.Ascii)
            # Perform Kannada conversion
            kannada_char = self.convert_to_kannada(english_char)
            # If Kannada character is available, send it as input
            if kannada_char:
                self.send_input(kannada_char)
                # Give some time for the system to process the input
                time.sleep(0.01)

        # Pass the event to the next hook in the chain
        return True


# Example usage:
converter = KannadaConverter()

# Create a hook manager
hm = pyHook.HookManager()
# Define the keyboard event handler
hm.KeyDown = converter.on_keyboard_event
# Set the hook
hm.HookKeyboard()

# Start the event loop
pythoncom.PumpMessages()
