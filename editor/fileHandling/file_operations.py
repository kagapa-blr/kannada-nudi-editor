import os

import pypandoc
from PyQt5.QtGui import QTextDocument, QTextCursor, QTextImageFormat, QTextBlockFormat
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QFileDialog
from docx import Document
from docx.shared import Inches

from utils.asciitounicode import process_line


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
                    content = "\n".join([para.text for para in doc.paragraphs])  # Maintain line breaks

                elif file_extension == 'rtf':
                    content = pypandoc.convert_file(self.editor.filename, 'plain', format='rtf')

                else:
                    raise ValueError("Unsupported file format")


                # **Split content by lines instead of words**
                lines = content.split("\n")

                current_page_content = []
                line_limit = 40  # Adjust as per your page capacity

                for line in lines:
                    current_page_content.append(line)

                    if len(current_page_content) >= line_limit:
                        self.editor.addPageWithContent("\n".join(current_page_content))
                        current_page_content = []

                # Add any remaining lines to a new page
                if current_page_content:
                    self.editor.addPageWithContent("\n".join(current_page_content))

            except Exception as e:
                self.editor.error_dialog.show_error_popup(f"Error opening file: {str(e)}")

            # Update window title and remove blank pages
            self.editor.setWindowTitle("ಕನ್ನಡ ನುಡಿ - " + self.editor.access_filename())
            self.editor.removeBlankPages()
            self.editor.statusbar.setStatusTip(f"Total pages: {self.editor.total_pages}")

            # Set the current file path
            self.editor.current_file_path = self.editor.filename

    def handle_save_file(self,content):
        if not self.editor.current_file_path:
            options = QFileDialog.Options()
            self.editor.current_file_path, _ = QFileDialog.getSaveFileName(
                self.editor, "Save File", "",
                "Text Files (*.txt);;Word Files (*.docx);;Rich Text Format (*.rtf);;PDF Files (*.pdf);;All Files (*)",
                options=options
            )

        if self.editor.current_file_path:
            try:
                if self.editor.current_file_path.endswith('.txt'):
                    with open(self.editor.current_file_path, 'w', encoding='utf-8') as file:
                        file.write(content)
                elif self.editor.current_file_path.endswith('.docx'):
                    doc = Document()
                    doc.add_paragraph(content)
                    doc.save(self.editor.current_file_path)
                elif self.editor.current_file_path.endswith('.rtf'):
                    pypandoc.convert_text(content, 'rtf', format='md', outputfile=self.editor.current_file_path,
                                          encoding='utf-8')
                elif self.editor.current_file_path.endswith('.pdf'):
                    printer = QPrinter(QPrinter.HighResolution)
                    printer.setOutputFormat(QPrinter.PdfFormat)
                    printer.setOutputFileName(self.editor.current_file_path)
                    doc = QTextDocument()
                    doc.setPlainText(content)
                    doc.print_(printer)
                else:
                    self.editor.error_dialog.show_error_popup("Unsupported file format")
            except Exception as e:
                self.editor.error_dialog.show_error_popup(str(e))

    def handle_save_as_file(self, content):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self.editor, "Save File", "",
            "Text Files (*.txt);;Word Files (*.docx);;Rich Text Format (*.rtf);;PDF Files (*.pdf);;All Files (*)",
            options=options
        )

        if file_path:
            try:
                # Capture alignment before saving
                cursor = self.editor.textCursor()
                alignment = cursor.blockFormat().alignment()

                # Detect images in the document
                doc_content = self.editor.document()
                images = []
                block = doc_content.begin()
                while block.isValid():
                    fragment = block.begin()
                    while fragment != block.end():
                        if fragment.fragment().charFormat().isImageFormat():
                            image_format = fragment.fragment().charFormat().toImageFormat()
                            images.append(image_format.name())
                        fragment += 1
                    block = block.next()

                # Save Text File
                if file_path.endswith('.txt'):
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)

                # Save Word Document (.docx) with images
                elif file_path.endswith('.docx'):
                    doc = Document()
                    paragraph = doc.add_paragraph(content)
                    paragraph.alignment = 1  # Align left (0=left, 1=center, 2=right, 3=justify)

                    for image in images:
                        if os.path.exists(image):
                            doc.add_picture(image, width=Inches(2))

                    doc.save(file_path)

                # Save RTF with images
                elif file_path.endswith('.rtf'):
                    pypandoc.convert_text(content, 'rtf', format='md', outputfile=file_path, encoding='utf-8')

                    # Append images manually
                    with open(file_path, 'a', encoding='utf-8') as file:
                        for image in images:
                            if os.path.exists(image):
                                file.write(f"{{\\pict\\jpegblip {image}}}")

                # **FIXED: Save as PDF with Images**
                elif file_path.endswith('.pdf'):
                    printer = QPrinter(QPrinter.HighResolution)
                    printer.setOutputFormat(QPrinter.PdfFormat)
                    printer.setOutputFileName(file_path)

                    doc = QTextDocument()
                    cursor = QTextCursor(doc)

                    # Insert text
                    cursor.insertText(content)

                    # Insert images
                    for image in images:
                        if os.path.exists(image):
                            cursor.insertBlock()
                            image_format = QTextImageFormat()
                            image_format.setName(image)
                            cursor.insertImage(image_format)

                    doc.print_(printer)

                else:
                    self.editor.error_dialog.show_error_popup("Unsupported file format")

                # Restore alignment after saving
                block_format = QTextBlockFormat()
                block_format.setAlignment(alignment)
                cursor.mergeBlockFormat(block_format)
                self.editor.setTextCursor(cursor)

            except Exception as e:
                self.editor.error_dialog.show_error_popup(str(e))

        # Update editor's current file path
        self.editor.current_file_path = file_path

    def handle_open_ascii_file(self):
        options = QFileDialog.Options()
        self.editor.filename, _ = QFileDialog.getOpenFileName(
            self.editor, "Open File", "",
            "All Files (*);;Text Files (*.txt);;Word Documents (*.docx);;Rich Text Format (*.rtf)",
            options=options)
        if self.editor.filename:
            content = ""
            file_extension = self.editor.filename.split('.')[-1].lower()

            try:
                if file_extension == 'txt':
                    with open(self.editor.filename, 'r', encoding="utf-8") as file:
                        unicode_lines = [process_line(line) for line in file]
                        content = ''.join(unicode_lines)
                elif file_extension == 'docx':
                    doc = Document(self.editor.filename)
                    paragraphs = [process_line(para.text) for para in doc.paragraphs]
                    content = "\n".join(paragraphs)
                elif file_extension == 'rtf':
                    plain_text = pypandoc.convert_file(self.editor.filename, 'plain', format='rtf')
                    unicode_lines = [process_line(line) for line in plain_text.splitlines()]
                    content = '\n'.join(unicode_lines)
                else:
                    self.editor.error_dialog("Unsupported file format")
                    # raise ValueError("Unsupported file format")

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
                self.editor.error_dialog.showError(str(e))

            # Update window title and remove blank pages
            self.editor.setWindowTitle("ಕನ್ನಡ ನುಡಿ - " + self.editor.access_filename())
            self.editor.removeBlankPages()