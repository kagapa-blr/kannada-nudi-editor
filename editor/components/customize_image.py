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


from PyQt5.QtCore import Qt, QSize, QRect, QRectF, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QIcon, QFont
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QSlider, QToolBar, QAction, QMessageBox, QLineEdit
)

from PyQt5.QtCore import Qt, QSize, QRect, QRectF
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QIcon, QFont, QColor
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QSlider, QToolBar, QAction, QMessageBox, QLineEdit, QColorDialog
)
class ImageEditDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.original_image = QImage(image_path)
        self.modified_image = self.original_image.copy()
        self.current_image = self.modified_image.copy()
        self.history = [self.current_image]
        self.history_index = 0
        self.brush_color = Qt.black
        self.brush_size = 5
        self.initUI()

        # Variables for drawing shapes
        self.drawing_shape = False
        self.shape_start = None
        self.current_pos = QPoint(0, 0)  # Initialize current_pos

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

        self.brush_color_button = QPushButton("Brush Color", self)
        self.brush_color_button.clicked.connect(self.selectBrushColor)
        controls_layout.addWidget(self.brush_color_button)

        self.brush_size_spinbox = QSpinBox(self)
        self.brush_size_spinbox.setRange(1, 50)
        self.brush_size_spinbox.setValue(5)
        self.brush_size_spinbox.valueChanged.connect(self.setBrushSize)
        controls_layout.addWidget(self.brush_size_spinbox)

        brush_button = QPushButton("Brush", self)
        brush_button.clicked.connect(self.useBrushTool)
        controls_layout.addWidget(brush_button)

        rectangle_button = QPushButton("Rectangle", self)
        rectangle_button.clicked.connect(self.drawRect)
        controls_layout.addWidget(rectangle_button)

        circle_button = QPushButton("Circle", self)
        circle_button.clicked.connect(self.drawCircle)
        controls_layout.addWidget(circle_button)

        fill_button = QPushButton("Fill", self)
        fill_button.clicked.connect(self.fillColor)
        controls_layout.addWidget(fill_button)

        layout.addLayout(controls_layout)

        # Insert button
        insert_button = QPushButton("Insert Image", self)
        insert_button.clicked.connect(self.accept)
        layout.addWidget(insert_button)

        # Set layout
        self.setLayout(layout)
        self.setWindowTitle("Image Editor")

    def selectBrushColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.brush_color = color

    def setBrushSize(self, size):
        self.brush_size = size

    def useBrushTool(self):
        self.drawing_shape = False

    def drawRect(self):
        self.drawing_shape = True
        self.shape_type = "Rectangle"

    def drawCircle(self):
        self.drawing_shape = True
        self.shape_type = "Circle"

    def fillColor(self):
        pass  # Implement fill tool functionality here

    def mousePressEventHandler(self, event):
        if event.button() == Qt.LeftButton:
            if self.drawing_shape:
                self.shape_start = event.pos()
            else:
                self.drawBrush(event.pos())

    def mouseMoveEventHandler(self, event):
        if self.drawing_shape and self.shape_start is not None:
            self.current_pos = event.pos()  # Update current_pos
            self.updatePreview()

    def mouseReleaseEventHandler(self, event):
        if event.button() == Qt.LeftButton:
            if self.drawing_shape and self.shape_start is not None:
                self.drawShape(event.pos())
            else:
                self.addToHistory(self.current_image)

            self.updatePreview()

    def drawBrush(self, pos):
        painter = QPainter(self.current_image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawPoint(pos)
        self.image_label.setPixmap(
            QPixmap.fromImage(self.current_image)
            .scaled(QSize(400, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def drawShape(self, end_pos):
        painter = QPainter(self.current_image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine))
        if self.shape_type == "Rectangle":
            painter.drawRect(QRect(self.shape_start, end_pos))
        elif self.shape_type == "Circle":
            radius = max(abs(self.shape_start.x() - end_pos.x()), abs(self.shape_start.y() - end_pos.y()))
            center = self.shape_start + QPoint(radius, radius)
            painter.drawEllipse(center, radius, radius)
        painter.end()

    def updatePreview(self):
        temp_image = self.current_image.copy()  # Start with a copy of the current image
        painter = QPainter(temp_image)
        if self.drawing_shape and self.shape_start is not None:
            if self.shape_type == "Rectangle":
                painter.drawRect(QRect(self.shape_start, self.current_pos))
            elif self.shape_type == "Circle":
                radius = max(abs(self.shape_start.x() - self.current_pos.x()), abs(self.shape_start.y() - self.current_pos.y()))
                center = self.shape_start + QPoint(radius, radius)
                painter.drawEllipse(center, radius, radius)
        painter.end()
        self.image_label.setPixmap(
            QPixmap.fromImage(temp_image)
            .scaled(QSize(400, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def addToHistory(self, image):
        # Remove future history when new action is performed after undo
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]

        self.history.append(image.copy())
        self.history_index = len(self.history) - 1

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.current_image = self.history[self.history_index].copy()
            self.updatePreview()

    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_image = self.history[self.history_index].copy()
            self.updatePreview()

    def getModifiedImage(self):
        return self.modified_image

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
