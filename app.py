import os
import subprocess
import sys

import psutil
from PyQt5.QtWidgets import QApplication, QDialog

from editor.nudi_editor import NewTextEditor
from editor.widgets.banner import SplashScreen
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
    """Initialize and start the text editor with a splash screen."""
    app = QApplication(sys.argv)

    # Show splash screen
    splash = SplashScreen()
    if splash.exec_() == QDialog.Accepted:  # Wait until user accepts
        # Start background processes
        start_background_exe()
        remove_spaces_in_filenames(folder_path='./resources/static/Nudi_fonts')

        # Load main editor window
        editor_window = NewTextEditor('./resources/images/logo.jpg')
        editor_window.show()

        # Stop background process when app quits
        app.aboutToQuit.connect(stop_background_exe)

        sys.exit(app.exec_())


if __name__ == '__main__':
    editor()
