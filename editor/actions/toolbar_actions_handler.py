import time

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QTextCharFormat, QTextCursor, QTextListFormat, QTextBlockFormat
from PyQt5.QtWidgets import QColorDialog, QDialog, QMessageBox, QApplication

from editor.components.format_content import SpacingDialog
from spellcheck.bloom_filter import start_bloom
from utils.corpus_clean import get_clean_words_for_dictionary


class ToolbarHandler:
    def __init__(self, editor):
        self.editor = editor

    def handle_font_size(self):
        size = int(self.editor.actions.fontSizeComboBox.currentText())
        if self.editor.current_page and hasattr(self.editor.current_page, 'editor'):
            try:
                self.editor.current_page.editor.setFontPointSize(size)
                print('setFontPointSize', size)
            except RuntimeError as e:
                print(f"Error setting font size: {str(e)}")
        else:
            self.editor.setActivePage(self.editor.current_page)
            print("Error: No current page or editor not available")

    def handle_toggle_bold(self):
        if self.editor.current_page:
            editor = self.editor.current_page.editor
            cursor = editor.textCursor()
            selected_text = cursor.selectedText()
            current_weight = editor.fontWeight()
            new_weight = QFont.Normal if current_weight == QFont.Bold else QFont.Bold
            editor.setFontWeight(new_weight)

    def handle_toggle_italic(self):
        if self.editor.current_page:
            state = self.editor.current_page.editor.fontItalic()
            self.editor.current_page.editor.setFontItalic(not state)

    def handle_toggle_underline(self):
        if self.editor.current_page:
            state = self.editor.current_page.editor.fontUnderline()
            self.editor.current_page.editor.setFontUnderline(not state)

    def handle_toggle_strikethrough(self):
        if self.editor.current_page:
            fmt = self.editor.current_page.editor.currentCharFormat()
            fmt.setFontStrikeOut(not fmt.fontStrikeOut())
            self.editor.current_page.editor.setCurrentCharFormat(fmt)

    def handle_font_color(self):
        # Get a color from the text dialog
        color = QColorDialog.getColor()
        # Set it as the new text color
        self.editor.current_page.editor.setTextColor(color)

    def handle_super_script(self):
        # Grab the current format
        fmt = self.editor.current_page.editor.currentCharFormat()
        # And get the vertical alignment property
        align = fmt.verticalAlignment()
        # Toggle the state
        if align == QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)
        # Set the new format
        self.editor.current_page.editor.setCurrentCharFormat(fmt)

    def handle_sub_script(self):
        # Grab the current format
        fmt = self.editor.current_page.editor.currentCharFormat()
        # And get the vertical alignment property
        align = fmt.verticalAlignment()
        # Toggle the state
        if align == QTextCharFormat.AlignNormal:
            fmt.setVerticalAlignment(QTextCharFormat.AlignSubScript)
        else:

            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)
        # Set the new format
        self.editor.current_page.editor.setCurrentCharFormat(fmt)

    def handle_indent(self):
        # Grab the cursor
        cursor = self.editor.current_page.editor.textCursor()
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

    def handle_dedent(self):
        cursor = self.editor.current_page.editor.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)

        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.anchor())
            diff = cursor.blockNumber() - temp
            direction = QTextCursor.Up if diff > 0 else QTextCursor.Down

            for _ in range(abs(diff) + 1):
                line = cursor.block().text()
                if line.startswith("\t"):
                    cursor.deleteChar()
                else:
                    for char in line[:8]:
                        if char != " ":
                            break
                        cursor.deleteChar()
                cursor.movePosition(direction)
        else:
            line = cursor.block().text()
            if line.startswith("\t"):
                cursor.deleteChar()
            else:
                for char in line[:8]:
                    if char != " ":
                        break
                    cursor.deleteChar()

    def handle_bullet_list(self):
        cursor = self.editor.current_page.editor.textCursor()
        # Insert bulleted list
        cursor.insertList(QTextListFormat.ListDisc)

    def handle_number_list(self):
        cursor = self.editor.current_page.editor.textCursor()
        # Insert list with numbers
        cursor.insertList(QTextListFormat.ListDecimal)

    def handle_highlight(self):
        color = QColorDialog.getColor()
        self.editor.current_page.editor.setTextBackgroundColor(color)

    def handle_set_spacing(self):
        if not self.editor.current_page or not self.editor.current_page.editor:
            print("Error: current_page or editor is not valid.")
            return

        dialog = SpacingDialog(self.editor)
        dialog.setWindowTitle('Line & Paragraph Spacing')

        # Retrieve current font pixel size if available
        current_font = self.editor.current_page.editor.currentFont()
        if current_font:
            dialog.customLineSpacingSpinBox.setValue(current_font.pixelSize())

        dialog.beforeParagraphSpinBox.setValue(0)
        dialog.afterParagraphSpinBox.setValue(0)

        if dialog.exec_() == QDialog.Accepted:
            dialog.applySettings()

    def handle_set_line_spacing(self, value):
        cursor = self.editor.current_page.editor.textCursor()
        fmt = cursor.blockFormat()
        fmt.setLineHeight(value, QTextBlockFormat.LineDistanceHeight)
        cursor.setBlockFormat(fmt)

    def handle_refresh_recheck(self):
        self.editor.total_pages = 0
        total_words = 0
        total_incorrect_words = 0
        start_time = time.time()

        for page in self.editor.pages:
            self.editor.total_pages += 1
            if not page or not page.editor:
                print("Page or editor is not valid.")
                continue

            # Retrieve plain text from current page's editor
            plain_text = page.editor.toPlainText()

            # Count total words
            words = plain_text.split()
            total_words += len(words)

            # Process text content for spell checking
            content_for_bloom = [get_clean_words_for_dictionary(word) for word in words if len(word) > 1]
            wrong_words = start_bloom(content_for_bloom)

            # Count total incorrect words
            total_incorrect_words += len(wrong_words)

            # Get the existing HTML content to preserve formatting and alignment
            highlighted_content = page.editor.toHtml()

            # Wrap the incorrect words with an inline style for red underline
            for word in wrong_words:
                # Use inline styling for red underline
                highlighted_content = highlighted_content.replace(word,
                                                                  f'<span style="text-decoration: underline; text-decoration-color: red;">{word}</span>')

            # Update the editor with the highlighted content
            page.editor.setHtml(highlighted_content)

        end_time = time.time()
        spellcheck_time = end_time - start_time

        # Show info dialog with the requested information and parent window's logo
        info_msg = QMessageBox()
        info_msg.setWindowTitle("ವರದಿ ಪರಿಶೀಲನೆ ಮಾಹಿತಿ")
        info_msg.setText(f"ಒಟ್ಟು ಪದಗಳ ಸಂಖ್ಯೆ : {total_words}\n"
                         f"ತಪ್ಪು ಪದಗಳ ಸಂಖ್ಯೆ : {total_incorrect_words}\n"
                         f"ಕಾಗುಣಿತ ಪರಿಶೀಲನೆಗಾಗಿ ತೆಗೆದುಕೊಂಡ ಒಟ್ಟು ಸಮಯ : {spellcheck_time:.2f} ಸೆಕೆಂಡುಗಳು")
        info_msg.setIcon(QMessageBox.Information)

        # Set the parent window's icon for the message box
        parent_icon = self.editor.windowIcon()
        if parent_icon:
            info_msg.setWindowIcon(parent_icon)
        info_msg.exec_()
        self.editor.removeBlankPages()
        self.editor.statusBar().showMessage("ಒಟ್ಟು ಪುಟಗಳು: " + str(self.editor.total_pages))
        # Automatically close the message box after 5 seconds
        QTimer.singleShot(5000, info_msg.close)
        # Ensure the application processes the event loop to display the message box
        QApplication.processEvents()


