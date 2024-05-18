import os
import subprocess

from PyQt5 import QtCore
from PyQt5 import QtPrintSupport
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QFileInfo, QEvent
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextDocument, QTextDocumentWriter, QPainter, QTextCursor, QTextCharFormat, QIcon
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QFileDialog, QMenu, QMessageBox, QInputDialog, QLineEdit
from docx import Document

from config import file_path as fp
from editor.components.customize_image import ImageEditDialog
from logger import setup_logger
from spellcheck.bloom_filter import bloom_lookup, reload_bloom_filter, start_bloom
from spellcheck.symspell_suggestions import suggestionReturner
from utils import find, datetime, table, wordcount
from utils.corpus_clean import get_clean_words_for_dictionary
from utils.util import has_letters_or_digits

filename = os.path.splitext(os.path.basename(__file__))[0]

# Set up logger
logger = setup_logger(filename)


def start_background_exe():
    exe_path = r"resources\keyboardDriver\kannadaKeyboard.exe"  # Path to your executable relative to the current directory
    #exe_path = r"resources\keyboardDriver\testing.exe"
    try:
        # Use subprocess.Popen to start the executable in the background
        print("kannada Nudi Keyboard loaded and running in background")
        subprocess.Popen([exe_path], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         start_new_session=True)

    except Exception as e:
        print(f"Error starting background exe: {e}")


class TextEditor(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self, parent)

        self.filename = None

        self.changesSaved = True

        self.initUI()

    def initToolbar(self):

        self.newAction = QtWidgets.QAction(QtGui.QIcon("resources/images/new-file.png"), "ಹೊಸ ಕಡತ", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create a new document from scratch.")
        self.newAction.triggered.connect(self.new)

        self.openAction = QtWidgets.QAction(QtGui.QIcon("resources/images/open-file.png"), "ಕಡತ ತೆರೆಯಿರಿ", self)
        self.openAction.setStatusTip("Open existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtWidgets.QAction(QtGui.QIcon("resources/images/stock_save.png"), "Save", self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.saveAsAction = QtWidgets.QAction(QtGui.QIcon("resources/images/stock_save.png"), "Save As...", self)
        self.saveAsAction.setStatusTip("Save document with a new name")
        self.saveAsAction.setShortcut("Ctrl+Shift+S")
        self.saveAsAction.triggered.connect(self.save_as)

        self.printAction = QtWidgets.QAction(QtGui.QIcon("resources/images/print.png"), "Print document", self)
        self.printAction.setStatusTip("Print document")
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.triggered.connect(self.printHandler)

        self.previewAction = QtWidgets.QAction(QtGui.QIcon("resources/images/preview.png"), "Page view", self)
        self.previewAction.setStatusTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)

        self.findAction = QtWidgets.QAction(QtGui.QIcon("resources/images/find.png"), "Find and replace", self)
        self.findAction.setStatusTip("Find and replace words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(find.Find(self).show)

        self.cutAction = QtWidgets.QAction(QtGui.QIcon("resources/images/stock_cut.png"), "Cut to clipboard", self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.editor.cut)

        self.copyAction = QtWidgets.QAction(QtGui.QIcon("resources/images/stock_copy.png"), "Copy to clipboard", self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.editor.copy)

        self.pasteAction = QtWidgets.QAction(QtGui.QIcon("resources/images/stock_paste.png"), "Paste from clipboard",
                                             self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.editor.paste)

        self.undoAction = QtWidgets.QAction(QtGui.QIcon("resources/images/undo.png"), "Undo last action", self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.editor.undo)

        self.redoAction = QtWidgets.QAction(QtGui.QIcon("resources/images/redo.png"), "Redo last undone thing", self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.editor.redo)

        dateTimeAction = QtWidgets.QAction(QtGui.QIcon("resources/images/calender.png"), "Insert current date/time",
                                           self)
        dateTimeAction.setStatusTip("Insert current date/time")
        dateTimeAction.setShortcut("Ctrl+D")
        dateTimeAction.triggered.connect(datetime.DateTime(self).show)

        wordCountAction = QtWidgets.QAction(QtGui.QIcon("resources/images/count.png"), "See word/symbol count", self)
        wordCountAction.setStatusTip("See word/symbol count")
        wordCountAction.setShortcut("Ctrl+W")
        wordCountAction.triggered.connect(self.wordCount)

        tableAction = QtWidgets.QAction(QtGui.QIcon("resources/images/insert-table.png"), "Insert table", self)
        tableAction.setStatusTip("Insert table")
        tableAction.setShortcut("Ctrl+T")
        tableAction.triggered.connect(table.Table(self).show)

        imageAction = QtWidgets.QAction(QtGui.QIcon("resources/images/add-image.png"), "Insert image", self)
        imageAction.setStatusTip("Insert image")
        imageAction.setShortcut("Ctrl+Shift+I")
        imageAction.triggered.connect(self.choose_image)

        bulletAction = QtWidgets.QAction(QtGui.QIcon("resources/images/bullet-list.png"), "Insert bullet List", self)
        bulletAction.setStatusTip("Insert bullet list")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList)

        numberedAction = QtWidgets.QAction(QtGui.QIcon("resources/images/number-list.png"), "Insert numbered List",
                                           self)
        numberedAction.setStatusTip("Insert numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)

        refresh_action = QtWidgets.QAction(QtGui.QIcon('resources/images/refresh.png'), 'Refresh and Recheck', self)
        refresh_action.setStatusTip("Refresh and Recheck")
        refresh_action.triggered.connect(self.refresh_recheck)
        #refresh_action.addAction(refresh_action)

        self.toolbar = self.addToolBar("Options")
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addAction(self.saveAsAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.findAction)
        self.toolbar.addAction(dateTimeAction)
        self.toolbar.addAction(wordCountAction)
        self.toolbar.addAction(tableAction)
        self.toolbar.addAction(imageAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(bulletAction)
        self.toolbar.addAction(numberedAction)
        self.toolbar.addAction(refresh_action)

        self.addToolBarBreak()

    def initFormatbar(self):

        fontBox = QtWidgets.QFontComboBox(self)
        fontBox.currentFontChanged.connect(lambda font: self.editor.setCurrentFont(font))

        # Set default font to "Nudist Parijath"
        default_font = QtGui.QFont("nudiParijatha")
        fontBox.setCurrentFont(default_font)

        fontSize = QtWidgets.QSpinBox(self)

        # Will display " pt" after each value
        fontSize.setSuffix(" pt")

        fontSize.valueChanged.connect(lambda size: self.editor.setFontPointSize(size))

        fontSize.setValue(14)

        fontColor = QtWidgets.QAction(QtGui.QIcon("resources/images/font-color.png"), "Change font color", self)
        fontColor.triggered.connect(self.fontColorChanged)

        boldAction = QtWidgets.QAction(QtGui.QIcon("resources/images/bold.png"), "Bold", self)
        boldAction.triggered.connect(self.bold)

        italicAction = QtWidgets.QAction(QtGui.QIcon("resources/images/italic.png"), "Italic", self)
        italicAction.triggered.connect(self.italic)

        underlAction = QtWidgets.QAction(QtGui.QIcon("resources/images/underline.png"), "Underline", self)
        underlAction.triggered.connect(self.underline)

        strikeAction = QtWidgets.QAction(QtGui.QIcon("resources/images/strike.png"), "Strike-out", self)
        strikeAction.triggered.connect(self.strike)

        superAction = QtWidgets.QAction(QtGui.QIcon("resources/images/superscript.png"), "Superscript", self)
        superAction.triggered.connect(self.superScript)

        subAction = QtWidgets.QAction(QtGui.QIcon("resources/images/subscript.png"), "Subscript", self)
        subAction.triggered.connect(self.subScript)

        alignLeft = QtWidgets.QAction(QtGui.QIcon("resources/images/align-left.png"), "Align left", self)
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QtWidgets.QAction(QtGui.QIcon("resources/images/align-center.png"), "Align center", self)
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QtWidgets.QAction(QtGui.QIcon("resources/images/align-right.png"), "Align right", self)
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QtWidgets.QAction(QtGui.QIcon("resources/images/align-justify.png"), "Align justify", self)
        alignJustify.triggered.connect(self.alignJustify)

        indentAction = QtWidgets.QAction(QtGui.QIcon("resources/images/indent.png"), "Indent Area", self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.indent)

        dedentAction = QtWidgets.QAction(QtGui.QIcon("resources/images/dedent.png"), "Dedent Area", self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.dedent)

        backColor = QtWidgets.QAction(QtGui.QIcon("resources/images/highlight.png"), "Change background color", self)
        backColor.triggered.connect(self.highlight)

        self.formatbar = self.addToolBar("Format")

        self.formatbar.addWidget(fontBox)
        self.formatbar.addWidget(fontSize)

        self.formatbar.addSeparator()

        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)

        self.formatbar.addSeparator()

        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addAction(strikeAction)
        self.formatbar.addAction(superAction)
        self.formatbar.addAction(subAction)

        self.formatbar.addSeparator()

        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)

        self.formatbar.addSeparator()

        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)

    def initMenubar(self):

        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        # Add the most important actions to the menubar

        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.saveAsAction)
        file.addAction(self.printAction)
        file.addAction(self.previewAction)

        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)
        edit.addAction(self.findAction)

        # Toggling actions for the various bars
        toolbarAction = QtWidgets.QAction("Toggle Toolbar", self)
        toolbarAction.triggered.connect(self.toggleToolbar)

        formatbarAction = QtWidgets.QAction("Toggle Formatbar", self)
        formatbarAction.triggered.connect(self.toggleFormatbar)

        statusbarAction = QtWidgets.QAction("Toggle Statusbar", self)
        statusbarAction.triggered.connect(self.toggleStatusbar)

        view.addAction(toolbarAction)
        view.addAction(formatbarAction)
        view.addAction(statusbarAction)

    def initUI(self):

        self.editor = QtWidgets.QTextEdit(self)
        start_background_exe()

        # Set the tab stop width to around 33 pixels which is
        # more or less 8 spaces
        self.editor.setTabStopWidth(33)

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        self.setCentralWidget(self.editor)

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # If the cursor position changes, call the function that displays
        # the line and column number
        self.editor.cursorPositionChanged.connect(self.cursorPosition)

        # We need our own context menu for tables
        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self.context)

        self.editor.textChanged.connect(self.changed)
        self.editor.installEventFilter(self)

        self.setGeometry(100, 100, 1030, 800)

        self.setWindowTitle("ಕನ್ನಡ ನುಡಿ - " + self.access_filename())
        #self.setWindowIcon(QtGui.QIcon("resources/images/icon.jpg"))
        self.setWindowIcon(QIcon('resources/images/logo.jpg'))  # Set the application icon

        #self.show()

    def changed(self):
        self.changesSaved = False

    def closeEvent(self, event):

        if self.changesSaved:

            event.accept()

        else:

            popup = QtWidgets.QMessageBox(self)
            popup.setIcon(QtWidgets.QMessageBox.Warning)
            popup.setWindowTitle("ಕನ್ನಡ ನುಡಿ")  # Set the title here
            popup.setText("ಡಾಕ್ಯುಮೆಂಟ್ ಅನ್ನು ಮಾರ್ಪಡಿಸಲಾಗಿದೆ")

            popup.setInformativeText("ನಿಮ್ಮ ಬದಲಾವಣೆಗಳನ್ನು ಉಳಿಸಲು ನೀವು ಬಯಸುವಿರಾ?")

            popup.setStandardButtons(QtWidgets.QMessageBox.Save |
                                     QtWidgets.QMessageBox.Cancel |
                                     QtWidgets.QMessageBox.Discard)

            popup.setDefaultButton(QtWidgets.QMessageBox.Save)

            answer = popup.exec_()

            if answer == QtWidgets.QMessageBox.Save:
                self.save()

            elif answer == QtWidgets.QMessageBox.Discard:
                event.accept()

            else:
                event.ignore()

    def context(self, pos):

        # Grab the cursor
        cursor = self.editor.textCursor()

        # Grab the current table, if there is one
        table = cursor.currentTable()

        # Above will return 0 if there is no current table, in which case
        # we call the normal context menu. If there is a table, we create
        # our own context menu specific to table interaction
        if table:

            menu = QMenu(self)

            appendRowAction = QtWidgets.QAction("Append row", self)
            appendRowAction.triggered.connect(lambda: table.appendRows(1))

            appendColAction = QtWidgets.QAction("Append column", self)
            appendColAction.triggered.connect(lambda: table.appendColumns(1))

            removeRowAction = QtWidgets.QAction("Remove row", self)
            removeRowAction.triggered.connect(self.removeRow)

            removeColAction = QtWidgets.QAction("Remove column", self)
            removeColAction.triggered.connect(self.removeCol)

            insertRowAction = QtWidgets.QAction("Insert row", self)
            insertRowAction.triggered.connect(self.insertRow)

            insertColAction = QtWidgets.QAction("Insert column", self)
            insertColAction.triggered.connect(self.insertCol)

            mergeAction = QtWidgets.QAction("Merge cells", self)
            mergeAction.triggered.connect(lambda: table.mergeCells(cursor))

            # Only allow merging if there is a selection
            if not cursor.hasSelection():
                mergeAction.setEnabled(False)

            splitAction = QtWidgets.QAction("Split cells", self)

            cell = table.cellAt(cursor)

            # Only allow splitting if the current cell is larger
            # than a normal cell
            if cell.rowSpan() > 1 or cell.columnSpan() > 1:

                splitAction.triggered.connect(lambda: table.splitCell(cell.row(), cell.column(), 1, 1))

            else:
                splitAction.setEnabled(False)

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

            # Convert the widget coordinates into global coordinates
            pos = self.mapToGlobal(pos)

            # Add pixels for the tool and formatbars, which are not included
            # in mapToGlobal(), but only if the two are currently visible and
            # not toggled by the user

            if self.toolbar.isVisible():
                pos.setY(pos.y() + 45)

            if self.formatbar.isVisible():
                pos.setY(pos.y() + 45)

            # Move the menu to the new position
            menu.move(pos)

            menu.show()

        if cursor.hasSelection():
            cursor = self.editor.cursorForPosition(pos)
            cursor.select(QTextCursor.WordUnderCursor)
            selected_word = cursor.selectedText()
            if bloom_lookup(selected_word):
                return
            suggestions = suggestionReturner(selected_word)
            if selected_word:
                menu = QMenu(self)

                # Create a function to handle the word replacement
                def replace_word_with_suggestion(suggestion):
                    cursor.removeSelectedText()
                    cursor.insertText(suggestion)

                # Add each suggestion to the context menu and connect them to the replacement function
                for suggestion in suggestions:
                    action = menu.addAction(suggestion)
                    action.triggered.connect(lambda _, s=suggestion: replace_word_with_suggestion(s))

                add_to_dict_action = menu.addAction("Add to Dictionary")
                ignore_action = menu.addAction("Ignore")
                replace_action = menu.addAction("Replace All")

                # Connect actions to corresponding functions
                add_to_dict_action.triggered.connect(lambda: self.addToDictionary(selected_word))
                ignore_action.triggered.connect(lambda: self.ignore_word(selected_word))
                replace_action.triggered.connect(lambda: self.replace_word(selected_word))

                menu.exec_(self.editor.mapToGlobal(pos))
        else:

            event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse, QtCore.QPoint())

            self.editor.contextMenuEvent(event)

    def removeRow(self):

        # Grab the cursor
        cursor = self.editor.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's row
        table.removeRows(cell.row(), 1)

    def removeCol(self):

        # Grab the cursor
        cursor = self.editor.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's column
        table.removeColumns(cell.column(), 1)

    def insertRow(self):

        # Grab the cursor
        cursor = self.editor.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertRows(cell.row(), 1)

    def insertCol(self):

        # Grab the cursor
        cursor = self.editor.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Insert a new row at the cell's position
        table.insertColumns(cell.column(), 1)

    def toggleToolbar(self):

        state = self.toolbar.isVisible()

        # Set the visibility to its inverse
        self.toolbar.setVisible(not state)

    def toggleFormatbar(self):

        state = self.formatbar.isVisible()

        # Set the visibility to its inverse
        self.formatbar.setVisible(not state)

    def toggleStatusbar(self):

        state = self.statusbar.isVisible()

        # Set the visibility to its inverse
        self.statusbar.setVisible(not state)

    def new(self):

        spawn = TextEditor()

        spawn.show()

    def open(self):
        # Define the file filter
        filter = "Text Files (*.txt);;Word Documents (*.docx);;Rich Text Files (*.rtf)"
        # Get filename using QFileDialog
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open File', ".", filter)
        print("filename: ", self.filename)

        if self.filename:
            # Open and read the selected file based on its extension
            try:
                if self.filename.endswith('.txt'):
                    with open(self.filename, 'r', encoding='utf-8') as file:
                        self.editor.setText(file.read())
                elif self.filename.endswith('.rtf'):
                    with open(self.filename, 'r') as file:
                        rtf_text = file.read()
                        document = QTextDocument()
                        document.setHtml(rtf_text)
                        self.editor.setDocument(document)
                elif self.filename.endswith('.docx'):
                    document = Document(self.filename)
                    text = []
                    for paragraph in document.paragraphs:
                        text.append(paragraph.text)
                    self.editor.setText('\n'.join(text))
                else:
                    QMessageBox.critical(self, 'Error', 'Unsupported file format')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error opening file: {str(e)}')

        self.setWindowTitle("ಕನ್ನಡ ನುಡಿ - " + self.access_filename())

    def save(self):
        try:
            if not self.filename:
                # If no filename is set, prompt the user to choose a file location for saving
                self.filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '',
                                                               filter="All Files (*);;RTF Files (*.rtf);;DOCX Files (*.docx);;PDF Files (*.pdf);;Text Files (*.txt)")

                if not self.filename:  # User cancelled the dialog
                    return

                # Determine the file extension and set the appropriate filter
                file_info = QFileInfo(self.filename)
                file_suffix = file_info.suffix().lower()
                if file_suffix not in ['rtf', 'docx', 'pdf', 'txt']:
                    QMessageBox.critical(self, 'Error', 'Unsupported file format.')
                    return

            # Create a QTextDocument and set the HTML content from QTextEdit
            document = QTextDocument()
            document.setHtml(self.editor.toHtml())

            if self.filename.endswith(".rtf"):
                # Save as RTF using QTextDocumentWriter
                writer = QTextDocumentWriter(self.filename)
                success = writer.write(document)
            elif self.filename.endswith(".docx"):
                # Save as DOCX using python-docx
                document = Document()
                for line in self.editor.toPlainText().split('\n'):
                    document.add_paragraph(line)
                document.save(self.filename)  # Use self.filename instead of filename
                success = True
            elif self.filename.endswith(".pdf"):
                # Save as PDF using QPrinter and QPainter
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(self.filename)
                painter = QPainter(printer)
                document.drawContents(painter)
                painter.end()
                success = True
            elif self.filename.endswith(".txt"):
                # Save as TXT
                with open(self.filename, "w", encoding="utf-8") as txt_file:
                    txt_file.write(self.editor.toPlainText())
                success = True
            else:
                QMessageBox.critical(self, 'Error', 'Unsupported file format.')
                return

            if success:
                QMessageBox.information(self, 'Success', f'File saved successfully: {self.filename}')
            else:
                QMessageBox.critical(self, 'Error', f'Error saving file: {self.filename}')

        except Exception as e:
            print(str(e))
            QMessageBox.critical(self, 'Error', f'Error saving file: {str(e)}')

        self.setWindowTitle("ಕನ್ನಡ ನುಡಿ - " + self.access_filename())

    # def save_as(self):
    #     try:
    #         # Prompt the user to choose a file location for saving
    #         filename, _ = QFileDialog.getSaveFileName(self, 'Save File As', '',
    #                                                   filter="All Files (*);;RTF Files (*.rtf);;DOCX Files (*.docx);;PDF Files (*.pdf);;Text Files (*.txt)")
    #
    #         if not filename:  # User cancelled the dialog
    #             return
    #
    #         # Determine the file extension and set the appropriate filter
    #         file_info = QFileInfo(filename)
    #         file_suffix = file_info.suffix().lower()
    #         if file_suffix not in ['rtf', 'docx', 'pdf', 'txt']:
    #             QMessageBox.critical(self, 'Error', 'Unsupported file format.')
    #             return
    #
    #         # Create a QTextDocument and set the HTML content from QTextEdit
    #         document = QTextDocument()
    #         document.setHtml(self.editor.toHtml())
    #
    #         if filename.endswith(".rtf"):
    #             # Save as RTF using QTextDocumentWriter
    #             writer = QTextDocumentWriter(filename)
    #             success = writer.write(document)
    #         if filename.endswith(".docx"):
    #             # Save as DOCX using QTextDocumentWriter
    #             writer = QTextDocumentWriter(filename)
    #             writer.setFormat(QByteArray(b"docx"))  # Convert the string to bytes and then to QByteArray
    #             success = writer.write(document)
    #         elif filename.endswith(".pdf"):
    #             # Save as PDF using QPrinter and QPainter
    #             printer = QPrinter(QPrinter.HighResolution)
    #             printer.setOutputFormat(QPrinter.PdfFormat)
    #             printer.setOutputFileName(filename)
    #             painter = QPainter(printer)
    #             document.drawContents(painter)
    #             painter.end()
    #             success = True
    #         elif filename.endswith(".txt"):
    #             # Save as TXT with UTF-8 encoding
    #             with open(filename, "w", encoding="utf-8") as txt_file:
    #                 txt_file.write(self.editor.toPlainText())
    #             success = True
    #         else:
    #             QMessageBox.critical(self, 'Error', 'Unsupported file format.')
    #             return
    #
    #         if success:
    #             QMessageBox.information(self, 'Success', f'File saved successfully: {filename}')
    #         else:
    #             QMessageBox.critical(self, 'Error', f'Error saving file: {filename}')
    #
    #     except Exception as e:
    #         print(str(e))
    #         QMessageBox.critical(self, 'Error', f'Error saving file: {str(e)}')
    #

    def save_as(self):
        try:
            # Prompt the user to choose a file location for saving
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File As', '',
                                                      filter="All Files (*);;RTF Files (*.rtf);;DOCX Files (*.docx);;PDF Files (*.pdf);;Text Files (*.txt)")

            if not filename:  # User cancelled the dialog
                return

            # Determine the file extension and set the appropriate filter
            file_info = QFileInfo(filename)
            file_suffix = file_info.suffix().lower()
            if file_suffix not in ['rtf', 'docx', 'pdf', 'txt']:
                QMessageBox.critical(self, 'Error', 'Unsupported file format.')
                return

            if filename.endswith(".rtf"):
                # Save as RTF using QTextDocumentWriter
                document = QTextDocument()
                document.setHtml(self.editor.toHtml())
                writer = QTextDocumentWriter(filename)
                success = writer.write(document)
            elif filename.endswith(".docx"):
                # Save as DOCX using python-docx
                document = Document()
                for line in self.editor.toPlainText().split('\n'):
                    document.add_paragraph(line)
                document.save(filename)
                success = True
            elif filename.endswith(".pdf"):
                # Save as PDF using QPrinter and QPainter
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(filename)
                painter = QPainter(printer)
                document = QTextDocument()
                document.setHtml(self.editor.toHtml())
                document.drawContents(painter)
                painter.end()
                success = True
            elif filename.endswith(".txt"):
                # Save as TXT with UTF-8 encoding
                with open(filename, "w", encoding="utf-8") as txt_file:
                    txt_file.write(self.editor.toPlainText())
                success = True
            else:
                QMessageBox.critical(self, 'Error', 'Unsupported file format.')
                return

            if success:
                QMessageBox.information(self, 'Success', f'File saved successfully: {filename}')
            else:
                QMessageBox.critical(self, 'Error', f'Error saving file: {filename}')

        except Exception as e:
            print(str(e))
            QMessageBox.critical(self, 'Error', f'Error saving file: {str(e)}')

    def preview(self):

        # Open preview dialog
        preview = QtPrintSupport.QPrintPreviewDialog()

        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.editor.print_(p))

        preview.exec_()

    def printHandler(self):

        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.editor.document().print_(dialog.printer())

    def cursorPosition(self):

        cursor = self.editor.textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line, col))

    def wordCount(self):

        wc = wordcount.WordCount(self)

        wc.getText()

        wc.show()

    def insertImage(self):

        # Get image file name
        # PYQT5 Returns a tuple in PyQt5
        filename = \
            QtWidgets.QFileDialog.getOpenFileName(self, 'Insert image', ".", "Images (*.png *.xpm *.jpg *.bmp *.gif)")[
                0]

        if filename:

            # Create image object
            image = QtGui.QImage(filename)

            # Error if unloadable
            if image.isNull():

                popup = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                              "Image load error",
                                              "Could not load image file!",
                                              QtWidgets.QMessageBox.Ok,
                                              self)
                popup.show()

            else:

                cursor = self.editor.textCursor()

                cursor.insertImage(image, filename)

    def fontColorChanged(self):

        # Get a color from the text dialog
        color = QtWidgets.QColorDialog.getColor()

        # Set it as the new text color
        self.editor.setTextColor(color)

    def highlight(self):

        color = QtWidgets.QColorDialog.getColor()

        self.editor.setTextBackgroundColor(color)

    def bold(self):

        if self.editor.fontWeight() == QtGui.QFont.Bold:

            self.editor.setFontWeight(QtGui.QFont.Normal)

        else:

            self.editor.setFontWeight(QtGui.QFont.Bold)

    def italic(self):

        state = self.editor.fontItalic()

        self.editor.setFontItalic(not state)

    def underline(self):

        state = self.editor.fontUnderline()

        self.editor.setFontUnderline(not state)

    def strike(self):

        # Grab the text's format
        fmt = self.editor.currentCharFormat()

        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())

        # And set the next char format
        self.editor.setCurrentCharFormat(fmt)

    def superScript(self):

        # Grab the current format
        fmt = self.editor.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)

        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.editor.setCurrentCharFormat(fmt)

    def subScript(self):

        # Grab the current format
        fmt = self.editor.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)

        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.editor.setCurrentCharFormat(fmt)

    def alignLeft(self):
        self.editor.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.editor.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.editor.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.editor.setAlignment(Qt.AlignJustify)

    def indent(self):

        # Grab the cursor
        cursor = self.editor.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's end
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines (diff absolute value)
            for n in range(abs(diff) + 1):
                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)

                # Insert tabbing
                cursor.insertText("\t")

                # And move back up
                cursor.movePosition(direction)

        # If there is no selection, just insert a tab
        else:

            cursor.insertText("\t")

    def handleDedent(self, cursor):

        cursor.movePosition(QtGui.QTextCursor.StartOfLine)

        # Grab the current line
        line = cursor.block().text()

        # If the line starts with a tab character, delete it
        if line.startswith("\t"):

            # Delete next character
            cursor.deleteChar()

        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:

                if char != " ":
                    break

                cursor.deleteChar()

    def dedent(self):

        cursor = self.editor.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QtGui.QTextCursor.Up if diff > 0 else QtGui.QTextCursor.Down

            # Iterate over lines
            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)

                # Move up
                cursor.movePosition(direction)

        else:
            self.handleDedent(cursor)

    def bulletList(self):

        cursor = self.editor.textCursor()

        # Insert bulleted list
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.editor.textCursor()

        # Insert list with numbers
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)

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
            #print("word left of cursor: ", wrong_word)
            html_content = self.editor.toHtml()
            new_html_content = html_content.replace(word_left_of_cursor.lstrip(), wrong_word.strip(), 1)
            # Set the new HTML content
            self.editor.setHtml(new_html_content)
            # Move the cursor to the right of the replaced word
            cursor.movePosition(QTextCursor.Right)
            self.editor.setTextCursor(cursor)

    def addToDictionary(self, word):
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

    def ignore_word(self, word):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()  # Begin editing block to improve performance

        format = QTextCharFormat()
        format.setForeground(self.editor.palette().color(self.editor.foregroundRole()))

        # Clear underline
        format.setUnderlineStyle(QTextCharFormat.NoUnderline)

        cursor.mergeCharFormat(format)
        cursor.endEditBlock()

    def replace_word(self, word_to_replace):
        new_word, ok = QInputDialog.getText(self, 'Replace Word', f'Enter new word to replace {word_to_replace}',
                                            QLineEdit.Normal)
        if ok and new_word:
            cursor = self.editor.textCursor()  # Get the current cursor position
            current_text = self.editor.toPlainText()
            new_text = current_text.replace(word_to_replace, new_word)
            self.editor.setPlainText(new_text)
            # Restore the cursor position
            cursor.setPosition(cursor.position() + len(new_word))
            self.editor.setTextCursor(cursor)

    def refresh_recheck(self):
        reload_bloom_filter()
        cursor_position = self.editor.textCursor()
        text_content = self.editor.toHtml()
        plain_text = self.editor.toPlainText()
        content_for_bloom = [get_clean_words_for_dictionary(word) for word in plain_text.split() if word if
                             len(word) > 1]
        wrong_words = start_bloom(content_for_bloom)
        # Highlight incorrect words in the editor
        highlighted_content = text_content
        for word in wrong_words:
            highlighted_content = highlighted_content.replace(word,
                                                              f'<span style="text-decoration: underline;">{word}</span>')
        # Update the editor with the highlighted content
        self.editor.setHtml(highlighted_content)
        # Restore the cursor position
        self.editor.setTextCursor(cursor_position)

    def access_filename(self):
        return self.filename if self.filename is not None else "Untitled"

    def choose_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.editAndInsertImage(file_path)

    def editAndInsertImage(self, image_path):
        image_dialog = ImageEditDialog(image_path, self)
        if image_dialog.exec_():
            modified_image = image_dialog.getModifiedImage()
            if not modified_image.isNull():
                cursor = self.editor.textCursor()
                cursor.insertImage(modified_image)
