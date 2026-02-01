from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QProgressBar, QLabel, QHBoxLayout


class ProgressBarCustom(QWidget):
    def __init__(self, filename: str):
        super().__init__()
        self._filename = filename
        self._text_label = QLabel(filename)
        self._progressbar = QProgressBar()
        self._progressbar_label = QLabel()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        self._progressbar.setMaximum(0)
        self._progressbar.setValue(0)
        self._progressbar.setTextVisible(False)
        layout.addWidget(self._text_label)
        layout.addWidget(self._progressbar)
        layout.addWidget(self._progressbar_label)
        self.setLayout(layout)
        self.hide()

    def _update(self):
        self._text_label.setStyleSheet("color: white")
        self._text_label.setText(self._filename)
        self._progressbar.show()

        if self.fvalue == self.fmaximum:
            self._progressbar_label.setText(f"{self.fmaximum:.1f} Mo")
        else:
            self._progressbar_label.setText(
                f"{self.fvalue:.1f} / {self.fmaximum:.1f} Mo"
            )
        self._progressbar_label.show()
        self.update()

    def setValueAndMax(self, value: int, maximum: int):
        self.fvalue = value / 1048576
        self.fmaximum = maximum / 1048576
        self._progressbar.setValue(value)
        self._progressbar.setMaximum(maximum)
        self._update()

    @Slot(str)
    def showInformationText(self, text: str):
        self._progressbar.hide()
        self._progressbar_label.hide()
        self._text_label.setStyleSheet("color: blue")
        self._text_label.setText(text)

    @Slot(str)
    def showErrorText(self, error: str):
        self._progressbar.hide()
        self._progressbar_label.hide()
        self._text_label.setStyleSheet("color: red")
        self._text_label.setText(error)

    @Slot()
    def showDoneText(self):
        self._progressbar.hide()
        self._progressbar_label.hide()
        self._text_label.setStyleSheet("color: green")
        self._text_label.setText("Done!")
