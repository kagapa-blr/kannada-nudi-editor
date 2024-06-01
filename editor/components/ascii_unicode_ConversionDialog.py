from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

from utils.asciitounicode import process_line


def show_error_popup(error_message):
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Critical)
    error_box.setWindowTitle("Error")
    error_box.setText("An error occurred:")
    error_box.setInformativeText(error_message)
    error_box.exec_()


class ConversionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filename = None
        self.setWindowTitle("ASCII ಮತ್ತು ಯುನಿಕೋಡ್ ಪರಿವರ್ತಕ - Untitled")

        # Set default font to NudiParijatha
        default_font = QtGui.QFont("NudiParijatha", 12)
        self.unsaved_changes = False
        self.setFont(default_font)

        self.initUI()

    def initUI(self):
        self.ascii_editor = QtWidgets.QTextEdit(self)
        self.ascii_editor.setMinimumSize(500, 450)
        self.ascii_editor.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.ascii_editor.textChanged.connect(self.mark_unsaved_changes)

        self.unicode_editor = QtWidgets.QTextEdit(self)
        self.unicode_editor.setReadOnly(False)
        self.unicode_editor.setMinimumSize(500, 450)
        self.unicode_editor.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.convert_to_unicode_button = QtWidgets.QPushButton("ಯುನಿಕೋಡ್‌ಗೆ ಪರಿವರ್ತಿಸು", self)
        self.convert_to_unicode_button.clicked.connect(self.convert_to_unicode)

        self.convert_to_ascii_button = QtWidgets.QPushButton("ASCII ಗೆ ಪರಿವರ್ತಿಸು", self)
        self.convert_to_ascii_button.clicked.connect(self.convert_to_ascii)

        self.reset_button = QtWidgets.QPushButton("ಮರುಹೊಂದಿಸಿ", self)
        self.reset_button.clicked.connect(self.reset_editors)

        ascii_label = QtWidgets.QLabel("ASCII ಇನ್‌ಪುಟ್")
        unicode_label = QtWidgets.QLabel("ಯುನಿಕೋಡ್ ಔಟ್")

        layout = QtWidgets.QVBoxLayout()
        editor_layout = QtWidgets.QHBoxLayout()

        ascii_layout = QtWidgets.QVBoxLayout()
        unicode_layout = QtWidgets.QVBoxLayout()

        ascii_layout.addWidget(ascii_label)
        ascii_layout.addWidget(self.ascii_editor)
        unicode_layout.addWidget(unicode_label)
        unicode_layout.addWidget(self.unicode_editor)

        editor_layout.addLayout(ascii_layout)
        editor_layout.addLayout(unicode_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.convert_to_unicode_button)
        button_layout.addWidget(self.convert_to_ascii_button)
        button_layout.addWidget(self.reset_button)

        layout.addLayout(editor_layout)
        layout.addStretch()  # Add stretch to push buttons to the bottom
        layout.addLayout(button_layout)

        # Add toolbar to the layout
        self.toolbar = QtWidgets.QToolBar('Main Toolbar')
        self.toolbar.addAction(QtGui.QIcon('icons/save.png'), 'Save')
        layout.addWidget(self.toolbar)

        self.setLayout(layout)
        self.resize(800, 600)

        self.initFormatbar()
        self.initMenubar()

    def initFormatbar(self):
        self.formatbar = QtWidgets.QToolBar('Format Toolbar')
        self.formatbar.addAction(QtGui.QIcon('icons/bold.png'), 'Bold')
        self.formatbar.addAction(QtGui.QIcon('icons/italic.png'), 'Italic')
        self.layout().addWidget(self.formatbar)

    def initMenubar(self):
        menubar = QtWidgets.QMenuBar()

        file_menu = menubar.addMenu('File')
        file_menu.addAction('Open ASCII File', self.open_ascii_file)
        file_menu.addAction('Open Unicode File', self.open_unicode_file)
        file_menu.addAction('Save', self.save_file)
        file_menu.addAction('Save As TXT', lambda: self.save_file_as('txt'))
        file_menu.addAction('Save As DOCX', lambda: self.save_file_as('docx'))
        file_menu.addAction('Save As PDF', lambda: self.save_file_as('pdf'))

        edit_menu = menubar.addMenu('Edit')
        edit_menu.addAction('Copy')
        edit_menu.addAction('Cut')
        edit_menu.addAction('Paste')

        self.layout().setMenuBar(menubar)

    def open_ascii_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open ASCII File', '',
                                                             'Text files (*.txt);;Word files (*.docx)')
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    ascii_text = file.read()
                    self.ascii_editor.setPlainText(ascii_text)
                    self.filename = file_path
                    self.update_window_title()
            except Exception as e:
                error_message = str(e)
                show_error_popup(error_message)

    def open_unicode_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Unicode File', '',
                                                             'Text files (*.txt);;Word files (*.docx)')
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    unicode_text = file.read()
                    self.unicode_editor.setPlainText(unicode_text)
                    self.filename = file_path
                    self.update_window_title()
            except Exception as e:
                error_message = str(e)
                show_error_popup(error_message)

    def save_file(self):
        if self.filename:
            try:
                with open(self.filename, 'w', encoding='utf-8') as file:
                    file.write(self.ascii_editor.toPlainText())
                self.unsaved_changes = False
            except Exception as e:
                error_message = str(e)
                show_error_popup(error_message)
        else:
            self.save_file_as('txt')

    def save_file_as(self, file_format):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File As', '',
                                                             f'{file_format.upper()} files (*.{file_format});;All files (*.*)')
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.ascii_editor.toPlainText())
                self.filename = file_path
                self.update_window_title()
                self.unsaved_changes = False
            except Exception as e:
                error_message = str(e)
                show_error_popup(error_message)

    def convert_to_unicode(self):
        ascii_text = self.ascii_editor.toPlainText()
        unicode_text = ""
        for line in ascii_text.split('\n'):
            processed_line = process_line(line)
            unicode_text += processed_line + '\n'
        self.unicode_editor.setPlainText(unicode_text.strip())

    def convert_to_ascii(self):
        unicode_text = self.unicode_editor.toPlainText()
        try:
            # Convert Unicode to ASCII
            ascii_text = unicode_text.encode('unicode_escape').decode()
            self.ascii_editor.setPlainText(ascii_text)
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            error_message = str(e)
            show_error_popup(error_message)
            self.ascii_editor.setPlainText("ಅಮಾನ್ಯ ಯುನಿಕೋಡ್ ಇನ್‌ಪುಟ್")

    def reset_editors(self):
        self.ascii_editor.clear()
        self.unicode_editor.clear()
        self.filename = None
        self.update_window_title()

    def mark_unsaved_changes(self):
        self.unsaved_changes = True

    def update_window_title(self):
        if self.filename:
            self.setWindowTitle(f"ASCII ಮತ್ತು ಯುನಿಕೋಡ್ ಪರಿವರ್ತಕ - {self.filename}")
        else:
            self.setWindowTitle("ASCII ಮತ್ತು ಯುನಿಕೋಡ್ ಪರಿವರ್ತಕ - Untitled")

    def closeEvent(self, event):
        if self.unsaved_changes:
            reply = QMessageBox.question(self, 'ಸೂಚನೆ',
                                         "ನೀವು ಉಳಿಸದ ಬದಲಾವಣೆಗಳನ್ನು ಹೊಂದಿದ್ದೀರಿ. ನಿಮ್ಮ ಬದಲಾವಣೆಗಳನ್ನು ಉಳಿಸಲು ನೀವು ಬಯಸುವಿರಾ?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                self.save_file()
                event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

