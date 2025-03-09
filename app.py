import os
import subprocess
import sys

import psutil
from PyQt5.QtWidgets import QApplication, QDialog

from editor.nudi_editor import NewTextEditor
from editor.widgets.banner import SplashScreen
from logger import setup_logger
from utils.util import remove_spaces_in_filenames

logger = setup_logger(logger_name='main_app')


def stop_background_exe():
    """Stop the Kannada Nudi Keyboard process if running."""
    try:
        for proc in psutil.process_iter():
            if "kannadakeyboard.exe" in proc.name().lower():  # Case-insensitive check
                proc.terminate()
                logger.info("Kannada Nudi Keyboard stopped successfully.")
                return
        logger.info("Kannada Nudi Keyboard is not running.")
    except Exception as e:
        logger.info(f"Error stopping background exe: {e}")


def start_background_exe():
    """Start the Kannada Nudi Keyboard process."""
    if sys.platform.startswith("linux"):
        logger.info("Linux system detected. The executable will not be started.")
        return

    exe_path = os.path.abspath(os.path.join("resources", "keyboardDriver", "kannadaKeyboard.exe"))

    if not os.path.exists(exe_path):
        logger.info(f"Error: Kannada Keyboard executable not found at {exe_path}")
        return

    try:
        subprocess.Popen([exe_path], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         start_new_session=True)
        logger.info("Kannada Nudi Keyboard loaded and running in background.")
    except Exception as e:
        logger.info(f"Error starting background exe: {e}")
        stop_background_exe()  # Stop background exe if an error occurs


def editor():
    """Initialize and start the text editor with a splash screen."""
    app = QApplication(sys.argv)

    # Show splash screen
    splash = SplashScreen()
    if splash.exec_() == QDialog.Accepted:  # Wait until user accepts
        try:
            # Start background processes
            start_background_exe()
            remove_spaces_in_filenames(folder_path='./resources/static/Nudi_fonts')

            # Load main editor window
            editor_window = NewTextEditor('./resources/images/logo.jpg')
            editor_window.show()

            # Stop background process when app quits
            app.aboutToQuit.connect(stop_background_exe)

            sys.exit(app.exec_())

        except Exception as e:
            logger.info(f"An error occurred: {e}")
            stop_background_exe()  # Stop background exe if an error occurs


if __name__ == '__main__':
    try:
        editor()
    except Exception as e:
        logger.info(f"Critical error: {e}")
        stop_background_exe()  # Stop background exe if a critical error occurs
