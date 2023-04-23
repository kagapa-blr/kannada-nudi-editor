#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: cp1252 -*-
# encoding=utf8
from __future__ import print_function

import locale
import os
import sys
# import proto.stt_pb2_grpc as stt_pb2_grpc
# import proto.stt_pb2 as stt_pb2
from configparser import ConfigParser

# import codecs

PYTHONIOENCODING = "UTF-8"
os_encoding = locale.getpreferredencoding()
from PIL import ImageTk, Image
import queue as Queue
import tkinter
from tkinter import BOTH
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
import tkinter.font
import logging
logging.basicConfig(level=logging.DEBUG, filename='logs/nudi.logs', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

logger.info("first mesg")
print(sys.version_info.major)
logger.info("python version detected by app: %s",sys.version_info.major)

if sys.version_info.major!=3:
    logger.info("you  don't have python 3 version")
else:
    logger.info("you   have python 3 version")
    pass


import sys
import time
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

# Reading from config file
parser = ConfigParser()
parser.read('user.config')

_TIMEOUT_SECONDS = 10
_TIMEOUT_SECONDS_STREAM = 1000

audioQueue = {}
transcription = {}

audioQueue["abcd"] = Queue.Queue()
transcription["abcd"] = ""

var = 0
f = ""
choiceStr = ""
cs = False
wwo = False

tt = True
tf = True
ts = True










def refresh():
    from pywin.framework import window
    window.destroy()
    os.startfile(".\\client_ka.exe")

import pyaudio
absolute_path = os.path.dirname(__file__)
relative_path = "media\icon\microphone.png"
#full_path = 
class RecAUD:

    def __init__(self, chunk=1024, frmat=pyaudio.paInt16, channels=1, rate=16000, py=pyaudio.PyAudio()):
        # Start Tkinter and set Title

        self.main = tkinter.Tk()
        # self.main.call('encoding', 'system', 'utf-8')  # unicode tkinter
        microphone = "media/icon/microphone.png"#os.path.join(absolute_path, relative_path)
        self.rec_img = ImageTk.PhotoImage(Image.open(microphone))
        mic = "media/icon/mic.ico"#os.path.join(absolute_path,"media/icon/mic.ico")
        self.stp_img = ImageTk.PhotoImage(Image.open(microphone))

        self.main.geometry("300x300+210+280")
        # self.main.t = tkinter.Text(self.main)
        self.main.title("wm min/max")  # hide the title bar button
        self.main.resizable(0, 0)
        self.main.iconbitmap('media/icon/mic.ico')
        # self.label = tkinter.Label(self.main, image=self.stp_img, bg='red')
        # self.main.overrideredirect(True) # disable the header button in frame
        self.collections = []
        self.main.lift()
        self.main.title('Voice')

        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        # self.main.attributes("-toolwindow", 1)  # make header close button only
        self.main.wm_attributes('-topmost', 1)
        self.main.wm_attributes('-topmost', 0)
        self.main.wm_attributes("-topmost", True)
        # self.main.attributes("-alpha", 0.9)  #transparent the baground
        self.st = 1  # self.main.attributes("-transparentcolor", "white") #disable movement of frame
        # self.main.wm_attributes("-disabled", True) #disable all activity of the header of window
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                                  frames_per_buffer=self.CHUNK)

        # Set Frames
        self.buttons = tkinter.Frame(self.main, padx=30, pady=10)

        # Pack Frame
        # self.label.pack() #self.buttons.pack(fill=BOTH) #self.buttons.pack()
        self.buttons.pack(fill=BOTH)

        # Text area Text BOX Add Here

        self.tex = tkinter.Text()
        self.tex = ScrolledText(self.main)
        # f.decode('utf-8') self.tex.insert('1.0', f.encode('UTF-8'))
        #self.tex.tk.call('font', 'configure', 'TkDefaultFont', '-size', '28')
        self.tex.config(state=tkinter.NORMAL, font=('Calibri', 16), fg="blue", bg="yellow")
        self.tex.pack(side=tkinter.RIGHT)

        # button

        self.strt_rec = tkinter.Button(self.buttons, width='40', height='60', padx=0, pady=5, image=self.stp_img,
                                       command=lambda: (self.start_record(), self.my_file()))
        self.strt_rec.grid(row=0, column=0, columnspan=1, padx=5, pady=5)

        self.main.call('wm', 'attributes', '.', '-topmost',
                       '1')  # it helps to appear window on top of all active window
        # self._offsetx = 0
        # self._offsety = 0

        # self.label.pack() #use anothe image mentioned above main.label
        tkinter.mainloop()

    def start_record(self):
        self.st = 1
        # self.strt_rec.configure(image=self.rec_img)
        # Creating button to stop
        self.stop_rec = tkinter.Button(self.buttons, width='40', height='60', padx=0, pady=5, image=self.rec_img,
                                       command=lambda: (self.stop(), self.my_file()))
        self.stop_rec.grid(row=0, column=0, columnspan=1, padx=5, pady=5)

        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                             frames_per_buffer=self.CHUNK)
        while self.st == 1:
            data = stream.read(self.CHUNK)
            audioQueue["abcd"].put(data)
            print("* recording")
            self.main.update()
        audioQueue["abcd"].put('EOS')
        print("* done")
        stream.stop_stream()
        stream.close()

    def stop(self):
        self.strt_rec = tkinter.Button(self.buttons, width='40', height='60', padx=0, pady=5, image=self.stp_img,
                                       command=lambda: (self.start_record(), self.my_file()))
        self.strt_rec.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        self.st = 0

        # os.system('start " " output.txt')
        # t.after(5000)
        # self.main.refresh()
        # os.startfile(".\\client_ka.exe")

    def my_file(self):
        # self.tex.DELAY = 100
        time.sleep(1)
        f = open("output.txt", "r+", encoding ='utf8')

        self.tex.insert(tkinter.END, f.read())  # read the text from text file ...

        if f:
            f = open('output.txt', 'w', encoding ='utf8')
            f.close()

        # self.tex.delete("1.0", "end") #delete the text in text area ( box )
        f.close()


guiAUD = RecAUD()

class Find(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.initUI()

    def initUI(self):

        self.lb1 = QLabel("Search for: ", self)
        self.lb1.setStyleSheet("font-size: 15px; ")
        self.lb1.move(10, 10)

        self.te = QTextEdit(self)
        self.te.move(10, 40)
        self.te.resize(250, 25)

        self.src = QPushButton("Find", self)
        self.src.move(270, 40)

        self.lb2 = QLabel("Replace all by: ", self)
        self.lb2.setStyleSheet("font-size: 15px; ")
        self.lb2.move(10, 80)

        self.rp = QTextEdit(self)
        self.rp.move(10, 110)
        self.rp.resize(250, 25)

        self.rpb = QPushButton("Replace", self)
        self.rpb.move(270, 110)

        self.opt1 = QCheckBox("Case sensitive", self)
        self.opt1.move(10, 160)
        self.opt1.stateChanged.connect(self.CS)

        self.opt2 = QCheckBox("Whole words only", self)
        self.opt2.move(10, 190)
        self.opt2.stateChanged.connect(self.WWO)

        self.close = QPushButton("Close", self)
        self.close.move(270, 220)
        self.close.clicked.connect(self.Close)

        self.setGeometry(300, 300, 360, 250)

    def CS(self, state):
        global cs

        if state == QtCore.Qt.Checked:
            cs = True
        else:
            cs = False

    def WWO(self, state):
        global wwo
        print(wwo)

        if state == QtCore.Qt.Checked:
            wwo = True
        else:
            wwo = False

    def Close(self):
        self.hide()


class Date(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.initUI()

    def initUI(self):
        self.form = QComboBox(self)
        self.form.move(10, 10)
        self.form.addItem(time.strftime("%d.%m.%Y"))
        self.form.addItem(time.strftime("%A, %d. %B %Y"))
        self.form.addItem(time.strftime("%d. %B %Y"))
        self.form.addItem(time.strftime("%d %m %Y"))
        self.form.addItem(time.strftime("%X"))
        self.form.addItem(time.strftime("%x"))
        self.form.addItem(time.strftime("%H:%M"))
        self.form.addItem(time.strftime("%A, %d. %B %Y %H:%M"))
        self.form.addItem(time.strftime("%d.%m.%Y %H:%M"))
        self.form.addItem(time.strftime("%d. %B %Y %H:%M"))

        self.form.activated[str].connect(self.handleChoice)

        self.ok = QPushButton("Insert", self)
        self.ok.move(180, 10)

        self.cancel = QPushButton("Cancel", self)
        self.cancel.move(180, 40)
        self.cancel.clicked.connect(self.Cancel)

        self.setGeometry(300, 300, 280, 70)

    def handleChoice(self, choice):
        global choiceStr

        choiceStr = choice

        print(choiceStr)

    def Cancel(self):
        self.close()


class Main(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self, None)
        self.initUI()

    def initUI(self):

        # ------- Toolbar --------------------------------------

        # -- Upper Toolbar --

        newAction = QAction(QIcon("icons/new.png"), "New", self)
        newAction.setShortcut("Ctrl+N")
        newAction.setStatusTip("Create a new document from scratch.")
        newAction.triggered.connect(self.New)

        openAction = QAction(QIcon("icons/open.png"), "Open file", self)
        openAction.setStatusTip("Open existing document")
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.Open)

        saveAction = QAction(QIcon("icons/save.png"), "Save", self)
        saveAction.setStatusTip("Save document")
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.Save)

        previewAction = QAction(QIcon("icons/preview.png"), "Page view", self)
        previewAction.setStatusTip("Preview page before printing")
        previewAction.setShortcut("Ctrl+Shift+P")
        previewAction.triggered.connect(self.PageView)

        findAction = QAction(QIcon("icons/find.png"), "Find", self)
        findAction.setStatusTip("Find words in your document")
        findAction.setShortcut("Ctrl+F")
        findAction.triggered.connect(self.Find)

        cutAction = QAction(QIcon("icons/cut.png"), "Cut to clipboard", self)
        cutAction.setStatusTip("Delete and copy text to clipboard")
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.Cut)

        copyAction = QAction(QIcon("icons/copy.png"), "Copy to clipboard", self)
        copyAction.setStatusTip("Copy text to clipboard")
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.Copy)

        pasteAction = QAction(QIcon("icons/paste.png"), "Paste from clipboard", self)
        pasteAction.setStatusTip("Paste text from clipboard")
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.Paste)

        undoAction = QAction(QIcon("icons/undo.png"), "Undo last action", self)
        undoAction.setStatusTip("Undo last action")
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(self.Undo)

        redoAction = QAction(QIcon("icons/redo.png"), "Redo last undone thing", self)
        redoAction.setStatusTip("Redo last undone thing")
        redoAction.setShortcut("Ctrl+Y")
        redoAction.triggered.connect(self.Redo)

        dtAction = QAction(QIcon("icons/datetime.png"), "Insert current date/time", self)
        dtAction.setStatusTip("Insert current date/time")
        dtAction.setShortcut("Ctrl+D")
        dtAction.triggered.connect(self.DateTime)

        printAction = QAction(QIcon("icons/print.png"), "Print document", self)
        printAction.setStatusTip("Print document")
        printAction.setShortcut("Ctrl+P")
        printAction.triggered.connect(self.Print)

        self.toolbar = self.addToolBar("Options")
        self.toolbar.addAction(newAction)
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(printAction)
        # self.toolbar.addAction(pdfAction)
        self.toolbar.addAction(previewAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(findAction)
        self.toolbar.addAction(cutAction)
        self.toolbar.addAction(copyAction)
        self.toolbar.addAction(pasteAction)
        self.toolbar.addAction(undoAction)
        self.toolbar.addAction(redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(dtAction)
        self.toolbar.addSeparator()

        self.addToolBarBreak()

        # -- Lower Toolbar --

        self.fontFamily = QFontComboBox(self)
        self.fontFamily.currentFontChanged.connect(self.FontFamily)

        fontSize = QComboBox(self)
        fontSize.setEditable(True)
        fontSize.setMinimumContentsLength(3)
        fontSize.activated.connect(self.FontSize)
        flist = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 26, 28, 32, 36, 40, 44, 48,
                 54, 60, 66, 72, 80, 88, 96]

        for i in flist:
            fontSize.addItem(str(i))

        fontColor = QAction(QIcon("icons/color.png"), "Change font color", self)
        fontColor.triggered.connect(self.FontColor)

        boldAction = QAction(QIcon("icons/bold.png"), "Bold", self)
        boldAction.triggered.connect(self.Bold)

        italicAction = QAction(QIcon("icons/italic.png"), "Italic", self)
        italicAction.triggered.connect(self.Italic)

        underlAction = QAction(QIcon("icons/underl.png"), "Underline", self)
        underlAction.triggered.connect(self.Underl)

        alignLeft = QAction(QIcon("icons/alignLeft.png"), "Align left", self)
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QAction(QIcon("icons/alignCenter.png"), "Align center", self)
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QAction(QIcon("icons/alignRight.png"), "Align right", self)
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QAction(QIcon("icons/alignJustify.png"), "Align justify", self)
        alignJustify.triggered.connect(self.alignJustify)

        indentAction = QAction(QIcon("icons/indent.png"), "Indent Area", self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.Indent)

        dedentAction = QAction(QIcon("icons/dedent.png"), "Dedent Area", self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.Dedent)

        backColor = QAction(QIcon("icons/backcolor.png"), "Change background color", self)
        backColor.triggered.connect(self.FontBackColor)

        bulletAction = QAction(QIcon("icons/bullet.png"), "Insert Bullet List", self)
        bulletAction.triggered.connect(self.BulletList)

        numberedAction = QAction(QIcon("icons/number.png"), "Insert Numbered List", self)
        numberedAction.triggered.connect(self.NumberedList)

        space1 = QLabel("  ", self)
        space2 = QLabel(" ", self)
        space3 = QLabel(" ", self)

        self.formatbar = self.addToolBar("Format")
        self.formatbar.addWidget(self.fontFamily)
        self.formatbar.addWidget(space1)
        self.formatbar.addWidget(fontSize)
        self.formatbar.addWidget(space2)

        self.formatbar.addSeparator()

        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)

        self.formatbar.addSeparator()

        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)

        self.formatbar.addSeparator()

        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)

        self.formatbar.addSeparator()

        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)
        self.formatbar.addAction(bulletAction)
        self.formatbar.addAction(numberedAction)

        # ------- Text Edit -----------------------------------

        self.text = QTextEdit(self)
        self.text.setTabStopWidth(12)
        self.setCentralWidget(self.text)

        # ------- Statusbar ------------------------------------

        self.status = self.statusBar()

        self.text.cursorPositionChanged.connect(self.CursorPosition)

        # ---------Window settings --------------------------------

        self.setGeometry(100, 100, 700, 700)
        self.setWindowTitle("Scriber")
        self.setWindowIcon(QIcon("icons/feather.png"))
        self.show()

        # ------- Menubar --------------------------------------

        menubar = self.menuBar()
        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        file.addAction(newAction)
        file.addAction(openAction)
        file.addAction(saveAction)
        file.addAction(printAction)
        file.addAction(previewAction)

        edit.addAction(undoAction)
        edit.addAction(redoAction)
        edit.addAction(cutAction)
        edit.addAction(copyAction)
        edit.addAction(findAction)
        edit.addAction(dtAction)

        toggleTool = QAction("Toggle Toolbar", self, checkable=True)
        toggleTool.triggered.connect(self.handleToggleTool)

        toggleFormat = QAction("Toggle Formatbar", self, checkable=True)
        toggleFormat.triggered.connect(self.handleToggleFormat)

        toggleStatus = QAction("Toggle Statusbar", self, checkable=True)
        toggleStatus.triggered.connect(self.handleToggleStatus)

        view.addAction(toggleTool)
        view.addAction(toggleFormat)
        view.addAction(toggleStatus)

    def handleToggleTool(self):
        global tt

        if tt == True:
            self.toolbar.hide()
            tt = False
        else:
            self.toolbar.show()
            tt = True

    def handleToggleFormat(self):
        global tf

        if tf == True:
            self.formatbar.hide()
            tf = False
        else:
            self.formatbar.show()
            tf = True

    def handleToggleStatus(self):
        global ts

        if ts == True:
            self.status.hide()
            ts = False
        else:
            self.status.show()
            ts = True

    # -------- Toolbar slots -----------------------------------

    def New(self):
        self.text.clear()

    def Open(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        f = open(filename, 'r')
        filedata = f.read()
        self.text.setText(filedata)
        f.close()

    def Save(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File')
        f = open(filename, 'w')
        filedata = self.text.toPlainText()
        f.write(filedata)
        f.close()

    def PageView(self):
        preview = QPrintPreviewDialog()
        preview.paintRequested.connect(self.PaintPageView)
        preview.exec_()

    def Print(self):
        from PyQt5.QtPrintSupport import QPrintDialog
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def PDF(self):
        printer = QPrinter()
        printer.setOutputFormat(printer.NativeFormat)

        dialog = QPrintDialog(printer)
        dialog.setOption(dialog.PrintToFile)
        if dialog.exec_() == QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def PaintPageView(self, printer):
        self.text.print_(printer)

    def Find(self):
        global f

        find = Find(self)
        find.show()

        def handleFind():

            f = find.te.toPlainText()
            print(f)

            if cs == True and wwo == False:
                flag = QTextDocument.FindBackward and QTextDocument.FindCaseSensitively

            elif cs == False and wwo == False:
                flag = QTextDocument.FindBackward

            elif cs == False and wwo == True:
                flag = QTextDocument.FindBackward and QTextDocument.FindWholeWords

            elif cs == True and wwo == True:
                flag = QTextDocument.FindBackward and QTextDocument.FindCaseSensitively and QTextDocument.FindWholeWords

            self.text.find(f, flag)

        def handleReplace():
            f = find.te.toPlainText()
            r = find.rp.toPlainText()

            text = self.text.toPlainText()

            newText = text.replace(f, r)

            self.text.clear()
            self.text.append(newText)

        find.src.clicked.connect(handleFind)
        find.rpb.clicked.connect(handleReplace)

    def Undo(self):
        self.text.undo()

    def Redo(self):
        self.text.redo()

    def Cut(self):
        self.text.cut()

    def Copy(self):
        self.text.copy()

    def Paste(self):
        self.text.paste()

    def DateTime(self):

        date = Date(self)
        date.show()

        date.ok.clicked.connect(self.insertDate)

    def insertDate(self):
        global choiceStr
        print(choiceStr)
        self.text.append(choiceStr)

    def CursorPosition(self):
        line = self.text.textCursor().blockNumber()
        col = self.text.textCursor().columnNumber()
        linecol = ("Line: " + str(line) + " | " + "Column: " + str(col))
        self.status.showMessage(linecol)

    def FontFamily(self, font):
        font = QFont(self.fontFamily.currentFont())
        self.text.setCurrentFont(font)

    def FontSize(self, fsize):
        size = (int(fsize))
        self.text.setFontPointSize(size)

    def FontColor(self):
        c = QColorDialog.getColor()

        self.text.setTextColor(c)

    def FontBackColor(self):
        c = QColorDialog.getColor()

        self.text.setTextBackgroundColor(c)

    def Bold(self):
        w = self.text.fontWeight()
        if w == 50:
            self.text.setFontWeight(QFont.Bold)
        elif w == 75:
            self.text.setFontWeight(QFont.Normal)

    def Italic(self):
        i = self.text.fontItalic()

        if i == False:
            self.text.setFontItalic(True)
        elif i == True:
            self.text.setFontItalic(False)

    def Underl(self):
        ul = self.text.fontUnderline()

        if ul == False:
            self.text.setFontUnderline(True)
        elif ul == True:
            self.text.setFontUnderline(False)

    def lThrough(self):
        lt = QFont.style()

        print(lt)

    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)

    def Indent(self):
        tab = "\t"
        cursor = self.text.textCursor()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(end)
        cursor.movePosition(cursor.EndOfLine)
        end = cursor.position()

        cursor.setPosition(start)
        cursor.movePosition(cursor.StartOfLine)
        start = cursor.position()

        while cursor.position() < end:
            global var

            print(cursor.position(), end)

            cursor.movePosition(cursor.StartOfLine)
            cursor.insertText(tab)
            cursor.movePosition(cursor.Down)
            end += len(tab)

            '''if cursor.position() == end:
                var +=1

            if var == 2:
                break'''

    def Dedent(self):
        tab = "\t"
        cursor = self.text.textCursor()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(end)
        cursor.movePosition(cursor.EndOfLine)
        end = cursor.position()

        cursor.setPosition(start)
        cursor.movePosition(cursor.StartOfLine)
        start = cursor.position()

        while cursor.position() < end:
            global var

            cursor.movePosition(cursor.StartOfLine)
            cursor.deleteChar()
            cursor.movePosition(cursor.EndOfLine)
            cursor.movePosition(cursor.Down)
            end -= len(tab)

            '''if cursor.position() == end:
                var +=1

            if var == 2:
                break'''

    def BulletList(self):
        print("bullet connects!")
        self.text.insertHtml("<ul><li> ...</li></ul>")

    def NumberedList(self):
        print("numbered connects!")
        self.text.insertHtml("<ol><li> ...</li></ol>")


def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()