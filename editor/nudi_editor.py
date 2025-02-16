import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence, QTextCursor
from PyQt5.QtWidgets import (QMainWindow, QScrollArea,
                             QSizePolicy, QMessageBox, QShortcut)
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from editor.actions.editor_actions import EditorActions
from editor.actions.toolbar_actions_handler import ToolbarHandler
from editor.common_Dialogs import CommonDialogs
from editor.components.ascii_unicode_ConversionDialog import ConversionDialog
from editor.components.excel_csv_file_handling import ExcelCsvViewer
from editor.components.new_editor_components import NewPage
from editor.fileHandling.file_operations import FileOperation
from editor.widgets.zoom_slider import ZoomSlider
from logger import setup_logger
from utils.wordcount import WordCount

filename = os.path.splitext(os.path.basename(__file__))[0]

# Set up logger
logger = setup_logger(filename)


class NewTextEditor(QMainWindow):
    def __init__(self,nudi_logo_icon):
        super().__init__()
        self.nudi_logo_icon = nudi_logo_icon
        self.statusbar = None
        self.scroll_layout = None
        self.scroll_content = None
        self.scroll_area = None
        self.actions = EditorActions(self)
        self.current_file_path = None
        self.total_pages = 0
        self.pages = []
        self.current_page = None
        self.filename = None
        self.speech_thread = None
        self.editor_windows = []  # Keep references to new editor windows
        self.error_dialog = CommonDialogs()
        self.current_zoom_factor = 1.0  # Default zoom factor
        self.toolbar_handler = ToolbarHandler(self)
        self.initUI()
        self.file_ops = FileOperation(self)


        # Initialize and add ZoomSlider
        self.zoom_slider = ZoomSlider()
        self.zoom_slider.initZoomSlider(self)

        shortcut = QShortcut(QKeySequence("Ctrl+A"), self)
        shortcut.activated.connect(self.selectAllPagesContent)

    # Initialize WordCount
    def initUI(self):
        self.actions.createActions()
        self.actions.createMenus()
        self.actions.createToolbars()
        self.actions.createFormatbar()

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

        # Add the first page on initialization
        self.addNewPage()
        self.current_page.editor.installEventFilter(self)
        self.setGeometry(100, 100, 1030, 800)
        self.setWindowTitle("ಕನ್ನಡ ನುಡಿ - " + self.access_filename())
        self.setWindowIcon(QIcon(self.nudi_logo_icon))  # Set the application icon
        self.showMaximized()
        self.setFocusToEditor()
        #self.statusbar.setStatusTip("total pages: " + str(self.total_pages))


    def setFocusToEditor(self):
        # Ensure focus is set to the editor of the current page
        if self.current_page and hasattr(self.current_page, 'editor'):
            self.current_page.editor.setFocus()

    def updateZoom(self, value):
        # Update the zoom factor
        self.current_zoom_factor = value / 100.0
        # Apply zoom to all existing pages
        for page in self.pages:
            page.setZoomFactor(self.current_zoom_factor)

    def addNewPage(self):
        # Check if the last page is blank and avoid adding another blank page

        # Save current cursor position
        current_cursor = self.getCursorPosition()
        if self.pages and self.pages[-1].editor.toPlainText().strip() == "":
            return self.pages[-1]  # Return the existing blank page if it exists

        page = NewPage(self, len(self.pages) + 1)  # Set page number correctly
        page.textOverflow.connect(self.handleTextOverflow)  # Connect the textOverflow signal
        page.clicked.connect(self.setActivePage)

        # Set the zoom factor for the new page
        page.setZoomFactor(self.current_zoom_factor)
        page.setPageMargins(96, 96, 96, 96)  # Apply default 1-inch margins

        self.pages.append(page)
        self.scroll_layout.addWidget(page)
        self.setActivePage(page)
        self.total_pages += 1

        # Update all page numbers
        self.updatePageNumbers()

        # Return the page so we can further customize it if needed
        # Restore the cursor position
        self.setCursorPosition(current_cursor)
        return page

    def getCursorPosition(self):
        """Gets the global cursor position across all pages."""
        cursor_data = []
        for page in self.pages:
            cursor = page.editor.textCursor()
            cursor_data.append((page, cursor.position()))
        return cursor_data

    def setCursorPosition(self, cursor_data):
        """Restores the cursor position on the correct page."""
        for page, position in cursor_data:
            cursor = page.editor.textCursor()
            cursor.setPosition(position)
            page.editor.setTextCursor(cursor)

    def updatePageNumbers(self):
        for index, page in enumerate(self.pages, start=1):
            page.setPageNumber(index)  # Ensure each page number is updated correctly

    def setActivePage(self, page):
        self.current_page = page

    def handleTextOverflow(self):
        if self.current_page:
            # Step 1: Create the new page and get a reference to it
            new_page = self.addNewPage()

            # Step 2: Move the overflowed content to the new page
            remaining_text = self.current_page.editor.toPlainText()

            # Clear the current page's editor
            self.current_page.editor.clear()

            # Set the text in the new page's editor
            new_page.editor.insertPlainText(remaining_text)

            # Step 3: Move the cursor to the new page and set focus there
            new_page.editor.setFocus()  # Focus the editor of the new page
            cursor = new_page.editor.textCursor()
            cursor.movePosition(QtGui.QTextCursor.Start)  # Move cursor to the start of the new page
            new_page.editor.setTextCursor(cursor)

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
        self.file_ops.handle_open_file()

    def saveFile(self):
        content = "\n\n".join([page.editor.toPlainText() for page in self.pages])  # Get text from all pages
        self.file_ops.handle_save_file(content=content)

    def saveAsFile(self):
        content = "\n\n".join([page.editor.toPlainText() for page in self.pages])  # Get text from all pages
        #self.file_ops.handle_save_file(content=content)
        self.file_ops.handle_save_as_file(content=content)

    def openAsciiFile(self):
        self.file_ops.handle_open_ascii_file()
    def removeBlankPages(self):
        for i in reversed(range(len(self.pages))):
            page = self.pages[i]
            text = page.editor.toPlainText().strip()
            if not text:
                self.scroll_layout.removeWidget(page)
                page.deleteLater()
                self.pages.pop(i)
                self.total_pages -= 1

    def addPageWithContent(self, content):
        if not content:
            return self.addNewPage()

        self.addNewPage()

        # Ensure content is displayed correctly
        self.current_page.editor.setPlainText(content)  # Use setPlainText to retain formatting

        self.handleTextOverflow()

    def selectAllPagesContent(self):
        """Selects and highlights all text across all pages."""
        for page in self.pages:
            cursor = page.editor.textCursor()
            cursor.select(QTextCursor.Document)  # Select the entire content of the page
            page.editor.setTextCursor(cursor)  # Apply the selection

    def setFontFamily(self, font):
        if self.current_page and hasattr(self.current_page, 'editor') and self.current_page.editor:
            self.current_page.editor.setCurrentFont(font)
        else:
            print("Error: current_page or its editor is not valid.")

    def setFontSize(self, index):
        self.toolbar_handler.handle_font_size()


    def toggleBold(self):
        self.toolbar_handler.handle_toggle_bold()

    def toggleItalic(self):
        self.toolbar_handler.handle_toggle_italic()
    def toggleUnderline(self):
        self.toolbar_handler.handle_toggle_underline()

    def strike(self):
        self.toolbar_handler.handle_toggle_strikethrough()

    def fontColorChanged(self):
        self.toolbar_handler.handle_font_color()

    def superScript(self):
        self.toolbar_handler.handle_super_script()

    def subScript(self):
        self.toolbar_handler.handle_sub_script()

    def alignLeft(self):
        self.current_page.editor.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.current_page.editor.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.current_page.editor.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.current_page.editor.setAlignment(Qt.AlignJustify)

    def indent(self):
        self.toolbar_handler.handle_indent()


    def dedent(self):
        self.toolbar_handler.handle_dedent()

    def bulletList(self):
        self.toolbar_handler.handle_bullet_list()

    def numberList(self):
        self.toolbar_handler.handle_number_list()

    def highlight(self):
        self.toolbar_handler.handle_highlight()

    def setSpacing(self):
        self.toolbar_handler.handle_set_spacing()

    def setLineSpacing(self, value):
        self.toolbar_handler.handle_set_line_spacing(value)
    # ----------------------------------------------------------------FORMAT functions ----------------------------------------------------------------

    def refresh_recheck(self):
        self.toolbar_handler.handle_refresh_recheck()

    def zoomIn(self):
        if self.current_page:
            self.current_page.editor.zoomIn()

    def zoomOut(self):
        if self.current_page:
            self.current_page.editor.zoomOut()

    def access_filename(self):
        return self.filename if self.filename is not None else "Untitled"

    def printHandler(self):
        self.toolbar_handler.handle_print()

    def new(self):
        new_editor = NewTextEditor(self.nudi_logo_icon)
        new_editor.show()
        self.editor_windows.append(new_editor)  # Keep a reference to the new editor window

    def page_layout_size(self):
        self.toolbar_handler.handle_page_layout_size()

    def page_margin_size(self):
        self.toolbar_handler.handle_page_margin_size()

    def undo(self):
        if self.current_page:
            self.current_page.editor.undo()

    def redo(self):
        if self.current_page:
            self.current_page.editor.redo()

    def insertTable(self):
        self.toolbar_handler.handle_insert_table()
    def find_replace(self):
        self.toolbar_handler.handle_find_replace()

    def choose_image(self):
        self.toolbar_handler.handle_choose_image()
    def insertEditedImage(self, edited_image):
        self.toolbar_handler.handle_insert_edited_image(edited_image)
    def sortByAction(self):
        self.toolbar_handler.handle_sort_by_action()
    def toggle_speech_to_text(self):
        self.toolbar_handler.handle_toggle_speech_to_text()

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
