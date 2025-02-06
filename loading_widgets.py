from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QMovie
import sys


class LoadingClass(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loading_type = None

    def initUI(self):
        self.setWindowFlag(Qt.FramelessWindowHint)  # Optional: Remove the window border
        self.setAttribute(Qt.WA_TranslucentBackground)  # Set transparent background
        self.setGeometry(100, 100, 500, 400)  # Default geometry

    def task_loading(self):
        """Show the simple spinner loading screen."""
        self.setWindowTitle("Loading...")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Circular spinner using QMovie (animated GIF)
        self.spinner_label = QLabel(self)
        self.movie = QMovie("resources/images/nudi-spinner.gif")  # Path to your rotating spinner GIF
        self.spinner_label.setMovie(self.movie)
        self.movie.start()

        # Kannada text label
        label = QLabel("ದಯವಿಟ್ಟು ನಿರೀಕ್ಷಿಸಿ...")
        label.setFont(QFont("Arial", 14, QFont.Bold))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.spinner_label, alignment=Qt.AlignCenter)
        layout.addWidget(label, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.show()

    def start_app_loading(self):
        """Show the full-screen loading screen with footer and gradient background."""
        self.setWindowTitle("Loading")
        self.setStyleSheet(
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 red, stop:1 yellow);")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Spinner using GIF
        self.spinner = QLabel(self)
        self.spinner.setAlignment(Qt.AlignCenter)
        movie = QMovie("resources/images/nudi-spinner.gif")
        self.spinner.setMovie(movie)
        movie.start()

        # Loading label in Kannada
        self.label = QLabel("ದಯವಿಟ್ಟು ನಿರೀಕ್ಷಿಸಿ...")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")

        # Footer messages
        self.footer1 = QLabel("ಕನ್ನಡ ನುಡಿ - ತಂತ್ರಾಂಶದ ವಿನ್ಯಾಸ ಮತ್ತು ಅಭಿವೃದ್ಧಿ - ಕನ್ನಡ ಗಣಕ ಪರಿಷತ್ - ಬೆಂಗಳೂರು")
        self.footer1.setAlignment(Qt.AlignCenter)
        self.footer1.setWordWrap(True)
        self.footer1.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

        self.footer2 = QLabel("Copyright © 2025 ಕಗಪ. ಎಲ್ಲಾ ಹಕ್ಕುಗಳನ್ನು ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ")
        self.footer2.setAlignment(Qt.AlignCenter)
        self.footer2.setWordWrap(True)
        self.footer2.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

        layout.addWidget(self.spinner)
        layout.addWidget(self.label)
        layout.addSpacing(20)
        layout.addWidget(self.footer1)
        layout.addWidget(self.footer2)

        self.setLayout(layout)
        self.show()

    def start_loading(self, loading_type):
        """Start the loading screen based on the passed loading_type."""
        self.loading_type = loading_type

        if loading_type == 'task':
            self.task_loading()
        elif loading_type == 'app':
            self.start_app_loading()

    def stop_loading(self, delay_seconds=0):
        """Stop the loading screen after a specified delay (in seconds)."""
        if self.loading_type is not None:
            # Delay before stopping the loading screen
            QTimer.singleShot(delay_seconds * 1000, self.close)
            self.loading_type = None
        else:
            print("No loading screen is currently active.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loader = LoadingClass()

    # Start task loading screen
    loader.start_loading('task')

    # Simulate a delay of 3 seconds before stopping the loading screen
    #loader.stop_loading(3)

    sys.exit(app.exec_())
