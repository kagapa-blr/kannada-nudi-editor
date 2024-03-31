# import ctypes
# import win32con
# import win32api
# import win32gui
# import pythoncom
# import pyWinhook
#
# # Mapping of English characters to Kannada characters
# kannada_mapping = {
#     'a': 'ಅ', 'b': 'ಬ', 'c': 'ಚ', 'd': 'ದ', 'e': 'ಎ',
#     'f': 'ಫ', 'g': 'ಗ', 'h': 'ಹ', 'i': 'ಇ', 'j': 'ಜ',
#     'k': 'ಕ', 'l': 'ಲ', 'm': 'ಮ', 'n': 'ನ', 'o': 'ಒ',
#     'p': 'ಪ', 'q': 'ಟ', 'r': 'ರ', 's': 'ಸ', 't': 'ತ',
#     'u': 'ಉ', 'v': 'ವ', 'w': 'ಡ', 'x': 'ಷ', 'y': 'ಯ',
#     'z': 'ಞ',
#     'A': 'ಆ', 'B': 'ಭ', 'C': 'ಛ', 'D': 'ಡ',
#     'E': 'ೇ', 'F': '್', 'G': 'ಘ', 'H': 'ಃ', 'I': 'ಈ',
#     'J': 'ಝ', 'K': 'ಖ', 'L': 'ಳ', 'M': 'ಂ', 'N': 'ಣ',
#     'O': 'ಓ', 'P': 'ಫ', 'Q': 'ಠ', 'R': 'ಋ', 'S': 'ಶ',
#     'T': 'ಥ', 'U': 'ಊ', 'V': 'ವ', 'W': 'ಢ', 'X': 'ಕ್ಷ',
#     'Y': 'ಐ', 'Z': 'ಜ್ಞ'
# }
#
# # Function to convert English character to Kannada character
# def convert_to_kannada(char):
#     return kannada_mapping.get(char, char)
#
# # Function to send keyboard input using SendMessage
# def send_keystroke(hwnd, char):
#     for c in char:
#         win32gui.SendMessage(hwnd, win32con.WM_CHAR, ord(c), 0)
#
# # Keyboard event handler
# def OnKeyboardEvent(event):
#     # If a printable character is pressed
#     if event.Ascii > 32 and event.Ascii < 127:
#         # Convert the character to Kannada
#         kannada_char = convert_to_kannada(chr(event.Ascii))
#         # Get the handle of the active window
#         hwnd = win32gui.GetForegroundWindow()
#         # Send the Kannada character
#         send_keystroke(hwnd, kannada_char)
#         # Suppress the original character
#         return False
#     # Otherwise, let the event pass throughC:\Users\Admin\Desktop\kagapa\spellcheker\venv\Scripts
#     return True
#
# # Set up the keyboard hookC:\Users\Admin\Desktop\kagapa\spellcheker\venv\Scripts
# def SetHook():keyboard/system_wide.py:49keyboard/system_wide.py:49
#     hm = pyWinhook.HookManager()
#     hm.KeyDown = OnKeyboardEvent
#     hm.HookKeyboard()
#     pythoncom.PumpMessages()
#
# if __name__ == '__main__':
#     try:
#         SetHook()
#     except Exception as e:
#         print(f"An error occurred: {e}")
