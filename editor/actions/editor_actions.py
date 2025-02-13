import os
import sys

from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtWidgets import QAction, QFontComboBox, QComboBox


class EditorActions:
    def __init__(self, editor):
        self.editor = editor
    def createActions(self):
        self.newAction = QAction(QIcon('resources/images/new-file.png'), 'New', self.editor)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setStatusTip('Create a new file')
        self.newAction.triggered.connect(self.editor.new)

        self.openAction = QAction(QIcon('resources/images/open-file.png'), 'Open', self.editor)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open an existing file')
        self.openAction.triggered.connect(self.editor.openFile)

        self.openAsciiAction = QAction(QIcon('resources/images/ascii-file-icon.png'), 'Open ASCII file', self.editor)
        self.openAsciiAction.setStatusTip('Open ASCII file')
        self.openAsciiAction.triggered.connect(self.editor.openAsciiFile)

        self.saveAction = QAction(QIcon('resources/images/stock_save.png'), 'Save', self.editor)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save the current file')
        self.saveAction.triggered.connect(self.editor.saveFile)

        self.saveAsAction = QAction(QIcon('resources/images/stock_save.png'), 'Save As', self.editor)
        self.saveAsAction.setStatusTip('SaveAs')
        self.saveAsAction.triggered.connect(self.editor.saveAsFile)

        self.undoAction = QAction(QIcon('resources/images/undo.png'), 'Undo', self.editor)
        self.undoAction.setShortcut('Ctrl+Z')
        self.undoAction.setStatusTip('Undo the last action')
        self.undoAction.triggered.connect(self.editor.undo)

        self.redoAction = QAction(QIcon('resources/images/redo.png'), 'Redo', self.editor)
        self.redoAction.setShortcut('Ctrl+Y')
        self.redoAction.setStatusTip('Redo the last undone action')
        self.redoAction.triggered.connect(self.editor.redo)

        self.printAction = QAction(QIcon('resources/images/print.png'), 'Print', self.editor)
        self.printAction.setShortcut('Ctrl+P')
        self.printAction.setStatusTip('Print the current file')
        self.printAction.triggered.connect(self.editor.printHandler)

        self.zoomInAction = QAction(QIcon('resources/images/zoom-in.png'), 'Zoom In', self.editor)
        self.zoomInAction.setShortcut('Ctrl++')
        self.zoomInAction.setStatusTip('Zoom in')
        self.zoomInAction.triggered.connect(self.editor.zoomIn)

        self.zoomOutAction = QAction(QIcon('resources/images/zoom-out.png'), 'Zoom Out', self.editor)
        self.zoomOutAction.setShortcut('Ctrl+-')
        self.zoomOutAction.setStatusTip('Zoom out')
        self.zoomOutAction.triggered.connect(self.editor.zoomOut)

        self.pageLayoutAction = QAction(QIcon('resources/images/page-layout.png'), 'Page Layout', self.editor)
        self.pageLayoutAction.setStatusTip('Set page layout and size')
        self.pageLayoutAction.triggered.connect(self.editor.page_layout_size)

        self.insertTableAction = QAction(QIcon('resources/images/insert-table.png'), 'Insert Table', self.editor)
        self.insertTableAction.setStatusTip('Insert a table into the document')
        self.insertTableAction.triggered.connect(self.editor.insertTable)

        self.findAction = QAction(QIcon("resources/images/find.png"), "Find and replace", self.editor)
        self.findAction.setStatusTip("Find and replace words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(self.editor.find_replace)

        self.imageAction = QAction(QIcon("resources/images/add-image.png"), "Insert image", self.editor)
        self.imageAction.setStatusTip("Insert image")
        self.imageAction.setShortcut("Ctrl+Shift+I")
        self.imageAction.triggered.connect(self.editor.choose_image)

        self.bulletAction = QAction(QIcon("resources/images/bullet-list.png"), "Insert bullet List", self.editor)
        self.bulletAction.setStatusTip("Insert bullet list")
        self.bulletAction.setShortcut("Ctrl+Shift+B")
        self.bulletAction.triggered.connect(self.editor.bulletList)

        self.numberedAction = QAction(QIcon("resources/images/number-list.png"), "Insert numbered List",
                                      self.editor)
        self.numberedAction.setStatusTip("Insert numbered list")
        self.numberedAction.setShortcut("Ctrl+Shift+L")
        self.numberedAction.triggered.connect(self.editor.numberList)

        self.sort_by_action = QAction(QIcon("resources/images/sortBy.png"), "Sort By",
                                      self.editor)
        self.sort_by_action.setStatusTip("sort by action")
        # self.sort_by_action.setShortcut("Ctrl+Shift+L")
        self.sort_by_action.triggered.connect(self.editor.sortByAction)

        self.speech_to_text = QAction(QIcon('resources/images/mic-speecch-to-text.png'), 'speech to Text', self.editor)
        self.speech_to_text.setStatusTip("speech to text")
        self.speech_to_text.setCheckable(True)
        self.speech_to_text.triggered.connect(self.editor.toggle_speech_to_text)

        self.ascii_to_unicode = QAction(QIcon('resources/images/convert.png'), 'ASCII to Unicode vs converter', self.editor)
        self.ascii_to_unicode.setStatusTip("ASCII to Unicode vs converter")
        self.ascii_to_unicode.setCheckable(True)
        self.ascii_to_unicode.triggered.connect(self.editor.ascii_to_unicode_converter)

        self.excel_csv = QAction(QIcon('resources/images/excel_csv.png'), 'Excel and CSV file operations', self.editor)
        self.excel_csv.setStatusTip("Excel File Handling")
        self.excel_csv.setCheckable(True)
        self.excel_csv.triggered.connect(self.editor.excel_csv_file)

        self.refresh_action = QAction(QIcon('resources/images/refresh.png'), 'Refresh and spellcheck', self.editor)
        self.refresh_action.setStatusTip("spellcheck")
        self.refresh_action.triggered.connect(self.editor.refresh_recheck)

        ####------format bar stated ----------------------------------------------------------

        self.fontColor = QAction(QIcon("resources/images/font-color.png"), "Change font color", self.editor)
        self.fontColor.setStatusTip("change font color")
        self.fontColor.triggered.connect(self.editor.fontColorChanged)

        self.boldAction = QAction(QIcon('resources/images/bold.png'), 'Bold', self.editor)
        self.boldAction.setShortcut('Ctrl+B')
        self.boldAction.setStatusTip('Make selected text bold')
        self.boldAction.triggered.connect(self.editor.toggleBold)

        self.italicAction = QAction(QIcon('resources/images/italic.png'), 'Italic', self.editor)
        self.italicAction.setShortcut('Ctrl+I')
        self.italicAction.setStatusTip('Make selected text italic')
        self.italicAction.triggered.connect(self.editor.toggleItalic)

        self.underlineAction = QAction(QIcon('resources/images/underline.png'), 'Underline', self.editor)
        self.underlineAction.setShortcut('Ctrl+U')
        self.underlineAction.setStatusTip('Underline selected text')
        self.underlineAction.triggered.connect(self.editor.toggleUnderline)

        self.strikeAction = QAction(QIcon("resources/images/strike.png"), "Strike-out", self.editor)
        self.underlineAction.setStatusTip('Strike-outt')
        self.strikeAction.triggered.connect(self.editor.strike)

        self.superAction = QAction(QIcon("resources/images/superscript.png"), "Superscript", self.editor)
        self.superAction.triggered.connect(self.editor.superScript)

        self.subAction = QAction(QIcon("resources/images/subscript.png"), "Subscript", self.editor)
        self.subAction.triggered.connect(self.editor.subScript)

        self.alignLeftAction = QAction(QIcon("resources/images/align-left.png"), "Align left", self.editor)
        self.alignLeftAction.triggered.connect(self.editor.alignLeft)

        self.alignCenterAction = QAction(QIcon("resources/images/align-center.png"), "Align center", self.editor)
        self.alignCenterAction.triggered.connect(self.editor.alignCenter)

        self.alignRightAction = QAction(QIcon("resources/images/align-right.png"), "Align right", self.editor)
        self.alignRightAction.triggered.connect(self.editor.alignRight)

        self.alignJustifyAction = QAction(QIcon("resources/images/align-justify.png"), "Align justify", self.editor)
        self.alignJustifyAction.triggered.connect(self.editor.alignJustify)

        self.indentAction = QAction(QIcon("resources/images/indent.png"), "Indent Area", self.editor)
        self.indentAction.setShortcut("Ctrl+Tab")
        self.indentAction.triggered.connect(self.editor.indent)

        self.dedentAction = QAction(QIcon("resources/images/dedent.png"), "Dedent Area", self.editor)
        self.dedentAction.setShortcut("Shift+Tab")
        self.dedentAction.triggered.connect(self.editor.dedent)

        self.fontbackColor = QAction(QIcon("resources/images/highlight.png"), "Change background color", self.editor)
        self.fontbackColor.triggered.connect(self.editor.highlight)

        self.line_para_spacing = QAction(QIcon("resources/images/line-paragraph-spacing.png"),
                                         "line and Paragraph spacing", self.editor)
        self.line_para_spacing.setStatusTip("line and paragraph spacing.")
        self.line_para_spacing.triggered.connect(self.editor.setSpacing)

        ##### ------ format bar ended----------------------------------------------------------------

    def createMenus(self):
        menubar = self.editor.menuBar()

        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.printAction)

        editMenu = menubar.addMenu('Edit')
        editMenu.addAction(self.boldAction)
        editMenu.addAction(self.italicAction)
        editMenu.addAction(self.underlineAction)

        viewMenu = menubar.addMenu('View')
        viewMenu.addAction(self.zoomInAction)
        viewMenu.addAction(self.zoomOutAction)

    def createToolbars(self):
        self.toolbar = self.editor.addToolBar('Main Toolbar')
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.openAsciiAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.pageLayoutAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.insertTableAction)
        self.toolbar.addAction(self.findAction)
        self.toolbar.addAction(self.imageAction)
        self.toolbar.addAction(self.bulletAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.numberedAction)
        self.toolbar.addAction(self.sort_by_action)
        self.toolbar.addAction(self.speech_to_text)
        self.toolbar.addAction(self.ascii_to_unicode)
        self.toolbar.addAction(self.excel_csv)
        self.toolbar.addSeparator()
        # self.toolbar.addAction(self.wordCountAction)
        self.toolbar.addAction(self.refresh_action)
        self.editor.addToolBarBreak()  # Add this line to create a break between toolbars
        #self.createFormatbar()  # Add this line to create the format bar below the main toolbar

    def createFormatbar(self):
        """Creates a formatting toolbar with font selection and styling options."""
        self.formatbar = self.editor.addToolBar('Format Toolbar')
        self.formatbar.addSeparator()

        # Font ComboBox
        self.fontComboBox = QFontComboBox(self.editor)
        self.formatbar.addWidget(self.fontComboBox)

        # OS-Specific Default Font Selection
        default_font = "NudiParijatha" if sys.platform.startswith("win") else "Noto Sans Kannada"

        # Load all TTF fonts from the directory
        font_dir = "./resources/static/Nudi_fonts"

        if os.path.exists(font_dir):
            for file in os.listdir(font_dir):
                if file.lower().endswith(".ttf"):
                    font_path = os.path.join(font_dir, file)
                    font_id = QFontDatabase.addApplicationFont(font_path)
                    if font_id != -1:
                        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                        if font_family:
                            self.fontComboBox.addItem(font_family)

        # Set the default font if available
        available_fonts = [self.fontComboBox.itemText(i) for i in range(self.fontComboBox.count())]
        if default_font in available_fonts:
            self.fontComboBox.setCurrentFont(QFont(default_font))
            print(f"Default font set to: {default_font}")
        else:
            print("Default font not found, using system default.")

        self.fontComboBox.currentFontChanged.connect(self.editor.setFontFamily)

        # Font Size Selection
        self.fontSizeComboBox = QComboBox(self.editor)
        self.fontSizeComboBox.addItems([str(size) for size in range(8, 49, 2)])
        self.fontSizeComboBox.setCurrentText("12")  # Default font size
        self.fontSizeComboBox.currentIndexChanged.connect(self.editor.setFontSize)
        self.formatbar.addWidget(self.fontSizeComboBox)

        # Formatting Actions
        actions = [
            self.fontColor, self.boldAction, self.italicAction, self.underlineAction,
            self.fontbackColor, self.strikeAction, self.superAction, self.subAction,
            self.alignLeftAction, self.alignCenterAction, self.alignRightAction,
            self.alignJustifyAction, self.indentAction, self.dedentAction, self.line_para_spacing
        ]

        for action in actions:
            self.formatbar.addAction(action)

        print("All fonts loaded successfully.")
