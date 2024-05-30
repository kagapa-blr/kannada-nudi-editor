from PyQt5 import QtWidgets


class ConversionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ASCII and Unicode Converter")

        self.ascii_editor = QtWidgets.QTextEdit(self)
        self.unicode_editor = QtWidgets.QTextEdit(self)
        self.unicode_editor.setReadOnly(False)

        self.convert_to_unicode_button = QtWidgets.QPushButton("Convert to Unicode", self)
        self.convert_to_unicode_button.clicked.connect(self.convert_to_unicode)

        self.convert_to_ascii_button = QtWidgets.QPushButton("Convert to ASCII", self)
        self.convert_to_ascii_button.clicked.connect(self.convert_to_ascii)

        ascii_label = QtWidgets.QLabel("ASCII Input")
        unicode_label = QtWidgets.QLabel("Unicode Output")

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

        layout.addLayout(editor_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.resize(800, 400)

    def convert_to_unicode(self):
        ascii_text = self.ascii_editor.toPlainText()
        try:
            unicode_text = ascii_text.encode('unicode_escape').decode('ascii')
            self.unicode_editor.setPlainText(unicode_text)
        except UnicodeEncodeError:
            self.unicode_editor.setPlainText("Invalid ASCII input")

    def convert_to_ascii(self):
        unicode_text = self.unicode_editor.toPlainText()
        try:
            ascii_text = unicode_text.encode('ascii').decode('unicode_escape')
            self.ascii_editor.setPlainText(ascii_text)
        except (UnicodeEncodeError, UnicodeDecodeError):
            self.ascii_editor.setPlainText("Invalid Unicode input")
