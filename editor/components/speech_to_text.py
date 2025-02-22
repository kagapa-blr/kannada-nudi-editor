import speech_recognition as sr
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel

from logger import setup_logger

# Initialize logger
logger = setup_logger(logger_name='speech_to_text')


class LanguageSelectionPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.selectedLanguage = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ಕನ್ನಡ ನುಡಿ - ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ')
        self.setWindowIcon(QIcon('resources/images/logo.jpg'))
        layout = QVBoxLayout()

        self.label = QLabel('ದಯವಿಟ್ಟು ಭಾಷಣ ಗುರುತಿಸುವಿಕೆಗಾಗಿ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:', self)
        layout.addWidget(self.label)

        self.kannadaButton = QPushButton('ಕನ್ನಡ', self)
        self.kannadaButton.clicked.connect(self.selectKannada)
        layout.addWidget(self.kannadaButton)

        self.englishButton = QPushButton('English', self)
        self.englishButton.clicked.connect(self.selectEnglish)
        layout.addWidget(self.englishButton)

        self.setLayout(layout)

    def selectEnglish(self):
        self.selectedLanguage = 'en-IN'
        self.accept()

    def selectKannada(self):
        self.selectedLanguage = 'kn-IN'
        self.accept()


class SpeechToTextThread(QThread):
    text_ready = pyqtSignal(str)  # Signal to send text to the UI

    def __init__(self, language):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.language = language
        self.running = True

    def run(self):
        if not self.language:
            logger.error("No language selected. Exiting thread.")
            return

        logger.info(f"Speech-to-Text started for language: {self.language}")

        with sr.Microphone() as source:
            while self.running:
                try:
                    logger.info("Listening for speech...")
                    audio = self.recognizer.listen(source, timeout=5)

                    if not self.running:
                        break  # Exit loop when stopped

                    logger.info("Recognizing speech...")
                    text = self.recognizer.recognize_google(audio, language=self.language)
                    self.text_ready.emit(text + " ")  # Emit text to main thread

                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    logger.warning("Could not understand the audio")
                except sr.RequestError as e:
                    logger.error(f"Speech recognition request failed: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error in Speech-to-Text: {e}")

        logger.info("Speech-to-Text thread stopped.")

    def stop(self):
        """ Gracefully stop the thread. """
        logger.info("Stopping Speech-to-Text...")
        self.running = False
        self.quit()
        self.wait()

