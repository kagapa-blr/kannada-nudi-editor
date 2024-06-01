from PyQt5.QtWidgets import QDialog, QMessageBox


class CommonDialogs(QDialog):
    def __init__(self):
        super().__init__()

    def show_error_popup(self,error_message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText("An error occurred:")
        error_box.setInformativeText(error_message)
        error_box.exec_()

