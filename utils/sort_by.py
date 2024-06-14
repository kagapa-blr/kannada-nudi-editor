from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGroupBox, QComboBox, QRadioButton, QLineEdit, QLabel, QHBoxLayout, QPushButton

class SortDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sort")

        layout = QVBoxLayout()

        # Sort By
        sort_by_group = QGroupBox("Sort by")
        sort_by_layout = QVBoxLayout()
        self.combo_sort_by = QComboBox()
        self.combo_sort_by.addItems(["Paragraph", "Headings", "Fields", "Header Name", "Column Number"])
        sort_by_layout.addWidget(self.combo_sort_by)
        sort_by_group.setLayout(sort_by_layout)

        # Type
        type_group = QGroupBox("Type")
        type_layout = QVBoxLayout()
        self.combo_type = QComboBox()
        self.combo_type.addItems(["Text", "Number", "Date"])
        type_layout.addWidget(self.combo_type)
        type_group.setLayout(type_layout)

        # Using
        using_group = QGroupBox("Using")
        using_layout = QVBoxLayout()
        self.combo_using = QComboBox()
        self.combo_using.addItems(["Paragraphs", "Fields"])
        using_layout.addWidget(self.combo_using)
        using_group.setLayout(using_layout)

        # Ascending or Descending
        order_group = QGroupBox("Ascending or Descending")
        order_layout = QVBoxLayout()
        self.radio_asc = QRadioButton("Ascending")
        self.radio_desc = QRadioButton("Descending")
        self.radio_asc.setChecked(True)
        order_layout.addWidget(self.radio_asc)
        order_layout.addWidget(self.radio_desc)
        order_group.setLayout(order_layout)

        # My list has
        list_has_group = QGroupBox("My list has")
        list_has_layout = QVBoxLayout()
        self.check_has_header = QRadioButton("Headers")
        self.check_no_header = QRadioButton("No Headers")
        self.check_has_header.setChecked(True)
        list_has_layout.addWidget(self.check_has_header)
        list_has_layout.addWidget(self.check_no_header)
        list_has_group.setLayout(list_has_layout)

        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        self.line_separator = QLineEdit()
        self.combo_sort_options = QComboBox()
        self.combo_sort_options.addItems(["Sort column only", "Case sensitive"])
        options_layout.addWidget(QLabel("Where to separate fields (Tabs, Comma, Other)"))
        options_layout.addWidget(self.line_separator)
        options_layout.addWidget(QLabel("Sort options"))
        options_layout.addWidget(self.combo_sort_options)
        options_group.setLayout(options_layout)

        buttons_layout = QHBoxLayout()
        self.btn_sort = QPushButton("Sort")
        self.btn_cancel = QPushButton("Cancel")
        buttons_layout.addWidget(self.btn_sort)
        buttons_layout.addWidget(self.btn_cancel)

        layout.addWidget(sort_by_group)
        layout.addWidget(type_group)
        layout.addWidget(using_group)
        layout.addWidget(order_group)
        layout.addWidget(list_has_group)
        layout.addWidget(options_group)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.btn_sort.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
