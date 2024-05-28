from PyQt5.QtWidgets import QDialog, QFormLayout, QComboBox, QLabel, QSpinBox


class SpacingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_editor = parent
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.lineSpacingLabel = QLabel("Line Spacing (pixels):")
        self.lineSpacingComboBox = QComboBox()
        self.lineSpacingComboBox.addItems([str(i) for i in range(6)] + ["Custom"])
        self.lineSpacingComboBox.currentIndexChanged.connect(self.lineSpacingChanged)
        self.customLineSpacingSpinBox = QSpinBox()
        self.customLineSpacingSpinBox.setRange(1, 100)
        self.customLineSpacingSpinBox.setEnabled(False)
        layout.addRow(self.lineSpacingLabel, self.lineSpacingComboBox)
        layout.addRow("Custom Line Spacing:", self.customLineSpacingSpinBox)

        self.beforeParagraphLabel = QLabel("Add Space Before Paragraph (pixels):")
        self.beforeParagraphSpinBox = QSpinBox()
        self.beforeParagraphSpinBox.setRange(0, 100)
        layout.addRow(self.beforeParagraphLabel, self.beforeParagraphSpinBox)

        self.afterParagraphLabel = QLabel("Add Space After Paragraph (pixels):")
        self.afterParagraphSpinBox = QSpinBox()
        self.afterParagraphSpinBox.setRange(0, 100)
        layout.addRow(self.afterParagraphLabel, self.afterParagraphSpinBox)

        self.setLayout(layout)

    def lineSpacingChanged(self):
        if self.lineSpacingComboBox.currentText() == "Custom":
            self.customLineSpacingSpinBox.setEnabled(True)
        else:
            self.customLineSpacingSpinBox.setEnabled(False)
            value = int(self.lineSpacingComboBox.currentText())
            self.customLineSpacingSpinBox.setValue(value)
            self.parent_editor.setLineSpacing(value)

    def applySettings(self):
        lineSpacing = self.customLineSpacingSpinBox.value() if self.lineSpacingComboBox.currentText() == "Custom" else int(self.lineSpacingComboBox.currentText())
        self.parent_editor.setLineSpacing(lineSpacing)
        self.parent_editor.setParagraphSpacing(self.beforeParagraphSpinBox.value(), self.afterParagraphSpinBox.value())
