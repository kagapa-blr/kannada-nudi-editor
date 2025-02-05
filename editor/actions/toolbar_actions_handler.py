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