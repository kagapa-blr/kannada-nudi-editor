import threading

import speech_recognition as sr
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel


class LanguageSelectionPopup(QDialog):
    def __init__(self):
        super().__init__()
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
        self.selectedLanguage = None

    def selectEnglish(self):
        self.selectedLanguage = 'en-IN'
        self.accept()  # Close the dialog and return a success code

    def selectKannada(self):
        self.selectedLanguage = 'kn-IN'
        self.accept()  # Close the dialog and return a success code


class SpeechToTextThread(threading.Thread):
    def __init__(self, editor, language):
        threading.Thread.__init__(self)
        self.recognizer = sr.Recognizer()
        self.editor = editor
        self.running = True
        self.language = language

    def run(self):
        if self.language is None:
            print("No language selected. Exiting thread.")
            return

        with sr.Microphone() as source:
            while self.running:
                try:
                    print("Listening...")
                    audio = self.recognizer.listen(source, timeout=5)
                    print("Recognizing...")
                    text = self.recognizer.recognize_google(audio, language=self.language)
                    self.editor.insertPlainText(text + " ")
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    print("Could not understand audio")
                    continue
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    continue

    def stop(self):
        self.running = False
