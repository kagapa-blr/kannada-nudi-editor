import os

import pypandoc
from PyQt5 import QtPrintSupport
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase, QTextListFormat, QTextCharFormat, QTextCursor, QTextDocument
from PyQt5.QtGui import QIcon
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QComboBox, QHBoxLayout, QMainWindow, QScrollArea,
                             QFileDialog, QFontComboBox, QSlider, QSizePolicy, QMessageBox, QColorDialog)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QAction
from docx import Document

from editor.common_Dialogs import CommonDialogs
from editor.components.ascii_unicode_ConversionDialog import ConversionDialog
from editor.components.customize_image import ImageEditDialog
from editor.components.excel_csv_file_handling import ExcelCsvViewer
from editor.components.format_content import SpacingDialog
from editor.components.new_editor_components import NewPageLayoutDialog, NewPage
from editor.components.speech_to_text import LanguageSelectionPopup, SpeechToTextThread
from logger import setup_logger
from spellcheck.bloom_filter import reload_bloom_filter, start_bloom
from utils.asciitounicode import process_line
from utils.corpus_clean import get_clean_words_for_dictionary
from utils.find import Find
from utils.sort_by import SortDialog
from utils.table import Table
from utils.wordcount import WordCount
import subprocess
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


class NewTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.total_pages = 0
        self.pages = []
        self.current_page = None
        self.filename = None
        self.speech_thread = None
        self.editor_windows = []  # Add this line to keep references to new editor windows
        self.error_dialog = CommonDialogs()
        self.initUI()

    def initUI(self):
        #start_background_exe()
        self.createActions()
        self.createMenus()
        self.createToolbars()
        #self.createFormatbar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove outer margins
        layout.setSpacing(0)  # Remove spacing between elements

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)  # Adjust margins as needed
        self.scroll_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.scroll_area.setWidget(self.scroll_content)

        layout.addWidget(self.scroll_area)

        self.statusbar = self.statusBar()
        self.initZoomSlider()  # Add the zoom slider
        self.addNewPage()

        self.setGeometry(100, 100, 1030, 800)
        self.setWindowTitle("ಕನ್ನಡ ನುಡಿ - " + self.access_filename())
        self.setWindowIcon(QIcon('resources/images/logo.jpg'))  # Set the application icon
        self.showMaximized()
        self.setFocusToEditor()

    def setFocusToEditor(self):
        # Ensure focus is set to the editor of the current page
        if self.current_page and hasattr(self.current_page, 'editor'):
            self.current_page.editor.setFocus()

    def initZoomSlider(self):
        zoom_label = QLabel("Zoom:", self)
        self.zoom_slider = QSlider(Qt.Horizontal, self)
        self.zoom_slider.setRange(10, 300)  # Zoom range from 10% to 300%
        self.zoom_slider.setValue(100)  # Default zoom level at 100%
        self.zoom_slider.setTickInterval(10)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setFixedWidth(150)  # Set a fixed width for the slider
        self.zoom_slider.valueChanged.connect(self.updateZoom)

        slider_layout = QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        slider_layout.setSpacing(0)  # Remove spacing
        slider_layout.addStretch(1)  # Add stretchable space to push slider to the right
        slider_layout.addWidget(zoom_label)
        slider_layout.addWidget(self.zoom_slider)

        central_layout = self.centralWidget().layout()
        central_layout.addLayout(slider_layout)
        central_layout.setAlignment(slider_layout, Qt.AlignBottom | Qt.AlignRight)

    def updateZoom(self, value):
        if self.current_page:
            factor = value / 100
            self.current_page.setZoomFactor(factor)

    def addNewPage(self):
        page = NewPage(self)
        page.textOverflow.connect(self.handleTextOverflow)  # Connect the textOverflow signal
        page.clicked.connect(self.setActivePage)
        self.pages.append(page)
        self.scroll_layout.addWidget(page)
        self.setActivePage(page)
        self.total_pages += 1
        self.statusbar.setStatusTip("total pages: " + str(self.total_pages))

    def setActivePage(self, page):
        self.current_page = page

    def handleTextOverflow(self):
        if self.current_page:
            self.addNewPage()
            # Move overflowed content to the new page
            remaining_text = self.current_page.editor.toPlainText()
            self.current_page.editor.clear()
            self.current_page.editor.insertPlainText(remaining_text)

    def createActions(self):
        self.newAction = QAction(QIcon('resources/images/new-file.png'), 'New', self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setStatusTip('Create a new file')
        self.newAction.triggered.connect(self.new)

        self.openAction = QAction(QIcon('resources/images/open-file.png'), 'Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open an existing file')
        self.openAction.triggered.connect(self.openFile)

        self.openAsciiAction = QAction(QIcon('resources/images/ascii-file-icon.png'), 'Open ASCII file', self)
        self.openAsciiAction.setStatusTip('Open ASCII file')
        self.openAsciiAction.triggered.connect(self.openAsciiFile)

        self.saveAction = QAction(QIcon('resources/images/stock_save.png'), 'Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save the current file')
        self.saveAction.triggered.connect(self.saveFile)

        self.undoAction = QAction(QIcon('resources/images/undo.png'), 'Undo', self)
        self.undoAction.setShortcut('Ctrl+Z')
        self.undoAction.setStatusTip('Undo the last action')
        self.undoAction.triggered.connect(self.undo)

        self.redoAction = QAction(QIcon('resources/images/redo.png'), 'Redo', self)
        self.redoAction.setShortcut('Ctrl+Y')
        self.redoAction.setStatusTip('Redo the last undone action')
        self.redoAction.triggered.connect(self.redo)

        self.printAction = QAction(QIcon('resources/images/print.png'), 'Print', self)
        self.printAction.setShortcut('Ctrl+P')
        self.printAction.setStatusTip('Print the current file')
        self.printAction.triggered.connect(self.printHandler)

        self.zoomInAction = QAction(QIcon('resources/images/zoom-in.png'), 'Zoom In', self)
        self.zoomInAction.setShortcut('Ctrl++')
        self.zoomInAction.setStatusTip('Zoom in')
        self.zoomInAction.triggered.connect(self.zoomIn)

        self.zoomOutAction = QAction(QIcon('resources/images/zoom-out.png'), 'Zoom Out', self)
        self.zoomOutAction.setShortcut('Ctrl+-')
        self.zoomOutAction.setStatusTip('Zoom out')
        self.zoomOutAction.triggered.connect(self.zoomOut)

        self.pageLayoutAction = QAction(QIcon('resources/images/page-layout.png'), 'Page Layout', self)
        self.pageLayoutAction.setStatusTip('Set page layout and size')
        self.pageLayoutAction.triggered.connect(self.page_layout_size)

        self.insertTableAction = QAction(QIcon('resources/images/insert-table.png'), 'Insert Table', self)
        self.insertTableAction.setStatusTip('Insert a table into the document')
        self.insertTableAction.triggered.connect(self.insertTable)

        self.findAction = QAction(QIcon("resources/images/find.png"), "Find and replace", self)
        self.findAction.setStatusTip("Find and replace words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(self.find_replace)

        self.imageAction = QAction(QIcon("resources/images/add-image.png"), "Insert image", self)
        self.imageAction.setStatusTip("Insert image")
        self.imageAction.setShortcut("Ctrl+Shift+I")
        self.imageAction.triggered.connect(self.choose_image)

        self.bulletAction = QAction(QIcon("resources/images/bullet-list.png"), "Insert bullet List", self)
        self.bulletAction.setStatusTip("Insert bullet list")
        self.bulletAction.setShortcut("Ctrl+Shift+B")
        self.bulletAction.triggered.connect(self.bulletList)

        self.numberedAction = QAction(QIcon("resources/images/number-list.png"), "Insert numbered List",
                                      self)
        self.numberedAction.setStatusTip("Insert numbered list")
        self.numberedAction.setShortcut("Ctrl+Shift+L")
        self.numberedAction.triggered.connect(self.numberList)

        self.sort_by_action = QAction(QIcon("resources/images/sortBy.png"), "Sort By",
                                      self)
        self.sort_by_action.setStatusTip("sort by action")
        # self.sort_by_action.setShortcut("Ctrl+Shift+L")
        self.sort_by_action.triggered.connect(self.sortByAction)

        self.speech_to_text = QAction(QIcon('resources/images/mic-speecch-to-text.png'), 'speech to Text', self)
        self.speech_to_text.setStatusTip("speech to text")
        self.speech_to_text.setCheckable(True)
        self.speech_to_text.triggered.connect(self.toggle_speech_to_text)

        self.ascii_to_unicode = QAction(QIcon('resources/images/convert.png'), 'ASCII to Unicode vs converter', self)
        self.ascii_to_unicode.setStatusTip("ASCII to Unicode vs converter")
        self.ascii_to_unicode.setCheckable(True)
        self.ascii_to_unicode.triggered.connect(self.ascii_to_unicode_converter)

        self.excel_csv = QAction(QIcon('resources/images/excel_csv.png'), 'Excel and CSV file operations', self)
        self.excel_csv.setStatusTip("Excel File Handling")
        self.excel_csv.setCheckable(True)
        self.excel_csv.triggered.connect(self.excel_csv_file)

        # self.wordCountAction = QAction(QIcon("resources/images/count.png"), "See word/symbol count", self)
        # self.wordCountAction.setStatusTip("See word/symbol count")
        # self.wordCountAction.setShortcut("Ctrl+W")
        # self.wordCountAction.triggered.connect(self.wordCount)

        self.refresh_action = QAction(QIcon('resources/images/refresh.png'), 'Refresh and spellcheck', self)
        self.refresh_action.setStatusTip("spellcheck")
        self.refresh_action.triggered.connect(self.refresh_recheck)

        ####------format bar stated ----------------------------------------------------------

        self.fontColor = QAction(QIcon("resources/images/font-color.png"), "Change font color", self)
        self.fontColor.setStatusTip("change font color")
        self.fontColor.triggered.connect(self.fontColorChanged)

        self.boldAction = QAction(QIcon('resources/images/bold.png'), 'Bold', self)
        self.boldAction.setShortcut('Ctrl+B')
        self.boldAction.setStatusTip('Make selected text bold')
        self.boldAction.triggered.connect(self.toggleBold)

        self.italicAction = QAction(QIcon('resources/images/italic.png'), 'Italic', self)
        self.italicAction.setShortcut('Ctrl+I')
        self.italicAction.setStatusTip('Make selected text italic')
        self.italicAction.triggered.connect(self.toggleItalic)

        self.underlineAction = QAction(QIcon('resources/images/underline.png'), 'Underline', self)
        self.underlineAction.setShortcut('Ctrl+U')
        self.underlineAction.setStatusTip('Underline selected text')
        self.underlineAction.triggered.connect(self.toggleUnderline)

        self.strikeAction = QAction(QIcon("resources/images/strike.png"), "Strike-out", self)
        self.underlineAction.setStatusTip('Strike-outt')
        self.strikeAction.triggered.connect(self.strike)

        self.superAction = QAction(QIcon("resources/images/superscript.png"), "Superscript", self)
        self.superAction.triggered.connect(self.superScript)

        self.subAction = QAction(QIcon("resources/images/subscript.png"), "Subscript", self)
        self.subAction.triggered.connect(self.subScript)

        self.alignLeftAction = QAction(QIcon("resources/images/align-left.png"), "Align left", self)
        self.alignLeftAction.triggered.connect(self.alignLeft)

        self.alignCenterAction = QAction(QIcon("resources/images/align-center.png"), "Align center", self)
        self.alignCenterAction.triggered.connect(self.alignCenter)

        self.alignRightAction = QAction(QIcon("resources/images/align-right.png"), "Align right", self)
        self.alignRightAction.triggered.connect(self.alignRight)

        self.alignJustifyAction = QAction(QIcon("resources/images/align-justify.png"), "Align justify", self)
        self.alignJustifyAction.triggered.connect(self.alignJustify)

        self.indentAction = QAction(QIcon("resources/images/indent.png"), "Indent Area", self)
        self.indentAction.setShortcut("Ctrl+Tab")
        self.indentAction.triggered.connect(self.indent)

        self.dedentAction = QAction(QIcon("resources/images/dedent.png"), "Dedent Area", self)
        self.dedentAction.setShortcut("Shift+Tab")
        self.dedentAction.triggered.connect(self.dedent)

        self.fontbackColor = QAction(QIcon("resources/images/highlight.png"), "Change background color", self)
        self.fontbackColor.triggered.connect(self.highlight)

        self.line_para_spacing = QAction(QIcon("resources/images/line-paragraph-spacing.png"),
                                         "line and Paragraph spacing", self)
        self.line_para_spacing.setStatusTip("line and paragraph spacing.")
        self.line_para_spacing.triggered.connect(self.setSpacing)

        ##### ------ format bar ended----------------------------------------------------------------

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
        self.toolbar.addAction(self.openAsciiAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.pageLayoutAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.insertTableAction)
        self.toolbar.addAction(self.findAction)
        self.toolbar.addAction(self.imageAction)
        self.toolbar.addAction(self.bulletAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.numberedAction)
        self.toolbar.addAction(self.sort_by_action)
        self.toolbar.addAction(self.speech_to_text)
        self.toolbar.addAction(self.ascii_to_unicode)
        self.toolbar.addAction(self.excel_csv)
        self.toolbar.addSeparator()
        #self.toolbar.addAction(self.wordCountAction)
        self.toolbar.addAction(self.refresh_action)

        self.addToolBarBreak()  # Add this line to create a break between toolbars
        self.createFormatbar()  # Add this line to create the format bar below the main toolbar

    def createFormatbar(self):
        self.formatbar = self.addToolBar('Format Toolbar')

        self.formatbar.addSeparator()
        self.fontComboBox = QFontComboBox(self)
        self.fontComboBox.currentFontChanged.connect(self.setFontFamily)
        self.formatbar.addWidget(self.fontComboBox)

        # Set the default font to NudiParijatha
        font_id = QFontDatabase.addApplicationFont("resources/static/Nudi_fonts/NudiParijatha.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.fontComboBox.setCurrentFont(QFont(font_family))

        self.fontSizeComboBox = QComboBox(self)
        self.fontSizeComboBox.addItems([str(size) for size in range(8, 49, 2)])
        self.fontSizeComboBox.currentIndexChanged.connect(self.setFontSize)
        self.formatbar.addWidget(self.fontSizeComboBox)

        # Set the default font size to 12
        self.fontSizeComboBox.setCurrentText("12")

        self.formatbar.addAction(self.fontColor)
        self.formatbar.addAction(self.boldAction)
        self.formatbar.addAction(self.italicAction)
        self.formatbar.addAction(self.underlineAction)
        self.formatbar.addAction(self.fontbackColor)
        self.formatbar.addAction(self.strikeAction)
        self.formatbar.addAction(self.superAction)
        self.formatbar.addAction(self.subAction)
        self.formatbar.addAction(self.alignLeftAction)
        self.formatbar.addAction(self.alignCenterAction)
        self.formatbar.addAction(self.alignRightAction)
        self.formatbar.addAction(self.alignJustifyAction)
        self.formatbar.addAction(self.indentAction)
        self.formatbar.addAction(self.dedentAction)
        self.formatbar.addAction(self.line_para_spacing)

    # Override the closeEvent method
    def closeEvent(self, event):
        try:
            if self.speech_thread:
                self.speech_thread.stop()
            event.accept()
        except Exception as e:
            self.error_dialog.show_error_popup(str(e))

        if any(page.is_changed for page in self.pages):
            reply = QMessageBox.question(self, 'ಸಂದೇಶ',
                                         "ನೀವು ಉಳಿಸದ ಬದಲಾವಣೆಗಳನ್ನು ಹೊಂದಿರುವಿರಿ. ನಿಮ್ಮ ಬದಲಾವಣೆಗಳನ್ನು ನೀವು ಉಳಿಸಲು ಬಯಸುವಿರಾ?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                         QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.saveFile()
                event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def newFile(self):
        self.pages.clear()
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.addNewPage()

    def openFile(self):
        options = QFileDialog.Options()
        self.filename, _ = QFileDialog.getOpenFileName(self,
                                                       "Open File",
                                                       "",
                                                       "All Files (*);;Text Files (*.txt);;Word Documents (*.docx);;Rich Text Format (*.rtf)",
                                                       options=options)
        if self.filename:
            content = ""
            file_extension = self.filename.split('.')[-1].lower()

            try:
                if file_extension == 'txt':
                    with open(self.filename, 'r', encoding="utf-8") as file:
                        content = file.read()
                elif file_extension == 'docx':
                    doc = Document(self.filename)
                    content = "\n".join([para.text for para in doc.paragraphs])
                elif file_extension == 'rtf':
                    content = pypandoc.convert_file(self.filename, 'plain', format='rtf')
                else:
                    raise ValueError("Unsupported file format")

                if len(content) > 8000:
                    chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
                    for chunk in chunks:
                        self.addPageWithContent(chunk)
                else:
                    self.addPageWithContent(content)
            except Exception as e:
                self.error_dialog.showError(str(e))

            # Update window title and remove blank pages
            self.setWindowTitle("ಕನ್ನಡ ನುಡಿ - " + self.access_filename())
            self.removeBlankPages()

    def openAsciiFile(self):
        options = QFileDialog.Options()
        self.filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "",
            "All Files (*);;Text Files (*.txt);;Word Documents (*.docx);;Rich Text Format (*.rtf)",
            options=options)
        if self.filename:
            content = ""
            file_extension = self.filename.split('.')[-1].lower()

            try:
                if file_extension == 'txt':
                    with open(self.filename, 'r', encoding="utf-8") as file:
                        unicode_lines = [process_line(line) for line in file]
                        content = ''.join(unicode_lines)
                elif file_extension == 'docx':
                    doc = Document(self.filename)
                    paragraphs = [process_line(para.text) for para in doc.paragraphs]
                    content = "\n".join(paragraphs)
                elif file_extension == 'rtf':
                    plain_text = pypandoc.convert_file(self.filename, 'plain', format='rtf')
                    unicode_lines = [process_line(line) for line in plain_text.splitlines()]
                    content = '\n'.join(unicode_lines)
                else:
                    self.error_dialog("Unsupported file format")
                    #raise ValueError("Unsupported file format")

                if len(content) > 8000:
                    chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
                    for chunk in chunks:
                        self.addPageWithContent(chunk)
                else:
                    self.addPageWithContent(content)
            except Exception as e:
                self.error_dialog.showError(str(e))

            # Update window title and remove blank pages
            self.setWindowTitle("ಕನ್ನಡ ನುಡಿ - " + self.access_filename())
            self.removeBlankPages()

    def removeBlankPages(self):
        for i in reversed(range(len(self.pages))):
            page = self.pages[i]
            text = page.editor.toPlainText().strip()
            if not text:
                self.scroll_layout.removeWidget(page)
                page.deleteLater()
                self.pages.pop(i)

    def addPageWithContent(self, content):
        if not content:
            return
        self.addNewPage()
        self.current_page.editor.insertPlainText(content)
        self.handleTextOverflow()

    def saveFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save File", "",
            "Text Files (*.txt);;Word Files (*.docx);;Rich Text Format (*.rtf);;PDF Files (*.pdf);;All Files (*)",
            options=options
        )
        if fileName:
            content = self.pages[0].editor.toPlainText()
            if fileName.endswith('.txt'):
                with open(fileName, 'w', encoding='utf-8') as file:
                    file.write(content)
            elif fileName.endswith('.docx'):
                doc = Document()
                doc.add_paragraph(content)
                doc.save(fileName)
            elif fileName.endswith('.rtf'):
                pypandoc.convert_text(content, 'rtf', format='md', outputfile=fileName, encoding='utf-8')
            elif fileName.endswith('.pdf'):
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(fileName)
                doc = QTextDocument()
                doc.setPlainText(content)
                doc.print_(printer)
            else:
                self.error_dialog.showError("Unsupported file format")

    def setFontFamily(self, font):
        if self.current_page:
            self.current_page.editor.setCurrentFont(font)

    def setFontSize(self, index):
        size = int(self.fontSizeComboBox.currentText())
        if self.current_page and hasattr(self.current_page, 'editor'):
            try:
                self.current_page.editor.setFontPointSize(size)
            except RuntimeError as e:
                print(f"Error setting font size: {str(e)}")
                # Handle the error as needed (e.g., log it, notify the user)
        else:
            print("Error: No current page or editor not available")
            # Handle the error as needed (e.g., log it, notify the user)

    def toggleBold(self):
        # if self.current_page:
        #     self.current_page.editor.setFontWeight(
        #         QFont.Bold if self.current_page.editor.fontWeight() != QFont.Bold else QFont.Normal)
        if self.current_page.editor.fontWeight() == QFont.Bold:

            self.current_page.editor.setFontWeight(QFont.Normal)

        else:

            self.current_page.editor.setFontWeight(QFont.Bold)

    def toggleItalic(self):
        if self.current_page:
            state = self.current_page.editor.fontItalic()
            self.current_page.editor.setFontItalic(not state)

    def toggleUnderline(self):
        if self.current_page:
            state = self.current_page.editor.fontUnderline()
            self.current_page.editor.setFontUnderline(not state)

    def strike(self):

        # Grab the text's format
        fmt = self.current_page.editor.currentCharFormat()

        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())

        # And set the next char format
        self.current_page.editor.setCurrentCharFormat(fmt)

    def fontColorChanged(self):

        # Get a color from the text dialog
        color = QColorDialog.getColor()

        # Set it as the new text color
        self.current_page.editor.setTextColor(color)

    def superScript(self):

        # Grab the current format
        fmt = self.current_page.editor.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QTextCharFormat.AlignSuperScript)

        else:

            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)

        # Set the new format
        self.current_page.editor.setCurrentCharFormat(fmt)

    def subScript(self):

        # Grab the current format
        fmt = self.current_page.editor.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QTextCharFormat.AlignSubScript)

        else:

            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)

        # Set the new format
        self.current_page.editor.setCurrentCharFormat(fmt)

    def alignLeft(self):
        self.current_page.editor.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.current_page.editor.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.current_page.editor.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.current_page.editor.setAlignment(Qt.AlignJustify)

    def indent(self):

        # Grab the cursor
        cursor = self.current_page.editor.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's end
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QTextCursor.Up if diff > 0 else QTextCursor.Down

            # Iterate over lines (diff absolute value)
            for n in range(abs(diff) + 1):
                # Move to start of each line
                cursor.movePosition(QTextCursor.StartOfLine)

                # Insert tabbing
                cursor.insertText("\t")

                # And move back up
                cursor.movePosition(direction)

        # If there is no selection, just insert a tab
        else:

            cursor.insertText("\t")

    def handleDedent(self, cursor):

        cursor.movePosition(QTextCursor.StartOfLine)

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

        cursor = self.current_page.editor.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QTextCursor.Up if diff > 0 else QTextCursor.Down

            # Iterate over lines
            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)

                # Move up
                cursor.movePosition(direction)

        else:
            self.handleDedent(cursor)

    def bulletList(self):

        cursor = self.current_page.editor.textCursor()

        # Insert bulleted list
        cursor.insertList(QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.current_page.editor.textCursor()

        # Insert list with numbers
        cursor.insertList(QTextListFormat.ListDecimal)

    def highlight(self):

        color = QColorDialog.getColor()

        self.current_page.editor.setTextBackgroundColor(color)

    def setSpacing(self):
        dialog = SpacingDialog(self)
        dialog.setWindowTitle('Line & Paragraph Spacing')
        dialog.lineSpacingLabel.setText('Line Spacing (pixels):')
        dialog.customLineSpacingSpinBox.setValue(self.current_page.editor.currentFont().pixelSize())
        dialog.beforeParagraphSpinBox.setValue(0)
        dialog.afterParagraphSpinBox.setValue(0)
        dialog.exec_()
        dialog.applySettings()

    #----------------------------------------------------------------FORMAT functions ----------------------------------------------------------------

    def refresh_recheck(self):
        self.total_pages = 0
        for page in self.pages:
            self.total_pages += 1
            if not page or not page.editor:
                print("Page or editor is not valid.")
                continue

            # Retrieve plain text from current page's editor
            plain_text = page.editor.toPlainText()

            # Process text content for spell checking
            content_for_bloom = [get_clean_words_for_dictionary(word) for word in plain_text.split() if len(word) > 1]
            wrong_words = start_bloom(content_for_bloom)

            # Underline incorrect words in the editor
            highlighted_content = plain_text
            for word in wrong_words:
                highlighted_content = highlighted_content.replace(word,
                                                                  f'<span style="text-decoration: underline;">{word}</span>')

            # Update the editor with the underlined content
            page.editor.setHtml(highlighted_content)
        self.removeBlankPages()
        self.statusBar().showMessage("total pages " + str(self.total_pages))

    def zoomIn(self):
        if self.current_page:
            self.current_page.editor.zoomIn()

    def zoomOut(self):
        if self.current_page:
            self.current_page.editor.zoomOut()

    def access_filename(self):
        return self.filename if self.filename is not None else "Untitled"

    def printHandler(self):

        # Open printing dialog
        dialog = QtPrintSupport.QPrintDialog()

        if dialog.exec_() == QDialog.Accepted:
            self.current_page.editor.document().print_(dialog.printer())
    def new(self):
        new_editor = NewTextEditor()
        new_editor.show()
        self.editor_windows.append(new_editor)  # Keep a reference to the new editor window

    def page_layout_size(self):
        dialog = NewPageLayoutDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            width, height = dialog.getPageSize()
            for page in self.pages:
                page.setPageSize(width, height)

    def undo(self):
        if self.current_page:
            self.current_page.editor.undo()

    def redo(self):
        if self.current_page:
            self.current_page.editor.redo()

    def insertTable(self):
        if self.current_page:
            table_dialog = Table(self.current_page.editor)  # Pass the QTextEdit widget to Table
            table_dialog.exec_()

    def find_replace(self):
        if self.current_page:
            find = Find(self.current_page.editor)  # Pass the QTextEdit widget to Table
            find.exec_()

    def choose_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            image_dialog = ImageEditDialog(file_path, self)
            if image_dialog.exec_() == QDialog.Accepted:
                modified_image = image_dialog.getModifiedImage()
                if not modified_image.isNull():
                    self.editAndInsertImage(modified_image)

    def editAndInsertImage(self, image_path):
        image_dialog = ImageEditDialog(image_path, self)
        if image_dialog.exec_() == QDialog.Accepted:
            modified_image = image_dialog.getModifiedImage()
            if not modified_image.isNull() and self.current_page:
                cursor = self.current_page.editor.textCursor()
                cursor.insertImage(modified_image)

    def bulletList(self):

        cursor = self.current_page.editor.textCursor()

        # Insert bulleted list
        cursor.insertList(QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.current_page.editor.textCursor()

        # Insert list with numbers
        cursor.insertList(QTextListFormat.ListDecimal)

    def sortByAction(self):
        if not self.current_page or not self.current_page.editor:
            # Handle case where current_page or editor is not valid
            return

        sort_dialog = SortDialog(self)
        if sort_dialog.exec_():
            sort_by = sort_dialog.combo_sort_by.currentText()
            type_ = sort_dialog.combo_type.currentText()
            using = sort_dialog.combo_using.currentText()
            ascending = sort_dialog.radio_asc.isChecked()
            has_header = sort_dialog.check_has_header.isChecked()
            separator = sort_dialog.line_separator.text()
            sort_options = sort_dialog.combo_sort_options.currentText()

            text = self.current_page.editor.toPlainText()
            lines = text.split('\n')

            # Implement sorting based on user input
            if type_ == "Text":
                lines.sort(key=str.lower if not sort_options == "Case sensitive" else str, reverse=not ascending)
            elif type_ == "Number":
                lines.sort(key=lambda x: float(x) if x.replace('.', '', 1).isdigit() else float('inf'),
                           reverse=not ascending)
            elif type_ == "Date":
                from datetime import datetime
                lines.sort(key=lambda x: datetime.strptime(x, '%Y-%m-%d'), reverse=not ascending)

            sorted_text = '\n'.join(lines)
            self.current_page.editor.setPlainText(sorted_text)

    def toggle_speech_to_text(self):
        sender = self.sender()
        if sender.isChecked():
            popup = LanguageSelectionPopup()
            if popup.exec_() == QDialog.Accepted:
                selected_language = popup.selectedLanguage
                if selected_language is None:
                    QMessageBox.critical(None, 'Error', 'No language selected')
                    sender.setChecked(False)
                    return

                sender.setText("Stop Speech to Text")
                self.speech_thread = SpeechToTextThread(self.current_page.editor, selected_language)
                self.speech_thread.start()
            else:
                sender.setChecked(False)
        else:
            sender.setText("Speech to Text")
            if self.speech_thread:
                self.speech_thread.stop()
                self.speech_thread = None

    def ascii_to_unicode_converter(self):
        dialog = ConversionDialog(self)
        dialog.exec_()

    def excel_csv_file(self):
        self.viewer = ExcelCsvViewer()
        self.viewer.show()

    def wordCount(self):
        wc = WordCount(self.current_page)

        wc.getText()

        wc.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    editor = NewTextEditor()
    editor.show()
    sys.exit(app.exec_())
