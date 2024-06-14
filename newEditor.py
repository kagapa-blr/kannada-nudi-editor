from PyQt5.QtCore import pyqtSignal, Qt, QEvent
from PyQt5.QtGui import QTextCursor, QIcon, QFont
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QDialogButtonBox,
                             QHBoxLayout,
                             QWidget, QTextEdit, QSizePolicy, QMainWindow, QScrollArea, QVBoxLayout, QAction, QToolBar,
                             QMenu,
                             QFileDialog, QFontComboBox, QComboBox)

from spellcheck.bloom_filter import bloom_lookup
from utils.util import has_letters_or_digits


class PageLayoutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Page Layout and Size")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

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


class Page(QWidget):
    textOverflow = pyqtSignal()
    clicked = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = QTextEdit(self)
        self.currentZoomFactor = 1.0
        self.initUI()
        self.editor.installEventFilter(self)
        self.editor.textChanged.connect(self.checkOverflow)
        self.editor.focusInEvent = self.onFocusInEvent

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.editor.setFixedSize(int(210 * 96 / 25.4), int(297 * 96 / 25.4))
        self.editor.setCursorWidth(2)
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.editor.setStyleSheet("""
            QTextEdit {
                border: 1px solid #C3BFBE;
                padding: 20px;
                background-color: white;
            }
        """)
        self.editor.setReadOnly(False)
        self.editor.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.editor.setFocusPolicy(Qt.StrongFocus)

        layout.addWidget(self.editor)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

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
        if self.editor.document().size().height() > self.editor.height():
            self.textOverflow.emit()

    def onFocusInEvent(self, event):
        self.clicked.emit(self)
        return QTextEdit.focusInEvent(self.editor, event)


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.pages = []
        self.current_page = None
        self.initUI()

    def initUI(self):
        self.createActions()
        self.createMenus()
        self.createToolbars()
        self.createFormatbar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignHCenter)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.scroll_area.setWidget(self.scroll_content)

        layout.addWidget(self.scroll_area)

        self.addNewPage()
        self.showMaximized()

    def createActions(self):
        self.newAction = QAction(QIcon('resources/images/new.png'), 'New', self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.triggered.connect(self.newFile)

        self.openAction = QAction(QIcon('resources/images/open.png'), 'Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.triggered.connect(self.openFile)

        self.saveAction = QAction(QIcon('resources/images/save.png'), 'Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.triggered.connect(self.saveFile)

        self.printAction = QAction(QIcon('resources/images/print.png'), 'Print', self)
        self.printAction.setShortcut('Ctrl+P')

        self.boldAction = QAction(QIcon('resources/images/bold.png'), 'Bold', self)
        self.boldAction.setShortcut('Ctrl+B')
        self.boldAction.triggered.connect(self.toggleBold)

        self.italicAction = QAction(QIcon('resources/images/italic.png'), 'Italic', self)
        self.italicAction.setShortcut('Ctrl+I')
        self.italicAction.triggered.connect(self.toggleItalic)

        self.underlineAction = QAction(QIcon('resources/images/underline.png'), 'Underline', self)
        self.underlineAction.setShortcut('Ctrl+U')
        self.underlineAction.triggered.connect(self.toggleUnderline)

        self.zoomInAction = QAction(QIcon('resources/images/zoom-in.png'), 'Zoom In', self)
        self.zoomInAction.setShortcut('Ctrl++')
        self.zoomInAction.triggered.connect(self.zoomIn)

        self.zoomOutAction = QAction(QIcon('resources/images/zoom-out.png'), 'Zoom Out', self)
        self.zoomOutAction.setShortcut('Ctrl+-')
        self.zoomOutAction.triggered.connect(self.zoomOut)

    def createMenus(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.printAction)

        editMenu = menubar.addMenu('Edit')
        editMenu.addAction(self.boldAction)
        editMenu.addAction(self.italicAction)
        editMenu.addAction(self.underlineAction)

        viewMenu = menubar.addMenu('View')
        viewMenu.addAction(self.zoomInAction)
        viewMenu.addAction(self.zoomOutAction)

    def createToolbars(self):
        self.toolbar = self.addToolBar('Main Toolbar')
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addAction(self.printAction)

    def createFormatbar(self):
        self.formatbar = self.addToolBar('Format Toolbar')
        self.formatbar.addAction(self.boldAction)
        self.formatbar.addAction(self.italicAction)
        self.formatbar.addAction(self.underlineAction)

        self.fontComboBox = QFontComboBox(self)
        self.fontComboBox.currentFontChanged.connect(self.setFontFamily)
        self.formatbar.addWidget(self.fontComboBox)

        self.fontSizeComboBox = QComboBox(self)
        self.fontSizeComboBox.addItems([str(size) for size in range(8, 49, 2)])
        self.fontSizeComboBox.currentIndexChanged.connect(self.setFontSize)
        self.formatbar.addWidget(self.fontSizeComboBox)

    def addNewPage(self):
        page = Page(self)
        page.textOverflow.connect(self.addNewPage)
        page.clicked.connect(self.setActivePage)
        self.pages.append(page)
        self.scroll_layout.addWidget(page)
        self.setActivePage(page)

    def setActivePage(self, page):
        self.current_page = page

    def newFile(self):
        self.pages.clear()
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.addNewPage()

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)",
                                                  options=options)
        if fileName:
            with open(fileName, 'r', encoding="utf-8") as file:
                content = file.read()
                self.pages[0].editor.setPlainText(content)

    def saveFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)",
                                                  options=options)
        if fileName:
            with open(fileName, 'w') as file:
                content = self.pages[0].editor.toPlainText()
                file.write(content)

    def setFontFamily(self, font):
        if self.current_page:
            self.current_page.editor.setCurrentFont(font)

    def setFontSize(self, index):
        size = int(self.fontSizeComboBox.currentText())
        if self.current_page:
            self.current_page.editor.setFontPointSize(size)

    def toggleBold(self):
        if self.current_page:
            self.current_page.editor.setFontWeight(
                QFont.Bold if self.current_page.editor.fontWeight() != QFont.Bold else QFont.Normal)

    def toggleItalic(self):
        if self.current_page:
            state = self.current_page.editor.fontItalic()
            self.current_page.editor.setFontItalic(not state)

    def toggleUnderline(self):
        if self.current_page:
            state = self.current_page.editor.fontUnderline()
            self.current_page.editor.setFontUnderline(not state)

    def zoomIn(self):
        if self.current_page:
            self.current_page.editor.zoomIn()

    def zoomOut(self):
        if self.current_page:
            self.current_page.editor.zoomOut()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
