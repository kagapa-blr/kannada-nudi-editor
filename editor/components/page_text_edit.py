from PyQt5.QtGui import QTextImageFormat, QTextOption
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QFrame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QFrame


class PageTextEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Create a frame to simulate the page boundary
        page_frame = QFrame(self)
        page_frame.setFrameStyle(QFrame.Box)
        page_frame.setStyleSheet("QFrame { border: 1px solid black; }")

        # Create a text edit widget within the page frame
        self.text_edit = QTextEdit()
        self.text_edit.setFixedSize(600, 800)  # Set the initial page size
        self.text_edit.setFrameStyle(QFrame.NoFrame)

        # Configure QTextEdit for text wrapping around pictures
        self.text_edit.setWordWrapMode(QTextOption.WrapAnywhere)
        self.text_edit.setStyleSheet("background-color: white;")

        # Add some sample text and images
        self.insertTextWithPicture("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                   "Pellentesque ac lectus quis velit aliquet pharetra.")
        self.insertPicture("resources/image1.jpg")
        self.insertTextWithPicture("Sed eget tortor non sapien fringilla porttitor eget vel erat. "
                                   "Vivamus rhoncus erat sed justo euismod, ac sollicitudin odio "
                                   "semper. Duis eget enim non metus aliquet consequat.")

        page_frame_layout = QVBoxLayout()
        page_frame_layout.addWidget(self.text_edit)
        page_frame.setLayout(page_frame_layout)

        layout.addWidget(page_frame)
        self.setLayout(layout)

    def insertTextWithPicture(self, text, image_path=None):
        cursor = self.text_edit.textCursor()
        cursor.insertText(text)

        if image_path:
            self.insertPicture(image_path)

    def insertPicture(self, image_path):
        cursor = self.text_edit.textCursor()
        cursor.insertBlock()

        image_format = QTextImageFormat()
        image_format.setWidth(200)  # Set the width of the image (adjust as needed)
        image_format.setHeight(150)  # Set the height of the image (adjust as needed)
        image_format.setName(image_path)

        cursor.insertImage(image_format)


