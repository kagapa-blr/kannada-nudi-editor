from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSlider, QHBoxLayout, QMainWindow, QWidget, QVBoxLayout


class ZoomSlider:
    def initZoomSlider(self, parent):
        zoom_label = QLabel("Zoom:", parent)
        self.zoom_slider = QSlider(Qt.Horizontal, parent)
        self.zoom_slider.setRange(10, 300)  # Zoom range from 10% to 300%
        self.zoom_slider.setValue(100)  # Default zoom level at 100%
        self.zoom_slider.setTickInterval(10)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setFixedWidth(150)  # Set a fixed width for the slider
        self.zoom_slider.valueChanged.connect(parent.updateZoom)

        slider_layout = QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        slider_layout.setSpacing(0)  # Remove spacing
        slider_layout.addStretch(1)  # Add stretchable space to push slider to the right
        slider_layout.addWidget(zoom_label)
        slider_layout.addWidget(self.zoom_slider)

        central_layout = parent.centralWidget().layout()
        central_layout.addLayout(slider_layout)
        central_layout.setAlignment(slider_layout, Qt.AlignBottom | Qt.AlignRight)
