import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMenuBar, QMenu, QStatusBar
from PyQt5.QtGui import QIcon, QTextCursor, QTextCharFormat
from PyQt5.QtCore import Qt

class TextEditor(QMainWindow):
    def __init(self):
        super().__init()

        self.initUI()

    def initUI(self):
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Ready')

        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        new_action = QAction(QIcon(os.path.join('images', 'new.png')), 'New', self)
        new_action.triggered.connect(self.newFile)
        file_menu.addAction(new_action)

        open_action = QAction(QIcon(os.path.join('images', 'open.png')), 'Open', self)
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon(os.path.join('images', 'save.png')), 'Save', self)
        save_action.triggered.connect(self.saveFile)
        file_menu.addAction(save_action)

        # Edit menu
        edit_menu = menubar.addMenu('Edit')

        cut_action = QAction(QIcon(os.path.join('images', 'cut.png')), 'Cut', self)
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('images', 'copy.png')), 'Copy', self)
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('images', 'paste.png')), 'Paste', self)
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

        undo_action = QAction(QIcon(os.path.join('images', 'undo.png')), 'Undo', self)
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('images', 'redo.png')), 'Redo', self)
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Text Editor')
        self.show()

    def newFile(self):
        self.text_edit.clear()

    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*);;Text Files (*.txt);', options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_edit.setPlainText(content)
            self.statusBar.showMessage(f'Opened: {file_name}')

    def saveFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;All Files (*)', options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                content = self.text_edit.toPlainText()
                file.write(content)
            self.statusBar.showMessage(f'Saved as: {file_name}')

def main():
    app = QApplication(sys.argv)
    editor = TextEditor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
