from PyQt5.QtGui import QFont


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
