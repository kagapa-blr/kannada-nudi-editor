from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal, Qt, QEvent
from PyQt5.QtGui import QFont, QFontDatabase, QTextCursor, QTextCharFormat, QContextMenuEvent, QFontMetrics
from PyQt5.QtWidgets import (QDialog, QLabel, QComboBox, QSpinBox, QDialogButtonBox,
                             QHBoxLayout, QInputDialog,
                             QLineEdit)
from PyQt5.QtWidgets import QTextEdit, QScrollArea, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QAction, QMenu

from config import file_path as fp
from editor.components.table_functionality import TableFunctionality
from spellcheck.bloom_filter import bloom_lookup
from spellcheck.symspell_suggestions import suggestionReturner
from utils.corpus_clean import get_clean_words_for_dictionary
from utils.util import has_letters_or_digits


class NewPageLayoutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Page Layout and Size")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        size_label = QLabel("Page Size:", self)
        self.size_combo = QComboBox(self)
        self.size_combo.addItems([
            "A0: 841 x 1189 mm",
            "A1: 594 x 841 mm",
            "A2: 420 x 594 mm",
            "A3: 297 x 420 mm",
            "A4: 210 x 297 mm",
            "A5: 148 x 210 mm",
            "A6: 105 x 148 mm",
            "A7: 74 x 105 mm",
            "A8: 52 x 74 mm",
            "A9: 37 x 52 mm",
            "A10: 26 x 37 mm",
            "B0: 1000 x 1414 mm",
            "B1: 707 x 1000 mm",
            "B2: 500 x 707 mm",
            "B3: 353 x 500 mm",
            "B4: 250 x 353 mm",
            "B5: 176 x 250 mm",
            "B6: 125 x 176 mm",
            "B7: 88 x 125 mm",
            "B8: 62 x 88 mm",
            "B9: 44 x 62 mm",
            "B10: 31 x 44 mm",
            "C0: 917 x 1297 mm",
            "C1: 648 x 917 mm",
            "C2: 458 x 648 mm",
            "C3: 324 x 458 mm",
            "C4: 229 x 324 mm",
            "C5: 162 x 229 mm",
            "C6: 114 x 162 mm",
            "C7: 81 x 114 mm",
            "C8: 57 x 81 mm",
            "C9: 40 x 57 mm",
            "C10: 28 x 40 mm",
            "Letter: 216 x 279 mm",
            "Legal: 216 x 356 mm",
            "Tabloid: 279 x 432 mm",
            "Ledger: 432 x 279 mm",
            "Executive: 184 x 267 mm",
            "Statement: 140 x 216 mm",
            "Folio: 210 x 330 mm",
            "Quarto: 215 x 275 mm",
            "Government Letter: 203 x 267 mm",
            "Government Legal: 216 x 330 mm",
            "Postcard: 100 x 148 mm",
            "Double Postcard: 148 x 200 mm",
            "DL (Envelope): 110 x 220 mm",
            "Custom"
        ])

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
            numeric_parts = [part.strip() for part in size_text.split(':')[1].split('x')]
            width, height = [int(part.split()[0]) for part in numeric_parts]
            return width, height


class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cursorPositionChanged.connect(self.centerCursor)

    def centerCursor(self):
        cursor = self.textCursor()
        rect = self.cursorRect(cursor)
        scroll_area = self.getScrollArea()

        if scroll_area:
            scroll_bar = scroll_area.verticalScrollBar()

            # Calculate cursor's absolute position within the scroll area
            editor_global_pos = self.mapTo(scroll_area.widget(), rect.center())
            target_scroll = editor_global_pos.y() - (scroll_area.height() // 2)

            # Smooth scrolling with a slight delay
            QTimer.singleShot(10, lambda: scroll_bar.setValue(target_scroll))

    def getScrollArea(self):
        """Find the QScrollArea that contains this editor."""
        parent = self.parent()
        while parent:
            if isinstance(parent, QScrollArea):
                return parent
            parent = parent.parent()
        return None


class NewPage(QWidget):
    textOverflow = pyqtSignal()
    clicked = pyqtSignal(QWidget)

    def __init__(self, parent=None, page_number=1):
        super().__init__(parent)
        self.page_number = page_number
        self.is_changed = False  # Add this line
        # self.editor = QTextEdit(self)
        self.editor = CustomTextEdit(self)

        self.currentZoomFactor = 1.0
        self.initUI()
        self.editor.installEventFilter(self)
        self.editor.textChanged.connect(self.checkOverflow)
        self.editor.textChanged.connect(self.changed)  # Connect to changed method
        self.editor.focusInEvent = self.onFocusInEvent

        # We need our own context menu for tables
        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self.context)
        # Instantiate TableFunctionality for table manipulation
        self.table_functionality = TableFunctionality()

    # Add the changed method
    def changed(self):
        self.is_changed = True

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.editor.setFixedSize(int(210 * 96 / 25.4), int(297 * 96 / 25.4))
        self.editor.setCursorWidth(2)
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.editor.setStyleSheet("""
            QTextEdit {
                border: 2px solid #AAA;
                padding: 20px;
                background-color: white;
            }
        """)
        self.editor.setReadOnly(False)
        self.editor.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.editor.setFocusPolicy(Qt.StrongFocus)

        self.page_label = QLabel(f"Page {self.page_number}", self)
        self.page_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.page_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #333;
            font-family: Arial, sans-serif;
        """)

        layout.addWidget(self.editor)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.page_label)

        # Load and set the default font
        font_id = QFontDatabase.addApplicationFont("resources/static/Nudi_fonts/NudiParijatha.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            default_font = QFont(font_family, 12)
            self.editor.setFont(default_font)

    def setPageSize(self, width, height):
        if self.editor is not None:
            self.editor.setFixedSize(int(width * 96 / 25.4), int(height * 96 / 25.4))

    def setZoomFactor(self, factor):
        self.currentZoomFactor = factor
        font = self.editor.font()
        font.setPointSize(int(12 * factor))
        self.editor.setFont(font)

        new_width = int(210 * 96 / 25.4 * factor)
        new_height = int(297 * 96 / 25.4 * factor)
        self.editor.setFixedSize(new_width, new_height)

    def eventFilter(self, obj, event):
        if obj == self.editor and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Space:
                self.spacebarClicked()
                return True
        return super().eventFilter(obj, event)

    def spacebarClicked(self):
        cursor = self.editor.textCursor()
        original_position = cursor.position()

        cursor.insertText(" ")

        cursor.movePosition(QTextCursor.WordLeft, QTextCursor.MoveAnchor)
        cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
        word_left_of_cursor = cursor.selectedText()

        if has_letters_or_digits(word_left_of_cursor):
            print("Correct word")
        elif not bloom_lookup(word_left_of_cursor):
            wrong_word = f'<span style="text-decoration: underline;">{word_left_of_cursor.strip()}</span>'
            html_content = self.editor.toHtml()
            new_html_content = html_content.replace(word_left_of_cursor.lstrip(), wrong_word.strip(), 1)
            self.editor.setHtml(new_html_content)
            new_cursor = self.editor.textCursor()
            new_cursor.setPosition(original_position + 1)
            self.editor.setTextCursor(new_cursor)

    def checkOverflow(self):
        """Detect if text overflows and emit a signal for a new page."""
        font_metrics = QFontMetrics(self.editor.font())
        line_height = font_metrics.lineSpacing()  # Height of one line
        # Calculate usable height
        document_margin = self.editor.contentsMargins()
        padding = 20  # Padding from setStyleSheet

        usable_height = self.editor.height() - document_margin.top() - document_margin.bottom() - (2 * padding)
        max_lines = usable_height // line_height  # Number of lines that fit
        current_lines = self.editor.document().blockCount()  # Current text block count

        if current_lines >= max_lines:  # Check for overflow
            # print("Triggering new page creation due to overflow")
            self.textOverflow.emit()

    def onFocusInEvent(self, event):
        self.clicked.emit(self)
        return QTextEdit.focusInEvent(self.editor, event)

    def context(self, pos):
        # Obtain the cursor at the position
        cursor = self.editor.cursorForPosition(pos)

        # Grab the current table, if there is one
        table = cursor.currentTable()

        # Above will return None if there is no current table
        if table:
            menu = QMenu(self)

            # Instantiate TableFunctionality for table manipulation
            table_functionality = TableFunctionality()

            # Add actions for table manipulation
            appendRowAction = QAction("Append row", self)
            appendRowAction.triggered.connect(lambda: table.appendRows(1))
            appendColAction = QAction("Append column", self)
            appendColAction.triggered.connect(lambda: table.appendColumns(1))
            removeRowAction = QAction("Remove row", self)
            removeRowAction.triggered.connect(lambda: table_functionality.removeRow(table, cursor))
            removeColAction = QAction("Remove column", self)
            removeColAction.triggered.connect(lambda: table_functionality.removeCol(table, cursor))
            insertRowAction = QAction("Insert row", self)
            insertRowAction.triggered.connect(lambda: table_functionality.insertRow(table, cursor))
            insertColAction = QAction("Insert column", self)
            insertColAction.triggered.connect(lambda: table_functionality.insertCol(table, cursor))
            mergeAction = QAction("Merge cells", self)
            mergeAction.triggered.connect(lambda: table_functionality.mergeCells(table, cursor))
            splitAction = QAction("Split cells", self)
            splitAction.triggered.connect(lambda: table_functionality.splitCell(table, cursor))

            # Only allow merging if there is a selection
            if not cursor.hasSelection():
                mergeAction.setEnabled(False)

            # Add actions to the menu
            menu.addAction(appendRowAction)
            menu.addAction(appendColAction)
            menu.addSeparator()
            menu.addAction(removeRowAction)
            menu.addAction(removeColAction)
            menu.addSeparator()
            menu.addAction(insertRowAction)
            menu.addAction(insertColAction)
            menu.addSeparator()
            menu.addAction(mergeAction)
            menu.addAction(splitAction)

            # Show the menu
            menu.exec_(self.editor.mapToGlobal(pos))

        else:
            # Handle word suggestions if no table is found
            cursor.select(QTextCursor.WordUnderCursor)
            selected_word = cursor.selectedText()
            if selected_word:
                menu = QMenu(self)
                if bloom_lookup(selected_word):
                    return
                suggestions = suggestionReturner(selected_word)

                # Create a function to handle word replacement
                def replace_word_with_suggestion(suggestion):
                    cursor.removeSelectedText()
                    cursor.insertText(suggestion)

                # Add each suggestion to the context menu and connect them to the replacement function
                for suggestion in suggestions:
                    action = menu.addAction(suggestion)
                    action.triggered.connect(lambda _, s=suggestion: replace_word_with_suggestion(s))

                # Add actions for adding to dictionary, ignoring, and replacing
                add_to_dict_action = menu.addAction("Add to Dictionary")
                ignore_action = menu.addAction("Ignore")
                replace_action = menu.addAction("Replace All")

                # Connect actions to corresponding functions
                add_to_dict_action.triggered.connect(lambda: self.addToDictionary(selected_word))
                ignore_action.triggered.connect(lambda: self.ignore_word())
                replace_action.triggered.connect(lambda: self.replace_word(selected_word))

                # Show the menu
                menu.exec_(self.editor.mapToGlobal(pos))
            else:
                # If no selection, call the default context menu event
                event = QContextMenuEvent(QContextMenuEvent.Mouse, pos)
                self.editor.contextMenuEvent(event)

    def addToDictionary(self, word):
        try:
            with open(fp.bloomfilter_data, 'a', encoding='utf-8') as dict_file:
                word = get_clean_words_for_dictionary(word)
                if not bloom_lookup(word):
                    dict_file.write(word + '\n')
                    with open(fp.symspell_word_freq_data, 'a', encoding='utf-8') as file:
                        file.write(f"{word} {1}\n")
                        print(word, "successfully Added to Dictionary")

                    # Remove underline from the word
                    cursor = self.editor.textCursor()
                    cursor.beginEditBlock()  # Begin editing block to improve performance
                    format = QTextCharFormat()
                    format.setForeground(self.editor.palette().color(self.editor.foregroundRole()))
                    format.setUnderlineStyle(QTextCharFormat.NoUnderline)  # Clear underline
                    cursor.mergeCharFormat(format)
                    cursor.endEditBlock()
                else:
                    print("word already present in Dictionary file")
        except Exception as e:
            print("Error adding word to dictionary:", str(e))

    def ignore_word(self):
        try:
            cursor = self.editor.textCursor()
            cursor.beginEditBlock()  # Begin editing block to improve performance

            format = QTextCharFormat()
            format.setForeground(self.editor.palette().color(self.editor.foregroundRole()))

            # Clear underline
            format.setUnderlineStyle(QTextCharFormat.NoUnderline)

            cursor.mergeCharFormat(format)
            cursor.endEditBlock()
        except Exception as e:
            print("Error ignoring word:", str(e))

    def replace_word(self, selected_word):
        try:
            cursor = self.editor.textCursor()
            if not cursor.hasSelection():
                return  # No text selected, nothing to replace

            new_word, ok = QInputDialog.getText(self, 'Replace Word',
                                                f'Enter the new word to replace "{selected_word}":',
                                                QLineEdit.Normal)
            if ok and new_word:
                cursor.insertText(new_word)
                cursor.removeSelectedText()
        except Exception as e:
            print("Error replacing word:", str(e))

    def setPageNumber(self, number):
        self.page_number = number
        self.page_label.setText(f"Page {self.page_number}")

    def setPageMargins(self, left=96, right=96, top=96, bottom=96):
        """Apply page margins dynamically to both layout and editor."""

        # Apply to main layout
        self.layout().setContentsMargins(left, top, right, bottom)

        # Apply padding inside QTextEdit
        self.editor.setStyleSheet(f"""
            QTextEdit {{
                border: 2px solid #AAA;
                padding: {top}px {right}px {bottom}px {left}px;
                background-color: white;
            }}
        """)
