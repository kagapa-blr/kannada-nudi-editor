import sys

from PyQt5.QtWidgets import QApplication
from editor.nudi_editor import TextEditor
#from editor.nudi_editor_backup import TextEditorBackup


def editor():
    app = QApplication(sys.argv)
    editor = TextEditor()
    #editor = TextEditorBackup()
    editor.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    editor()
