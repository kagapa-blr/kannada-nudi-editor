import sys

from PyQt5.QtWidgets import QApplication
from editor.nudi_editor import TextEditor


def editor():
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    editor()
