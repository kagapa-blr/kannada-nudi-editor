from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QDialog, QGraphicsDropShadowEffect, QApplication, QDesktopWidget
import sys


class SplashScreen(QDialog):
    """Professional and modern splash screen with smooth animations."""
    def __init__(self):
        super().__init__()

        # Dialog Properties (Increased Width)
        self.setWindowTitle("Welcome to Kannada Nudi Editor")
        self.setFixedSize(900, 500)  # Wider Window for Better Text Visibility
        self.setStyleSheet("background-color: white; border-radius: 12px;")  # Rounded corners
        self.center_window()  # Center the Window on Screen

        # Drop Shadow Effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)

        # Banner Image (Adjusted Width)
        self.banner = QLabel(self)
        pixmap = QPixmap("./resources/images/logo.jpg").scaled(800, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.banner.setPixmap(pixmap)
        self.banner.setAlignment(Qt.AlignCenter)
        self.banner.setStyleSheet("margin-top: 20px;")

        # Main Message - Kannada "Please wait..."
        self.label = QLabel("ದಯವಿಟ್ಟು ನಿರೀಕ್ಷಿಸಿ...", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 24, QFont.Bold))
        self.label.setStyleSheet("color: #333; margin-top: 10px;")

        # Footer Message - Kannada Nudi Credits
        self.footer_top = QLabel("ಕನ್ನಡ ನುಡಿ - ತಂತ್ರಾಂಶದ ವಿನ್ಯಾಸ ಮತ್ತು ಅಭಿವೃದ್ಧಿ - ಕನ್ನಡ ಗಣಕ ಪರಿಷತ್ - ಬೆಂಗಳೂರು", self)
        self.footer_top.setAlignment(Qt.AlignCenter)
        self.footer_top.setFont(QFont("Arial", 16, QFont.Bold))
        self.footer_top.setStyleSheet("color: #555; margin-top: 20px; padding: 0 30px;")  # Added padding for better alignment

        # Copyright Message
        self.footer_bottom = QLabel("Copyright © 2025 ಕಗಪ. ಎಲ್ಲಾ ಹಕ್ಕುಗಳನ್ನು ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ", self)
        self.footer_bottom.setAlignment(Qt.AlignCenter)
        self.footer_bottom.setFont(QFont("Arial", 14))
        self.footer_bottom.setStyleSheet("color: #777; margin-bottom: 20px;")

        # Accept Button with Modern Style
        self.accept_button = QPushButton("Accept", self)
        self.accept_button.setFont(QFont("Arial", 18))  # Slightly Larger Button
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
        layout.setContentsMargins(40, 20, 40, 20)  # More spacious margins

        self.setLayout(layout)

        # Fade-in Animation
        self.fade_in()

    def fade_in(self):
        """Smooth fade-in effect for better UI experience."""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(600)  # 600ms
        self.animation.setStartValue(QRect(self.x(), self.y() - 50, self.width(), self.height()))
        self.animation.setEndValue(QRect(self.x(), self.y(), self.width(), self.height()))
        self.animation.start()

    def center_window(self):
        """Center the window on the screen."""
        screen_geometry = QDesktopWidget().screenGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())


# Test the SplashScreen (Only for Standalone Testing)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.exec_()
