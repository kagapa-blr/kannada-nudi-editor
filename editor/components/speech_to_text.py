import threading

import speech_recognition as sr


class SpeechToTextThread(threading.Thread):
    def __init__(self, editor):
        threading.Thread.__init__(self)
        self.recognizer = sr.Recognizer()
        self.editor = editor
        self.running = True

    def run(self):
        with sr.Microphone() as source:
            while self.running:
                try:
                    print("Listening...")
                    audio = self.recognizer.listen(source, timeout=5)
                    print("Recognizing...")
                    text = self.recognizer.recognize_google(audio, language='kn-IN')
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
