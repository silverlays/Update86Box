# Python
import os
import sys

# PySide6
from PySide6.QtCore import Qt, Signal, QObject, QThread
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

# Personal
from local import Local as l
from remote import Remote as r
from settings import Settings
from ui_tools import StatusText
from constants import *

from ui.mainwindow_ui import Ui_MainWindow
from progressbar import ProgressBarCustom


class LoadingWorker(QObject):
    changelog_finished = Signal(str)

    def run(self):
        changelog = r.getChangelog(l.build)
        self.changelog_finished.emit(changelog)


class Main(QMainWindow, Ui_MainWindow):
    download_finished = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.statusbar.addPermanentWidget(StatusText.getWidget())
        self.settings = Settings()
        l.load(self.settings.command_line)  # type: ignore
        r.load()

        # Loading thread
        self.loading_thread = QThread()
        self.loading_worker = LoadingWorker()
        self.loading_worker.moveToThread(self.loading_thread)

        self.loading_thread.started.connect(self.loading_worker.run)
        self.loading_worker.changelog_finished.connect(self.on_changelog_received)
        self.loading_worker.changelog_finished.connect(self.checkUpdateNeeded)
        self.loading_worker.changelog_finished.connect(self.loading_thread.quit)
        self.loading_worker.changelog_finished.connect(self.loading_thread.deleteLater)

        self.loading_thread.start()

        if l.roms_mtime < r._github_last_commit:
            self.updateRomsCheckBox.setChecked(True)
            self.updateRomsCheckBox.setText(
                f"{self.updateRomsCheckBox.text()} (update available)"
            )

        # Window events
        self.download_finished.connect(self.on_download_finished)

        ## Widgets events
        self.newDynarecCheckBox.toggled.connect(self.on_new_dynarec_toggled)
        self.updateNowPushButton.clicked.connect(self.updateNow)
        self.notNowPushButton.clicked.connect(self.launchCommandLine)

        # Window properties
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        self.newDynarecCheckBox.setChecked(self.settings.new_dynarec)  # type: ignore
        self.installedBuildLabel.setText(str(l.build))
        self.lastestBuildLabel.setText(str(r._jenkins_last_build))
        self.commandLineLineEdit.setText(self.settings.command_line)  # type: ignore

    def checkUpdateNeeded(self):
        if l.build == r._jenkins_last_build and l.roms_mtime >= r._github_last_commit:
            self.launchCommandLine()
            self.close()

    def launchCommandLine(self):
        if os.path.exists(self.settings.command_line):  # type: ignore
            os.startfile(self.settings.command_line)  # type: ignore

    def on_download_finished(self):
        if len(r.download_workers) == 0:
            self.launchCommandLine()
            self.close()

    def on_changelog_received(self, changelog: str):
        self.changelogTextBrowser.setMarkdown(changelog)

    def on_new_dynarec_toggled(self, checked: bool):
        self.settings.new_dynarec = checked

    def on_update_commandline_button_clicked(self):
        try:
            self.settings.command_line = self.commandLineLineEdit.text()
        except FileNotFoundError:
            self.commandLineLineEdit.setProperty("error", True)

    def updateNow(self):
        self.pbc_86Box = ProgressBarCustom(ZIP_86BOX_NAME)
        self.updateNowPushButton.setEnabled(False)
        self.statusbar.addWidget(self.pbc_86Box)
        r.download86Box(
            self.newDynarecCheckBox.isChecked(), self.pbc_86Box, self.download_finished
        )

        if self.updateRomsCheckBox.isChecked():
            self.pbc_roms = ProgressBarCustom(ZIP_ROMS_NAME)
            self.statusbar.addWidget(self.pbc_roms)
            r.downloadRoms(self.pbc_roms, self.download_finished)


if __name__ == "__main__":
    app = QApplication()
    app.setOrganizationName("INFORLAC")
    app.setApplicationName("86BoxUpdater")
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "app.ico")))
    window = Main()
    window.show()
    sys.exit(app.exec())
