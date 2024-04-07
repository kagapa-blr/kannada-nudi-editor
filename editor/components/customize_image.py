#
#
# class ImageEditDialog(QDialog):
#     def __init__(self, image_path, parent=None):
#         super().__init__(parent)
#         self.original_image = QImage(image_path)
#         self.modified_image = self.original_image.copy()
#         self.initUI()
#
#     def initUI(self):
#         layout = QVBoxLayout(self)
#
#         self.image_label = QLabel(self)
#         self.image_label.setPixmap(QPixmap.fromImage(self.modified_image).scaled(QSize(400, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation))
#         layout.addWidget(self.image_label)
#
#         # Image editing controls
#         controls_layout = QHBoxLayout()
#
#         # Resize controls
#         self.resize_spinbox = QSpinBox(self)
#         self.resize_spinbox.setRange(10, 2000)
#         self.resize_spinbox.setValue(self.original_image.width())
#         controls_layout.addWidget(self.resize_spinbox)
#
#         resize_button = QPushButton("Resize", self)
#         resize_button.clicked.connect(self.resizeImage)
#         controls_layout.addWidget(resize_button)
#
#         # Rotation controls
#         self.rotate_slider = QSlider(Qt.Horizontal, self)
#         self.rotate_slider.setRange(-180, 180)
#         self.rotate_slider.setValue(0)
#         controls_layout.addWidget(self.rotate_slider)
#
#         rotate_button = QPushButton("Rotate", self)
#         rotate_button.clicked.connect(self.rotateImage)
#         controls_layout.addWidget(rotate_button)
#
#         layout.addLayout(controls_layout)
#
#         # Insert button
#         insert_button = QPushButton("Insert Image", self)
#         insert_button.clicked.connect(self.accept)
#         layout.addWidget(insert_button)
#
#         self.setLayout(layout)
#         self.setWindowTitle("Image Editor")
#
#     def resizeImage(self):
#         new_width = self.resize_spinbox.value()
#         scale_factor = new_width / self.original_image.width()
#         self.modified_image = self.original_image.scaledToWidth(new_width)
#         self.image_label.setPixmap(QPixmap.fromImage(self.modified_image).scaled(QSize(400, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation))
#
#     def rotateImage(self):
#         angle = self.rotate_slider.value()
#         transform = QTransform().rotate(angle)
#         self.modified_image = self.original_image.transformed(transform)
#         self.image_label.setPixmap(QPixmap.fromImage(self.modified_image).scaled(QSize(400, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation))
#
#     def getModifiedImage(self):
#         return self.modified_image


from PyQt5.QtCore import Qt, QSize, QRect, QRectF
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QIcon, QFont
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QSlider, QToolBar, QAction, QMessageBox, QLineEdit
)


class ImageEditDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.original_image = QImage(image_path)
        self.modified_image = self.original_image.copy()
        self.current_image = self.modified_image.copy()
        self.history = [self.current_image]
        self.history_index = 0
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.image_label = QLabel(self)
        self.image_label.setPixmap(
            QPixmap.fromImage(self.current_image)
            .scaled(QSize(400, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.image_label.mousePressEvent = self.mousePressEventHandler
        self.image_label.mouseMoveEvent = self.mouseMoveEventHandler
        self.image_label.mouseReleaseEvent = self.mouseReleaseEventHandler
        layout.addWidget(self.image_label)

        # Image editing controls
        controls_layout = QHBoxLayout()

        self.resize_spinbox = QSpinBox(self)
        self.resize_spinbox.setRange(10, 2000)
        self.resize_spinbox.setValue(self.original_image.width())
        controls_layout.addWidget(self.resize_spinbox)

        resize_button = QPushButton("Resize", self)
        resize_button.clicked.connect(self.resizeImage)
        controls_layout.addWidget(resize_button)

        self.rotate_slider = QSlider(Qt.Horizontal, self)
        self.rotate_slider.setRange(-180, 180)
        self.rotate_slider.setValue(0)
        controls_layout.addWidget(self.rotate_slider)

        rotate_button = QPushButton("Rotate", self)
        rotate_button.clicked.connect(self.rotateImage)
        controls_layout.addWidget(rotate_button)

        crop_button = QPushButton("Crop", self)
        crop_button.clicked.connect(self.cropImage)
        controls_layout.addWidget(crop_button)

        layout.addLayout(controls_layout)

        # Insert button
        insert_button = QPushButton("Insert Image", self)
        insert_button.clicked.connect(self.accept)
        layout.addWidget(insert_button)

        # Text input for inserting text
        self.text_input = QLineEdit(self)
        layout.addWidget(self.text_input)

        # Button to insert text
        insert_text_button = QPushButton("Insert Text", self)
        insert_text_button.clicked.connect(self.insertTextOnImage)
        layout.addWidget(insert_text_button)

        # Toolbar setup
        toolbar = QToolBar()
        layout.addWidget(toolbar)

        undo_action = QAction(QIcon('resources/images/undo.png'), 'Undo', self)
        undo_action.triggered.connect(self.undo)
        toolbar.addAction(undo_action)

        redo_action = QAction(QIcon('resources/images/redo.png'), 'Redo', self)
        redo_action.triggered.connect(self.redo)
        toolbar.addAction(redo_action)

        self.setLayout(layout)
        self.setWindowTitle("Image Editor")

        # Variables for cropping
        self.drag_start = None
        self.crop_rect = None

    def insertTextOnImage(self):
        text = self.text_input.text()
        if text:
            temp_image = self.current_image.copy()
            painter = QPainter(temp_image)
            painter.setPen(QPen(Qt.black))  # Set text color
            painter.setFont(QFont("Arial", 20))  # Set font and size
            painter.drawText(QRectF(50, 50, temp_image.width(), temp_image.height()), Qt.AlignLeft | Qt.AlignTop, text)  # Draw text at position (50, 50)
            painter.end()
            self.addToHistory(temp_image)
            self.current_image = temp_image
            self.modified_image = temp_image  # Update modified_image to reflect the most recent state including text
            self.updatePreview()

    def resizeImage(self):
        new_width = self.resize_spinbox.value()
        new_image = self.original_image.scaledToWidth(new_width)
        self.addToHistory(new_image)
        self.current_image = new_image
        self.updatePreview()

    def rotateImage(self):
        angle = self.rotate_slider.value()
        transform = QTransform().rotate(angle)
        new_image = self.original_image.transformed(transform)
        self.addToHistory(new_image)
        self.current_image = new_image
        self.updatePreview()

    def cropImage(self):
        if self.crop_rect is None:
            QMessageBox.warning(self, "No Selection", "Please select an image area to crop.")
            return

        new_image = self.current_image.copy(self.crop_rect)
        self.addToHistory(new_image)
        self.current_image = new_image
        self.crop_rect = None
        self.updatePreview()

    def mousePressEventHandler(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start = event.pos()

    def mouseMoveEventHandler(self, event):
        if self.drag_start is not None:
            end_pos = event.pos()
            self.crop_rect = QRect(self.drag_start, end_pos).normalized()
            self.updatePreview()

    def mouseReleaseEventHandler(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start = None

    def addToHistory(self, image):
        # Remove future history when new action is performed after undo
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]

        self.history.append(image)
        self.history_index = len(self.history) - 1

    def updatePreview(self):
        temp_image = self.current_image.copy()  # Start with a copy of the current image
        if self.crop_rect is not None:
            painter = QPainter(temp_image)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(self.crop_rect)
            painter.end()

        self.image_label.setPixmap(
            QPixmap.fromImage(temp_image)
            .scaled(QSize(400, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.current_image = self.history[self.history_index]
            self.updatePreview()

    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_image = self.history[self.history_index]
            self.updatePreview()

    def getModifiedImage(self):
        return self.modified_image
