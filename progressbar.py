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
    fvalue = ((self._progressbar.value() / 1024) / 1024)
    fmaximum = ((self._progressbar.maximum() / 1024) / 1024)
    self._text_label.setStyleSheet("color: white")
    self._text_label.setText(self._filename)
    self._progressbar.show()
    self._progressbar_label.setText(f"{fvalue:.1f} / {fmaximum:.1f} Mb")
    self._progressbar_label.show()
    self.update()

  def setValueAndMax(self, value: int, maximum: int):
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