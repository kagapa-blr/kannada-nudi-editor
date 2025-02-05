from PyQt5.QtGui import QFont, QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import QColorDialog


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
