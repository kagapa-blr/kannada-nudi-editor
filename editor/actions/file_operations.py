import pypandoc
from PyQt5.QtWidgets import QFileDialog
from docx import Document


class FileOperation:
    def __init__(self, editor):
        self.editor = editor

    def handle_open_file(self):

        options = QFileDialog.Options()
        self.editor.filename, _ = QFileDialog.getOpenFileName(
            self.editor,
            "Open File",
            "",
            "All Files (*);;Text Files (*.txt);;Word Documents (*.docx);;Rich Text Format (*.rtf)",
            options=options
        )
        if self.editor.filename:
            self.editor.content = ""
            file_extension = self.editor.filename.split('.')[-1].lower()

            try:
                if file_extension == 'txt':
                    with open(self.editor.filename, 'r', encoding="utf-8") as file:
                        content = file.read()

                elif file_extension == 'docx':
                    doc = Document(self.editor.filename)
                    content = '\n'.join([para.text for para in doc.paragraphs])

                elif file_extension == 'rtf':
                    content = pypandoc.convert_file(self.editor.filename, 'plain', format='rtf')

                else:
                    raise ValueError("Unsupported file format")

                # Split content into chunks of approximately 490 words
                words = content.split()
                word_limit = 490
                current_word_count = 0
                current_page_content = []

                for word in words:
                    current_page_content.append(word)
                    current_word_count += 1

                    if current_word_count >= word_limit:
                        self.editor.addPageWithContent(' '.join(current_page_content))
                        current_page_content = []
                        current_word_count = 0

                # Add any remaining content to a new page if not empty
                if current_page_content:
                    self.editor.addPageWithContent(' '.join(current_page_content))

            except Exception as e:
                self.editor.error_dialog.show_error_popup(f"Error opening file: {str(e)}")

            # Update window title and remove blank pages
            self.editor.setWindowTitle("ಕನ್ನಡ ನುಡಿ - " + self.editor.access_filename())
            self.editor.removeBlankPages()
            self.editor.statusbar.setStatusTip(f"Total pages: {self.editor.total_pages}")

            # Set the current file path
            self.editor.current_file_path = self.editor.filename
