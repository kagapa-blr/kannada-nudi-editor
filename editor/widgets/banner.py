import sys
import os
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QDialog, QGraphicsDropShadowEffect, QApplication, QDesktopWidget


class SplashScreen(QDialog):
    """Professional and modern splash screen with smooth animations."""
    def __init__(self):
        super().__init__()

        # Determine OS and Set Font Path
        if sys.platform.startswith("win"):  # Windows
            font_path = "./resources/static/Nudi_fonts/NudiParijatha.ttf"
        else:  # Linux/macOS
            font_path = "./resources/static/Nudi_fonts/NotoSansKannada-Regular.ttf"

        # Load the Selected Font
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Failed to load font: {font_path}")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Arial"

        # Dialog Properties
        self.setWindowTitle("Welcome to Kannada Nudi Editor")
        self.setFixedSize(900, 500)
        self.setStyleSheet("background-color: white; border-radius: 12px;")
        self.center_window()

        # Drop Shadow Effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)

        # Banner Image
        self.banner = QLabel(self)
        pixmap = QPixmap("./resources/images/logo.jpg").scaled(800, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.banner.setPixmap(pixmap)
        self.banner.setAlignment(Qt.AlignCenter)
        self.banner.setStyleSheet("margin-top: 20px;")

        # Main Message - Kannada "Please wait..."
        self.label = QLabel("ದಯವಿಟ್ಟು ನಿರೀಕ್ಷಿಸಿ...", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont(font_family, 24, QFont.Bold))
        self.label.setStyleSheet("color: #333; margin-top: 10px;")

        # Footer Message - Kannada Nudi Credits
        self.footer_top = QLabel("ಕನ್ನಡ ನುಡಿ - ತಂತ್ರಾಂಶದ ವಿನ್ಯಾಸ ಮತ್ತು ಅಭಿವೃದ್ಧಿ - ಕನ್ನಡ ಗಣಕ ಪರಿಷತ್ - ಬೆಂಗಳೂರು", self)
        self.footer_top.setAlignment(Qt.AlignCenter)
        self.footer_top.setFont(QFont(font_family, 16, QFont.Bold))
        self.footer_top.setStyleSheet("color: #555; margin-top: 20px; padding: 0 30px;")

        # Copyright Message
        self.footer_bottom = QLabel("Copyright © 2025 ಕಗಪ. ಎಲ್ಲಾ ಹಕ್ಕುಗಳನ್ನು ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ", self)
        self.footer_bottom.setAlignment(Qt.AlignCenter)
        self.footer_bottom.setFont(QFont(font_family, 14))
        self.footer_bottom.setStyleSheet("color: #777; margin-bottom: 20px;")

        # Accept Button
        self.accept_button = QPushButton("Accept", self)
        self.accept_button.setFont(QFont("Arial", 18))
        self.accept_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005CBF;
            }
            QPushButton:pressed {
                background-color: #004E9A;
            }
        """)
        self.accept_button.clicked.connect(self.accept)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.banner)
        layout.addWidget(self.label)
        layout.addWidget(self.footer_top)
        layout.addWidget(self.footer_bottom)
        layout.addWidget(self.accept_button, alignment=Qt.AlignCenter)
        layout.setContentsMargins(40, 20, 40, 20)

        self.setLayout(layout)

        # Fade-in Animation
        self.fade_in()

    def fade_in(self):
        """Smooth fade-in effect."""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(600)
        self.animation.setStartValue(QRect(self.x(), self.y() - 50, self.width(), self.height()))
        self.animation.setEndValue(QRect(self.x(), self.y(), self.width(), self.height()))
        self.animation.start()

    def center_window(self):
        """Center the window on the screen."""
        screen_geometry = QDesktopWidget().screenGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())


# Test the SplashScreen (Standalone Mode)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.exec_()
