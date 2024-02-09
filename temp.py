import sys

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import QFile, QTextStream


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Text Editor')
        self.setGeometry(100, 100, 600, 400)

        # Create a QTextEdit widget
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Apply CSS styles
        self.loadStyleSheet('resources/static/css/styles.css')

        # Connect textChanged signal to the underlineText method
        self.text_edit.textChanged.connect(self.underlineText)

    def underlineText(self):
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(self.text_edit.currentCharFormat())
        char_format = self.text_edit.currentCharFormat()
        char_format.setUnderlineStyle(1)  # Set underline style
        char_format.setUnderlineColor('#FF0000')  # Set underline color (red)
        cursor.setCharFormat(char_format)

    def loadStyleSheet(self, file_path):
        style_sheet = QFile(file_path)
        if not style_sheet.open(QFile.ReadOnly | QFile.Text):
            return
        style_stream = QTextStream(style_sheet)
        self.setStyleSheet(style_stream.readAll())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
