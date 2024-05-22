from PyQt5.QtCore import pyqtSignal, Qt, QEvent
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QSizePolicy

from spellcheck.bloom_filter import bloom_lookup
from utils.util import has_letters_or_digits

class Page(QWidget):
    activeEditorChanged = pyqtSignal(QTextEdit)
    textOverflow = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentZoomFactor = 1.0
        self.initUI()
        self.editor.installEventFilter(self)

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # Margins around the page

        self.editor = QTextEdit(self)
        self.editor.setFixedSize(int(210 * 96 / 25.4), int(297 * 96 / 25.4))  # A4 size
        self.editor.setCursorWidth(2)  # Set cursor width
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable vertical scrollbar
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable horizontal scrollbar
        self.editor.setStyleSheet("""
            QTextEdit {
                border: 2px solid black; /* Set border */
            }
        """)
        self.editor.setReadOnly(False)  # Set read-only mode to False
        self.editor.setTextInteractionFlags(Qt.TextEditorInteraction)  # Enable text interaction
        self.editor.setFocusPolicy(Qt.StrongFocus)  # Enable focus

        layout.addWidget(self.editor)

        # Ensure the parent widget's layout does not allow expanding beyond fixed size
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def setZoomFactor(self, factor):
        self.currentZoomFactor = factor
        font = self.editor.font()
        font.setPointSize(int(12 * factor))  # Convert the result to an integer
        self.editor.setFont(font)

        # Adjust page size based on zoom factor
        new_width = int(210 * 96 / 25.4 * factor)
        new_height = int(297 * 96 / 25.4 * factor)
        self.editor.setFixedSize(new_width, new_height)

    def eventFilter(self, obj, event):
        if obj == self.editor and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Space:
                self.spacebarClicked()
                return True  # Event handled
        return super().eventFilter(obj, event)

    def spacebarClicked(self):
        cursor = self.editor.textCursor()
        original_position = cursor.position()

        # Insert a space
        cursor.insertText(" ")

        # Move cursor to the left of the inserted space
        cursor.movePosition(QTextCursor.WordLeft, QTextCursor.MoveAnchor)

        # Select the entire word to the left of the cursor
        cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
        word_left_of_cursor = cursor.selectedText()

        if has_letters_or_digits(word_left_of_cursor):
            print("Correct word")
        elif not bloom_lookup(word_left_of_cursor):
            # Trim the selected word
            wrong_word = f'<span style="text-decoration: underline;">{word_left_of_cursor.strip()}</span>'
            html_content = self.editor.toHtml()
            new_html_content = html_content.replace(word_left_of_cursor.lstrip(), wrong_word.strip(), 1)
            # Set the new HTML content
            self.editor.setHtml(new_html_content)

            # Restore the cursor to the original position plus one (after the inserted space)
            new_cursor = self.editor.textCursor()
            new_cursor.setPosition(original_position + 1)
            self.editor.setTextCursor(new_cursor)
