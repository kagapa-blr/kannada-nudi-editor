import csv

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from openpyxl import load_workbook


class ExcelCsvViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel/CSV Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Set up the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add button to open files
        self.open_button = QPushButton("Open Excel/CSV File")
        self.open_button.clicked.connect(self.open_file)
        self.layout.addWidget(self.open_button)

        # Add table to display file data
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    def open_file(self):
        # Open file dialog
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel/CSV File", "", "Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            if file_name.endswith('.xlsx'):
                self.load_excel(file_name)
            elif file_name.endswith('.csv'):
                self.load_csv(file_name)

    def load_excel(self, file_name):
        # Load the Excel file
        workbook = load_workbook(file_name)
        sheet = workbook.active

        # Get the dimensions of the sheet
        rows = sheet.max_row
        columns = sheet.max_column

        # Set the table row and column count
        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)

        # Fill the table with data
        for i, row in enumerate(sheet.iter_rows(values_only=True)):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def load_csv(self, file_name):
        # Load the CSV file
        with open(file_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        # Get the dimensions of the data
        rows = len(data)
        columns = len(data[0]) if rows > 0 else 0

        # Set the table row and column count
        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)

        # Fill the table with data
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))