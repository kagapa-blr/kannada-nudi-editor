import os
import subprocess

import docx
from PyQt5.QtCore import Qt, QEvent, QFile, QTextStream
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QIcon, QFontDatabase, QTextListFormat, QTextBlockFormat, \
    QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QMenu, QToolBar, QMessageBox, \
    QInputDialog, QLineEdit, QColorDialog, QTextEdit, QTableWidget, QTableWidgetItem

from config import file_path as fp
from editor.components.customize_image import ImageEditDialog
from logger import setup_logger
from spellcheck.bloom_filter import bloom_lookup, start_bloom, reload_bloom_filter
from spellcheck.symspell_suggestions import suggestionReturner
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
        subprocess.Popen([exe_path], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         start_new_session=True)

    except Exception as e:
        print(f"Error starting background exe: {e}")


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        start_background_exe()

    def initUI(self):

        #self.text_edit = KannadaTextEdit()
        self.text_edit = QTextEdit(self)

        self.setCentralWidget(self.text_edit)
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.showContextMenu)
        # Create a QFont with the "Noto Sans Kannada" font family
        font_url = "resources/static/Nudi_fonts/NudiParijatha.ttf"
        self.font_id = QFontDatabase.addApplicationFont(font_url)
        self.family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.text_edit.installEventFilter(self)
        self.loadStyleSheet('resources/static/css/styles.css')

        self.css_style = 'color: black; text-decoration: underline; text-decoration-color: red; text-decoration-thickness: 2px;'

        current_font = self.text_edit.currentFont()
        new_font_size = 15
        new_font = current_font
        new_font.setPointSize(new_font_size)
        new_font.setFamily(self.family)
        self.text_edit.setFont(new_font)
        # ----------------------------------------------------------------file Menu Bar start----------------------------------------------------------------
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')
        open_action = QAction(QIcon('resources/images/stock_open-16.png'), 'Open', self)
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon('resources/images/stock_save.png'), 'Save', self)
        save_action.triggered.connect(self.saveFile)
        file_menu.addAction(save_action)

        save_as_action = QAction(QIcon('resources/images/stock_save-16.png'), 'Save As', self)
        save_as_action.triggered.connect(self.saveFileAs)
        file_menu.addAction(save_as_action)

        save_as_docx_action = QAction('Save As .docx', self)
        save_as_docx_action.triggered.connect(self.saveFileAsDocx)
        file_menu.addAction(save_as_docx_action)

        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        cut_action = QAction(QIcon('resources/images/stock_cut.png'), 'Cut', self)
        cut_action.setShortcut('Ctrl+x')
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon('resources/images/stock_copy.png'), 'Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon('resources/images/stock_paste.png'), 'Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

        edit_undo_action = QAction(QIcon('resources/images/undo.png'), 'Undo', self)
        edit_undo_action.setShortcut('Ctrl+Z')
        edit_undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(edit_undo_action)

        edit_redo_action = QAction(QIcon('resources/images/redo.png'), 'Redo', self)
        edit_redo_action.setShortcut('Ctrl+Y')
        edit_redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(edit_redo_action)

        ##----------------------------------------------------------------Menu--------------------------------------------------------
        # Font size menu
        font_size_menu = menubar.addMenu('Font')

        increase_font_size_action = QAction('Increase Font Size (+)', self)
        increase_font_size_action.setShortcut('Ctrl++')  # Set the shortcut (e.g., Ctrl++)
        increase_font_size_action.triggered.connect(self.increaseFontSize)
        font_size_menu.addAction(increase_font_size_action)

        decrease_font_size_action = QAction('Decrease Font Size (-)', self)
        decrease_font_size_action.setShortcut('Ctrl+-')  # Set the shortcut (e.g., Ctrl+-)
        decrease_font_size_action.triggered.connect(self.decreaseFontSize)
        font_size_menu.addAction(decrease_font_size_action)
        # Add more font actions as needed

        #----------------------------------------------------------------tool bar----------------------------------------------------------------
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        # Add actions with icons to the toolbar
        open_action = QAction(QIcon('resources/images/stock_open.png'), 'Open', self)
        open_action.triggered.connect(self.openFile)
        toolbar.addAction(open_action)

        save_action = QAction(QIcon('resources/images/stock_save.png'), 'Save', self)
        save_action.triggered.connect(self.saveFile)
        toolbar.addAction(save_action)

        refresh_action = QAction(QIcon('resources/images/refresh.png'), 'Refresh and Recheck', self)
        refresh_action.triggered.connect(self.refresh_recheck)
        toolbar.addAction(refresh_action)

        undo_action = QAction(QIcon('resources/images/undo.png'), 'Undo', self)
        undo_action.triggered.connect(self.text_edit.undo)
        toolbar.addAction(undo_action)

        redo_action = QAction(QIcon('resources/images/redo.png'), 'Redo', self)
        redo_action.triggered.connect(self.text_edit.redo)
        toolbar.addAction(redo_action)

        bold_action = QAction(QIcon('resources/images/bold.png'), 'Bold', self)
        bold_action.setShortcut('Ctrl+B')
        bold_action.triggered.connect(self.toggleBold)
        toolbar.addAction(bold_action)

        italic_action = QAction(QIcon('resources/images/italic.png'), 'Italic', self)
        italic_action.setShortcut('Ctrl+I')
        italic_action.triggered.connect(self.toggleItalic)
        toolbar.addAction(italic_action)

        underline_action = QAction(QIcon('resources/images/underline.png'), 'Underline', self)
        underline_action.setShortcut('Ctrl+U')
        underline_action.triggered.connect(self.toggleUnderline)
        toolbar.addAction(underline_action)

        #-alinment
        align_left_action = QAction(QIcon("resources/images/align-left.png"), "Align Left", self)
        align_left_action.triggered.connect(lambda: self.alignText("left"))
        toolbar.addAction(align_left_action)

        align_center_action = QAction(QIcon("resources/images/align-center.png"), "Align Center", self)
        align_center_action.triggered.connect(lambda: self.alignText("center"))
        toolbar.addAction(align_center_action)

        align_right_action = QAction(QIcon("resources/images/align-right.png"), "Align Right", self)
        align_right_action.triggered.connect(lambda: self.alignText("right"))
        toolbar.addAction(align_right_action)

        align_justify_action = QAction(QIcon("resources/images/align-justify.png"), "Align justify", self)
        align_justify_action.triggered.connect(lambda: self.alignText("justify"))
        toolbar.addAction(align_justify_action)
        #list

        bullet_list_action = QAction(QIcon("resources/images/bullet-list.png"), "Bullet List", self)
        bullet_list_action.setCheckable(True)  # Make the action checkable
        bullet_list_action.triggered.connect(self.toggleBulletList)  # Connect to toggle method
        toolbar.addAction(bullet_list_action)
        self.bullet_list_active = False  # Keep track of bullet list status

        number_list_action = QAction(QIcon("resources/images/number-list.png"), "Number List", self)
        number_list_action.setCheckable(True)  # Make the action checkable
        number_list_action.triggered.connect(self.toggleNumberList)  # Connect to toggle method
        toolbar.addAction(number_list_action)
        self.number_list_active = False  # Keep track of number list status

        font_color_action = QAction(QIcon("resources/images/font-color.png"), "Choose Font Color", self)
        font_color_action.triggered.connect(self.chooseFontColor)
        toolbar.addAction(font_color_action)

        copy_action = QAction(QIcon("resources/images/stock_copy.png"), "Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)  # Set shortcut (Ctrl+C) for copy action
        copy_action.triggered.connect(self.text_edit.copy)  # Connect to QTextEdit's copy method
        toolbar.addAction(copy_action)

        cut_action = QAction(QIcon("resources/images/stock_cut.png"), "Cut", self)
        cut_action.setShortcut(QKeySequence.Cut)  # Set shortcut (Ctrl+X) for cut action
        cut_action.triggered.connect(self.text_edit.cut)  # Connect to QTextEdit's cut method
        toolbar.addAction(cut_action)

        paste_action = QAction(QIcon("resources/images/stock_paste.png"), "Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)  # Set shortcut (Ctrl+V) for paste action
        paste_action.triggered.connect(self.text_edit.paste)  # Connect to QTextEdit's paste method
        toolbar.addAction(paste_action)


        # Add Insert Table action button to the toolbar
        insert_table_action = QAction(QIcon('resources/images/insert-table.png'), 'Insert Table', self)
        insert_table_action.triggered.connect(self.insertTable)
        toolbar.addAction(insert_table_action)


        # Add Insert Picture action button to the toolbar
        insert_picture_action = QAction(QIcon('resources/images/add-image.png'), 'Insert Picture', self)
        insert_picture_action.triggered.connect(self.choose_image)
        toolbar.addAction(insert_picture_action)


        #----------------------------------------------------------------Editor Size Settings----------------------------------------------------------------
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Kannada Spellchecker')
        self.setWindowIcon(QIcon('resources/images/logo.jpg'))  # Set the application icon
        self.show()



    def loadStyleSheet(self, file_path):
        style_sheet = QFile(file_path)
        if not style_sheet.open(QFile.ReadOnly | QFile.Text):
            return
        style_stream = QTextStream(style_sheet)
        self.setStyleSheet(style_stream.readAll())

    def openFile(self):
        format = QTextCharFormat()
        format.setForeground(Qt.red)  # You can set the color to any color you want
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '',
                                                   'All Files (*);;Word Documents (*.docx);Text Files (*.txt);',
                                                   options=options)
        if file_name:
            if file_name.endswith('.docx'):
                doc = docx.Document(file_name)
                paragraphs = [paragraph.text for paragraph in doc.paragraphs]
                content = "<br>".join(paragraphs)  # Preserve line breaks
            else:
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
            import time
            start_time = time.time()
            content_for_bloom = [get_clean_words_for_dictionary(word) for word in content.split() if word if
                                 len(word) > 1]
            print("clean_up time: ", time.time() - start_time)
            start_time = time.time()
            wrong_words = start_bloom(content_for_bloom)
            print("time taken to find wrong words: ", time.time() - start_time)
            start_time = time.time()
            for word in wrong_words:
                content = content.replace(word, f'<span style="{self.css_style}">{word}</span>')

            print("time taken to hilight words : ", time.time() - start_time)
            self.setWindowTitle('Kannada Spellchecker - ' + file_name)
            current_font = self.text_edit.currentFont()
            new_font_size = 12
            new_font = current_font
            new_font.setPointSize(new_font_size)
            new_font.setFamily(self.family)
            self.text_edit.setFont(new_font)
            self.text_edit.setHtml(content)

    def saveFile(self):
        if hasattr(self, 'current_file'):
            with open(self.current_file, 'w', encoding='utf-8') as file:
                if (len(self.text_edit.toPlainText()) == 0):
                    print("No content")
                file.write(self.text_edit.toPlainText())
        else:
            self.saveFileAs()

    def saveFileAs(self):
        content = self.text_edit.toPlainText()
        if len(content) == 0:
            QMessageBox.warning(self, 'Warning', 'No content to save.')
            return
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;All Files (*)',
                                                   options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.toPlainText())
            self.current_file = file_name

    def saveFileAsDocx(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save As .docx', '', 'Word Documents (*.docx);;All Files (*)',
                                                   options=options)
        if file_name:
            doc = docx.Document()
            doc.add_paragraph(self.text_edit.toPlainText())
            doc.save(file_name)

    def showContextMenu(self, pos):
        cursor = self.text_edit.cursorForPosition(pos)
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

            menu.exec_(self.text_edit.mapToGlobal(pos))

    def addToDictionary(self, word):
        with open(fp.bloomfilter_data, 'a', encoding='utf-8') as dict_file:
            word = get_clean_words_for_dictionary(word)
            if not bloom_lookup(word):
                dict_file.write(word + '\n')
                with open(fp.symspell_word_freq_data, 'a', encoding='utf-8') as file:
                    file.write(f"{word} {1}\n")
                    print(word, "successfully Added to Dictionary")

                # Remove underline from the word
                cursor = self.text_edit.textCursor()
                cursor.beginEditBlock()  # Begin editing block to improve performance
                format = QTextCharFormat()
                format.setForeground(self.text_edit.palette().color(self.text_edit.foregroundRole()))
                format.setUnderlineStyle(QTextCharFormat.NoUnderline)  # Clear underline
                cursor.mergeCharFormat(format)
                cursor.endEditBlock()
            else:
                print("word already present in Dictionary file")

    def ignore_word(self, word):
        cursor = self.text_edit.textCursor()
        cursor.beginEditBlock()  # Begin editing block to improve performance

        format = QTextCharFormat()
        format.setForeground(self.text_edit.palette().color(self.text_edit.foregroundRole()))

        # Clear underline
        format.setUnderlineStyle(QTextCharFormat.NoUnderline)

        cursor.mergeCharFormat(format)
        cursor.endEditBlock()

    def replace_word(self, word_to_replace):
        new_word, ok = QInputDialog.getText(self, 'Replace Word', f'Enter new word to replace {word_to_replace}',
                                            QLineEdit.Normal)
        if ok and new_word:
            cursor = self.text_edit.textCursor()  # Get the current cursor position
            current_text = self.text_edit.toPlainText()
            new_text = current_text.replace(word_to_replace, new_word)
            self.text_edit.setPlainText(new_text)
            # Restore the cursor position
            cursor.setPosition(cursor.position() + len(new_word))
            self.text_edit.setTextCursor(cursor)

    def increaseFontSize(self):
        current_font = self.text_edit.currentFont()
        new_font_size = current_font.pointSize() + 2
        new_font = current_font
        new_font.setPointSize(new_font_size)
        new_font.setFamily(self.family)
        self.text_edit.setFont(new_font)

    def decreaseFontSize(self):
        current_font = self.text_edit.currentFont()
        new_font_size = max(current_font.pointSize() - 2, 2)  # Ensure font size doesn't go below 2
        new_font = current_font
        new_font.setPointSize(new_font_size)
        new_font.setFamily(self.family)
        self.text_edit.setFont(new_font)

    def changeFontSize(self, delta):
        current_font = self.text_edit.currentFont()
        new_font_size = max(current_font.pointSize() + delta, 2)
        new_font = current_font
        new_font.setPointSize(new_font_size)
        self.text_edit.setFont(new_font)

    def enlargeText(self):
        self.changeFontSize(2)

    def shrinkText(self):
        self.changeFontSize(-2)

    def wheelEvent(self, event):
        # Check if Ctrl key is pressed
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            # Determine whether the scroll is up or down
            delta = event.angleDelta().y()
            if delta > 0:
                self.enlargeText()
            elif delta < 0:
                self.shrinkText()

    def refresh_recheck(self):
        reload_bloom_filter()
        cursor_position = self.text_edit.textCursor()
        text_content = self.text_edit.toHtml()
        plain_text = self.text_edit.toPlainText()
        content_for_bloom = [get_clean_words_for_dictionary(word) for word in plain_text.split() if word if
                             len(word) > 1]
        wrong_words = start_bloom(content_for_bloom)
        # Highlight incorrect words in the editor
        highlighted_content = text_content
        for word in wrong_words:
            highlighted_content = highlighted_content.replace(word, f'<span style="{self.css_style}">{word}</span>')
        # Update the editor with the highlighted content
        self.text_edit.setHtml(highlighted_content)
        # Restore the cursor position
        self.text_edit.setTextCursor(cursor_position)

    def eventFilter(self, obj, event):
        if obj == self.text_edit and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Space:
                #self.text_edit.is_space(True)
                self.spacebarClicked()
                return True  # Event handled
        return super().eventFilter(obj, event)

    def spacebarClicked(self):
        cursor = self.text_edit.textCursor()
        cursor_position = self.text_edit.textCursor()
        # Save the current position of the cursor
        original_position = cursor.position()
        # Insert a space
        cursor.insertText(" ")
        # Move the cursor to the left of the current position
        cursor.movePosition(QTextCursor.WordLeft)
        # Retrieve the entire word to the left of the cursor using a regular expression
        cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
        word_left_of_cursor = cursor.selectedText()
        # Restore the cursor to the original position
        #cursor.setPosition(original_position)
        if has_letters_or_digits(word_left_of_cursor):
            print("correct word")
        elif not bloom_lookup(word_left_of_cursor):
            wrong_word = f'<span style="{self.css_style}">{word_left_of_cursor.strip()}</span> '

            html_content = self.text_edit.toHtml()
            new_html_content = html_content.replace(word_left_of_cursor.lstrip(), wrong_word.strip(), 1)
            # Set the new HTML content
            self.text_edit.setHtml(new_html_content)
            # Move the cursor to the right of the replaced word
            cursor.movePosition(QTextCursor.Right)
            self.text_edit.setTextCursor(cursor)

    def getWordLeftOfCursor(self):
        cursor = self.text_edit.textCursor()
        # Save the current position of the cursor
        original_position = cursor.position()
        # Move the cursor to the left of the current position
        cursor.movePosition(QTextCursor.WordLeft)
        # Retrieve the entire word to the left of the cursor using a regular expression
        cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
        word_left_of_cursor = cursor.selectedText()
        # Restore the cursor to the original position
        cursor.setPosition(original_position)
        return word_left_of_cursor.strip()

    def toggleBold(self):
        font = self.text_edit.currentFont()
        font.setBold(not font.bold())
        self.text_edit.setCurrentFont(font)

    def toggleItalic(self):
        font = self.text_edit.currentFont()
        font.setItalic(not font.italic())
        self.text_edit.setCurrentFont(font)

    def toggleUnderline(self):
        font = self.text_edit.currentFont()
        font.setUnderline(not font.underline())
        self.text_edit.setCurrentFont(font)

    def alignText(self, alignment):
        cursor = self.text_edit.textCursor()
        cursor.setPosition(0)
        cursor.movePosition(cursor.End, cursor.KeepAnchor)

        # Retrieve the current QTextBlockFormat
        block_format = cursor.blockFormat()

        # Set alignment on the block format
        if alignment == "left":
            block_format.setAlignment(Qt.AlignLeft)
        elif alignment == "center":
            block_format.setAlignment(Qt.AlignCenter)
        elif alignment == "right":
            block_format.setAlignment(Qt.AlignRight)
        elif alignment == "justify":
            block_format.setAlignment(Qt.AlignJustify)

        # Apply the modified format back to the text block
        cursor.mergeBlockFormat(block_format)
        self.text_edit.setTextCursor(cursor)

    def toggleBulletList(self, checked):
        if checked:  # If the action is checked
            self.insertBulletList()  # Insert bullet list
        else:
            self.clearBulletList()  # Clear bullet list

    def insertBulletList(self):
        cursor = self.text_edit.textCursor()
        cursor.insertList(QTextListFormat.ListDisc)
        self.bullet_list_active = True  # Update status

    def clearBulletList(self):
        cursor = self.text_edit.textCursor()
        cursor.clearSelection()
        cursor.select(QTextCursor.BlockUnderCursor)
        cursor.setBlockFormat(QTextBlockFormat())
        self.bullet_list_active = False  # Update status

    def toggleNumberList(self, checked):
        if checked:  # If the action is checked
            self.insertNumberList()  # Insert number list
        else:
            self.clearNumberList()  # Clear number list

    def insertNumberList(self):
        cursor = self.text_edit.textCursor()
        cursor.insertList(QTextListFormat.ListDecimal)
        self.number_list_active = True  # Update status

    def clearNumberList(self):
        cursor = self.text_edit.textCursor()
        cursor.clearSelection()
        cursor.select(QTextCursor.BlockUnderCursor)
        cursor.setBlockFormat(QTextBlockFormat())
        self.number_list_active = False  # Update status

    def chooseFontColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextColor(color)


    def insertTable(self):
        rows, ok1 = QInputDialog.getInt(self, "Table", "Rows:", 3, 1, 50, 1)
        cols, ok2 = QInputDialog.getInt(self, "Table", "Columns:", 3, 1, 50, 1)

        if ok1 and ok2:
            table = QTableWidget(rows, cols, self)
            for row in range(rows):
                for col in range(cols):
                    item = QTableWidgetItem()
                    table.setItem(row, col, item)

            cursor = self.text_edit.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.End)
            cursor.insertTable(rows, cols)

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
                cursor = self.text_edit.textCursor()
                cursor.insertImage(modified_image)