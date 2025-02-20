from PyQt5.QtWidgets import QDialogButtonBox, QFormLayout, QDialog, QVBoxLayout, QSpinBox, QComboBox


class PageMarginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Page Margins")

        layout = QVBoxLayout(self)

        # Dropdown for predefined options
        self.margin_presets = QComboBox()
        self.margin_presets.addItems(["Normal", "Narrow", "Moderate", "Wide", "Custom"])
        self.margin_presets.currentIndexChanged.connect(self.updateMargins)

        # Margin input fields
        self.left_margin = QSpinBox()
        self.right_margin = QSpinBox()
        self.top_margin = QSpinBox()
        self.bottom_margin = QSpinBox()

        for spinbox in [self.left_margin, self.right_margin, self.top_margin, self.bottom_margin]:
            spinbox.setRange(0, 200)  # Max 2 inches (192 px)
            spinbox.setSuffix(" px")
            spinbox.setValue(96)  # Default to 1 inch
            spinbox.setEnabled(False)  # Initially disabled

        form_layout = QFormLayout()
        form_layout.addRow("Preset:", self.margin_presets)
        form_layout.addRow("Left:", self.left_margin)
        form_layout.addRow("Right:", self.right_margin)
        form_layout.addRow("Top:", self.top_margin)
        form_layout.addRow("Bottom:", self.bottom_margin)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
        self.updateMargins(0)  # Set default margins

    def updateMargins(self, index):
        """Update margin values based on preset selection."""
        presets = {
            "Normal": (96, 96, 96, 96),
            "Narrow": (48, 48, 48, 48),
            "Moderate": (96, 96, 72, 72),
            "Wide": (144, 144, 96, 96),
        }

        if self.margin_presets.currentText() in presets:
            left, right, top, bottom = presets[self.margin_presets.currentText()]
            self.left_margin.setValue(left)
            self.right_margin.setValue(right)
            self.top_margin.setValue(top)
            self.bottom_margin.setValue(bottom)

            for spinbox in [self.left_margin, self.right_margin, self.top_margin, self.bottom_margin]:
                spinbox.setEnabled(False)  # Disable editing
        else:
            for spinbox in [self.left_margin, self.right_margin, self.top_margin, self.bottom_margin]:
                spinbox.setEnabled(True)  # Enable editing for "Custom"

    def getPageMargins(self):
        return self.left_margin.value(), self.right_margin.value(), self.top_margin.value(), self.bottom_margin.value()
