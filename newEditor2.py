from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase, QImage, QTextListFormat
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QComboBox, QHBoxLayout, QMainWindow, QScrollArea,
                             QFileDialog, QFontComboBox, QSlider, QSizePolicy, QMessageBox)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QAction

from editor.common_Dialogs import CommonDialogs
from editor.components.ascii_unicode_ConversionDialog import ConversionDialog
from editor.components.customize_image import ImageEditDialog
from editor.components.excel_csv_file_handling import ExcelCsvViewer
from editor.components.new_editor_components import NewPageLayoutDialog, NewPage
from editor.components.speech_to_text import LanguageSelectionPopup, SpeechToTextThread
from utils import find
from utils.find import Find
from utils.sort_by import SortDialog
from utils.table import Table


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pages = []
        self.current_page = None
        self.filename = None
        self.speech_thread = None
        self.editor_windows = []  # Add this line to keep references to new editor windows
        self.error_dialog = CommonDialogs()
        self.initUI()

    def initUI(self):
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
        #self.sort_by_action.setShortcut("Ctrl+Shift+L")
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

        self.addToolBarBreak()  # Add this line to create a break between toolbars
        self.createFormatbar()  # Add this line to create the format bar below the main toolbar

    def createFormatbar(self):
        self.formatbar = self.addToolBar('Format Toolbar')
        self.formatbar.addAction(self.boldAction)
        self.formatbar.addAction(self.italicAction)
        self.formatbar.addAction(self.underlineAction)
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

    def addNewPage(self):
        page = NewPage(self)
        page.textOverflow.connect(self.addNewPage)
        page.clicked.connect(self.setActivePage)
        self.pages.append(page)
        self.scroll_layout.addWidget(page)
        self.setActivePage(page)

    def setActivePage(self, page):
        self.current_page = page

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
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)",
                                                       options=options)
        if self.filename:
            with open(self.filename, 'r', encoding="utf-8") as file:
                content = file.read()
                if len(content) > 8000:
                    chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
                    for chunk in chunks:
                        self.addPageWithContent(chunk)
                else:
                    self.addPageWithContent(content)

        # Remove blank pages
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

    def zoomIn(self):
        if self.current_page:
            self.current_page.editor.zoomIn()

    def zoomOut(self):
        if self.current_page:
            self.current_page.editor.zoomOut()

    def access_filename(self):
        return self.filename if self.filename is not None else "Untitled"

    def new(self):
        new_editor = TextEditor()
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


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
