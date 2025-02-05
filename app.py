import sys

import psutil
from PyQt5.QtWidgets import QApplication
#from editor.nudi_editor import TextEditor
from newEditor2 import NewTextEditor
from utils.util import remove_spaces_in_filenames


#from editor.nudi_editor_backup import TextEditorBackup
def stop_background_exe():
    try:
        for proc in psutil.process_iter():
            if "kannadaKeyboard.exe" in proc.name():
                proc.terminate()
                print("Kannada Nudi Keyboard stopped successfully.")
                return
        print("Kannada Nudi Keyboard is not running.")
    except Exception as e:
        print(f"Error stopping background exe: {e}")

def editor():
    remove_spaces_in_filenames(folder_path='./resources/static/Nudi_fonts')
    app = QApplication(sys.argv)
    editor = NewTextEditor()
    #editor = TextEditorBackup()
    editor.show()
    app.aboutToQuit.connect(stop_background_exe)
    sys.exit(app.exec_())


if __name__ == '__main__':
    editor()
