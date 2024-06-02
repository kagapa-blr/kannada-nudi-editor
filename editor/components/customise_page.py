from PyQt5.QtCore import pyqtSignal, Qt, QEvent
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QDialogButtonBox, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QTextEdit, QSizePolicy

from spellcheck.bloom_filter import bloom_lookup
from utils.util import has_letters_or_digits


class PageLayoutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Page Layout and Size")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Page size options
        size_label = QLabel("Page Size:", self)
        self.size_combo = QComboBox(self)
        self.size_combo.addItems(["A4: 210 x 297 mm",
                                  "A3: 297 x 420 mm",
                                  "A5: 148 x 210 mm",
                                  "B4: 250 x 353 mm",
                                  "B5: 176 x 250 mm",
                                  "Letter: 216 x 279 mm",
                                  "Legal: 216 x 356 mm",
                                  "Tabloid: 279 x 432 mm",
                                  "Executive: 184 x 267 mm",
                                  "Custom"])

        # Width and height for custom size
        custom_layout = QHBoxLayout()
        self.width_spinbox = QSpinBox(self)
        self.width_spinbox.setRange(1, 10000)
        self.width_spinbox.setSuffix(" mm")
        self.width_spinbox.setEnabled(False)

        self.height_spinbox = QSpinBox(self)
        self.height_spinbox.setRange(1, 10000)
        self.height_spinbox.setSuffix(" mm")
        self.height_spinbox.setEnabled(False)

        custom_layout.addWidget(QLabel("Width:"))
        custom_layout.addWidget(self.width_spinbox)
        custom_layout.addWidget(QLabel("Height:"))
        custom_layout.addWidget(self.height_spinbox)

        self.size_combo.currentIndexChanged.connect(self.onSizeComboChanged)

        layout.addWidget(size_label)
        layout.addWidget(self.size_combo)
        layout.addLayout(custom_layout)

        # OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

    def onSizeComboChanged(self, index):
        if self.size_combo.currentText() == "Custom":
            self.width_spinbox.setEnabled(True)
            self.height_spinbox.setEnabled(True)
        else:
            self.width_spinbox.setEnabled(False)
            self.height_spinbox.setEnabled(False)

    def getPageSize(self):
        if self.size_combo.currentText() == "Custom":
            return self.width_spinbox.value(), self.height_spinbox.value()
        else:
            size_text = self.size_combo.currentText()
            # Extract numeric parts from the size text
            numeric_parts = [part.strip() for part in size_text.split(':')[1].split('x')]
            # Convert numeric parts to integers
            width, height = [int(part.split()[0]) for part in numeric_parts]
            return width, height


class Page(QWidget):
    activeEditorChanged = pyqtSignal(QTextEdit)
    textOverflow = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = QTextEdit(self)
        self.currentZoomFactor = 1.0
        self.initUI()
        self.editor.installEventFilter(self)

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # Margins around the page

        self.editor.setFixedSize(int(210 * 96 / 25.4), int(297 * 96 / 25.4))  # A4 size
        self.editor.setCursorWidth(2)  # Set cursor width
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable vertical scrollbar
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable horizontal scrollbar
        self.editor.setStyleSheet("""
            QTextEdit {
                border: 1px solid #C3BFBE; /* Add border with specified color */
                padding: 20px; /* Add padding to the text */
                background-color: white; /* Set background color to white */
            }
        """)
        self.editor.setReadOnly(False)  # Set read-only mode to False
        self.editor.setTextInteractionFlags(Qt.TextEditorInteraction)  # Enable text interaction
        self.editor.setFocusPolicy(Qt.StrongFocus)  # Enable focus

        layout.addWidget(self.editor)

        # Ensure the parent widget's layout does not allow expanding beyond fixed size
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def setPageSize(self, width, height):
        if self.editor is not None:
            self.editor.setFixedSize(int(width * 96 / 25.4), int(height * 96 / 25.4))

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