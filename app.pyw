# Python
import os
import subprocess
import sys

# PySide6
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

# Personal
import app_rc
from mainwindow_ui import Ui_MainWindow


APP = QApplication(sys.argv)


class App(QMainWindow, Ui_MainWindow):
  download_finished = Signal()
  
  def __init__(self) -> None:
    import local, remote
    from progressbar import ProgressBarCustom
    super().__init__()
    self.setupUi(self)
    self.pbc_86Box = ProgressBarCustom(local.ZIPFILE_86BOX)
    self.pbc_roms = ProgressBarCustom(local.ZIPFILE_ROMS)

    # Check if update is needed (executable + roms)
    if local.build == remote.last_build \
      and local.roms_mtime >= remote.roms_mtime:
        self.launch86ManagerAndExit()

    if local.roms_mtime < remote.roms_mtime:
      self.updateRomsCheckBox.setChecked(True)
      self.updateRomsCheckBox.setText(self.updateRomsCheckBox.text() + " (update available)")

    self.statusbar.addWidget(self.pbc_86Box)
    self.statusbar.addWidget(self.pbc_roms)

    # Window properties
    self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
    self.download_finished.connect(self.on_download_finished)
    self.updateNowPushButton.clicked.connect(self.updateNow)
    self.notNowPushButton.clicked.connect(self.launch86ManagerAndExit)

    # Window data setup
    self.installedBuildLabel.setText(str(local.build))
    self.lastestBuildLabel.setText(str(remote.last_build))
    self.changelogPlainText.setPlainText(remote.getChangelog(local.build))

    self.show()
    sys.exit(APP.exec())

  def launch86ManagerAndExit(self):
    if os.path.exists("86Manager.exe"):
      subprocess.Popen("86Manager.exe", creationflags=subprocess.DETACHED_PROCESS, close_fds=True)
    self.close()
    sys.exit(0)

  def on_download_finished(self):
    import remote
    if len(remote.download_workers) == 0:
      self.launch86ManagerAndExit()

  def updateNow(self):
    import remote
    self.updateNowPushButton.setEnabled(False)
    remote.download86Box(self.newDynarecCheckBox, self.pbc_86Box, self.download_finished)
    if self.updateRomsCheckBox.isChecked():
      remote.downloadRoms(self.pbc_roms, self.download_finished)


if __name__ == "__main__":
  APP.setApplicationName("86BoxUpdater")
  APP.setDesktopFileName("86BoxUpdater")
  APP.setWindowIcon(QIcon(":/icons/app.png"))
  App()
