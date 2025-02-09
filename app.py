import os
import subprocess
import sys
import psutil
from PyQt5.QtWidgets import QApplication
from editor.nudi_editor import NewTextEditor
from utils.util import remove_spaces_in_filenames

def stop_background_exe():
    """Stop the Kannada Nudi Keyboard process if running."""
    try:
        for proc in psutil.process_iter():
            if "kannadakeyboard.exe" in proc.name().lower():  # Case-insensitive check
                proc.terminate()
                print("Kannada Nudi Keyboard stopped successfully.")
                return
        print("Kannada Nudi Keyboard is not running.")
    except Exception as e:
        print(f"Error stopping background exe: {e}")

def start_background_exe():
    """Start the Kannada Nudi Keyboard process."""
    if sys.platform.startswith("linux"):
        print("Linux system detected. The executable will not be started.")
        return

    exe_path = os.path.abspath(os.path.join("resources", "keyboardDriver", "kannadaKeyboard.exe"))

    if not os.path.exists(exe_path):
        print(f"Error: Kannada Keyboard executable not found at {exe_path}")
        return

    try:
        subprocess.Popen([exe_path], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        print("Kannada Nudi Keyboard loaded and running in background.")
    except Exception as e:
        print(f"Error starting background exe: {e}")

def editor():
    """Initialize and start the text editor."""
    nudi_logo_icon = './resources/images/logo.jpg'
    start_background_exe()
    remove_spaces_in_filenames(folder_path='./resources/static/Nudi_fonts')

    app = QApplication(sys.argv)
    editor_window = NewTextEditor(nudi_logo_icon)
    editor_window.show()

    app.aboutToQuit.connect(stop_background_exe)
    sys.exit(app.exec_())

if __name__ == '__main__':
    editor()
