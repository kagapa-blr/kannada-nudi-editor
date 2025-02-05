import os
import sys
import time
from PyQt5 import QtPrintSupport, QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QTextListFormat, QTextCharFormat, QTextCursor, QTextBlockFormat
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QScrollArea,
                             QFileDialog, QSizePolicy, QMessageBox, QColorDialog)
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from editor.actions.editor_actions import EditorActions
from editor.actions.toolbar_actions_handler import ToolbarHandler
from editor.fileHandling.file_operations import FileOperation
from editor.common_Dialogs import CommonDialogs
from editor.components.ascii_unicode_ConversionDialog import ConversionDialog
from editor.components.customize_image import ImageEditDialog
from editor.components.excel_csv_file_handling import ExcelCsvViewer
from editor.components.format_content import SpacingDialog
from editor.components.new_editor_components import NewPageLayoutDialog, NewPage
from editor.components.speech_to_text import LanguageSelectionPopup, SpeechToTextThread
from editor.widgets.zoom_slider import ZoomSlider
from logger import setup_logger
from spellcheck.bloom_filter import start_bloom
from utils.corpus_clean import get_clean_words_for_dictionary
from utils.find import Find
from utils.sort_by import SortDialog
from utils.table import Table
from utils.wordcount import WordCount

filename = os.path.splitext(os.path.basename(__file__))[0]

# Set up logger
logger = setup_logger(filename)


import subprocess
import os

def start_background_exe():
    if sys.platform.startswith("linux"):
        print("Linux system detected. The executable will not be started.")
        return

    exe_path = os.path.join("resources", "keyboardDriver", "kannadaKeyboard.exe")  # OS-independent path handling

    try:
        print("Kannada Nudi Keyboard loaded and running in background")
        subprocess.Popen([exe_path], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         start_new_session=True)
    except Exception as e:
        print(f"Error starting background exe: {e}")



class NewTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
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

    def initUI(self):
        start_background_exe()
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
        self.setWindowIcon(QIcon('resources/images/logo.jpg'))  # Set the application icon
        self.showMaximized()
        self.setFocusToEditor()
        self.statusbar.setStatusTip("total pages: " + str(self.total_pages))


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
        if self.pages and self.pages[-1].editor.toPlainText().strip() == "":
            return self.pages[-1]  # Return the existing blank page if it exists

        page = NewPage(self)
        page.textOverflow.connect(self.handleTextOverflow)  # Connect the textOverflow signal
        page.clicked.connect(self.setActivePage)

        # Set the zoom factor for the new page
        page.setZoomFactor(self.current_zoom_factor)

        self.pages.append(page)
        self.scroll_layout.addWidget(page)
        self.setActivePage(page)
        self.total_pages += 1

        # Return the page so we can further customize it if needed
        return page

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
        self.file_ops.handle_save_file(content=content)
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
        self.current_page.editor.setHtml(content)
        self.handleTextOverflow()

    def setFontFamily(self, font):
        if self.current_page:
            self.current_page.editor.setCurrentFont(font)

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
                    self.insertEditedImage(modified_image)

    def insertEditedImage(self, edited_image):
        if self.current_page:
            cursor = self.current_page.editor.textCursor()
            cursor.insertImage(edited_image)

    def bulletList(self):

        cursor = self.current_page.editor.textCursor()

        # Insert bulleted list
        cursor.insertList(QTextListFormat.ListDisc)

    def numberList(self):
        if not self.current_page or not self.current_page.editor:
            print("Error: current_page or editor is not valid.")
            return
        cursor = self.current_page.editor.textCursor()

        # Insert list with numbers
        cursor.insertList(QTextListFormat.ListDecimal)

    def sortByAction(self):
        if not self.current_page or not self.current_page.editor:
            print("Error: current_page or editor is not valid.")
            return

        # Create and execute the SortDialog
        sort_dialog = SortDialog(self)
        if sort_dialog.exec_():
            sort_by = sort_dialog.combo_sort_by.currentText()
            type_ = sort_dialog.combo_type.currentText()
            using = sort_dialog.combo_using.currentText()
            ascending = sort_dialog.radio_asc.isChecked()
            has_header = sort_dialog.check_has_header.isChecked()
            separator = sort_dialog.line_separator.text()
            sort_options = sort_dialog.combo_sort_options.currentText()

            # Retrieve text from QTextEdit
            text = self.current_page.editor.toPlainText()
            lines = text.split('\n')

            # Implement sorting based on user input
            if sort_by == "Paragraph":
                # Implement sorting logic for Paragraph sorting
                pass
            elif sort_by == "Headings":
                # Implement sorting logic for Headings sorting
                pass
            elif sort_by == "Fields":
                # Implement sorting logic for Fields sorting
                pass
            elif sort_by == "Header Name":
                # Implement sorting logic for Header Name sorting
                pass
            elif sort_by == "Column Number":
                # Implement sorting logic for Column Number sorting
                pass
            else:
                print("Unknown sort_by option:", sort_by)
                return

            # Example sorting for different types
            if type_ == "Text":
                lines.sort(key=str.lower if not sort_options == "Case sensitive" else str, reverse=not ascending)
            elif type_ == "Number":
                lines.sort(key=lambda x: float(x) if x.replace('.', '', 1).isdigit() else float('inf'),
                           reverse=not ascending)
            elif type_ == "Date":
                from datetime import datetime
                lines.sort(key=lambda x: datetime.strptime(x, '%Y-%m-%d'), reverse=not ascending)

            sorted_text = '\n'.join(lines)

            # Update QTextEdit with sorted text
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
