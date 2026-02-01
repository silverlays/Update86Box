import json
import os
import requests
from contextlib import suppress
from datetime import datetime
from zipfile import ZipFile

from PySide6.QtCore import Signal, QFile, QObject, SignalInstance
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

import constants as c
from ui_tools import StatusText
from progressbar import ProgressBarCustom


### DOWNLOAD THREAD START ###
class DownloadWorker(QObject):
    aborted = Signal(str)
    initiated = Signal(str)
    extracting = Signal(str)
    download_updated = Signal(int, int)
    task_completed = Signal()

    def __init__(self, source: str, target: str):
        super().__init__()
        self._source_url = source
        self._target_file = QFile(target)
        self._nam = QNetworkAccessManager()

    def run(self) -> None:
        assert self._source_url, "No source url specified."
        assert self._target_file, "No target file specified."
        self.initiated.emit("Loading...")
        request = QNetworkRequest(self._source_url)
        self.reply = self._nam.get(request)
        self.reply.downloadProgress.connect(self.on_download_progress)
        self.reply.errorOccurred.connect(self.on_error_occured)
        self.reply.finished.connect(self.on_finished)

    def on_error_occured(self, error: QNetworkReply.NetworkError):
        self.aborted.emit(str(error.value))

    def on_finished(self):
        self.extracting.emit("Extracting...")
        self._target_file.open(QFile.OpenModeFlag.WriteOnly)
        self._target_file.write(self.reply.readAll())
        self._target_file.close()
        try:
            if c.ZIP_86BOX_NAME in self._target_file.fileName():
                with ZipFile(self._target_file.fileName()) as zf:
                    zf.extractall()
                os.remove(self._target_file.fileName())
            elif c.ZIP_ROMS_NAME in self._target_file.fileName():
                with ZipFile(self._target_file.fileName()) as zf:
                    for zip_info in zf.filelist:
                        if zip_info.filename != "roms-master/":
                            zip_info.filename = zip_info.filename.replace(
                                "roms-master/", "roms/"
                            )
                            zf.extract(zip_info)
                os.remove(self._target_file.fileName())
        except Exception as e:
            print(e)
            self.aborted.emit(e.args[0])
        finally:
            self.deleteLater()

    def on_download_progress(self, bytes_received: int, bytes_total: int):
        if bytes_total == -1:
            # Download finish
            bytes_total = bytes_received
        self.download_updated.emit(bytes_received, bytes_total)


class Remote:
    _jenkins_last_build = -1
    _github_last_commit = datetime(2000, 1, 1, 0, 0, 0, 0)
    download_workers: list[QObject] = []

    @classmethod
    def load(cls):
        # Jenkins last successful build
        with suppress(Exception):
            response = requests.get(f"{c.JENKINS_BASE_URL}/api/json")
            if response.status_code == 200:
                json_data = json.loads(response.content)
                cls._jenkins_last_build = int(
                    json_data["lastSuccessfulBuild"]["number"]
                )

        # Github roms last commit date
        with suppress(Exception):
            response = requests.get(c.ROMS_COMMITS_URL)
            if response.status_code == 200:
                json_data = json.loads(response.content)
                date_str = json_data[0]["commit"]["verification"]["verified_at"]
                cls._github_last_commit = datetime.strptime(
                    date_str, "%Y-%m-%dT%H:%M:%SZ"
                )

    @classmethod
    def download86Box(
        cls, ndr: bool, pb: ProgressBarCustom | None, callback: SignalInstance | None
    ):
        """Download the last artifact of 86Box from Jenkins.

        Args:
            ndr (bool): Specify if we must download the New Dynarec instead of the Old Dynarec.
            pb (ProgressBarCustom, optional): The progress bar used for progression.
            callback (Signal, optional): The signal who will be send at the end of the work.
        """
        if cls._jenkins_last_build == -1:
            StatusText.setText("No remote build found.")

        worker = DownloadWorker(cls._buildArtifactURL(ndr), c.ZIP_86BOX_FILE)
        if pb:
            worker.aborted.connect(pb.showErrorText)
            worker.initiated.connect(pb.showInformationText)
            worker.download_updated.connect(pb.setValueAndMax)
            worker.extracting.connect(pb.showInformationText)
            worker.destroyed.connect(pb.showDoneText)
        worker.destroyed.connect(lambda: cls.download_workers.remove(worker))
        if callback:
            worker.destroyed.connect(callback.emit)
        cls.download_workers.append(worker)
        pb.show()  # type: ignore
        worker.run()

    @classmethod
    def downloadRoms(
        cls, pb: ProgressBarCustom | None, callback: SignalInstance | None
    ):
        """Download the last Roms repository.

        Args:
            pb (ProgressBarCustom, optional): The progress bar used for progression.
            callback (Signal, optional): The signal who will be send at the end of the work.
        """
        worker = DownloadWorker(c.ROMS_URL, c.ZIP_ROMS_FILE)
        if pb:
            worker.aborted.connect(pb.showErrorText)
            worker.initiated.connect(pb.showInformationText)
            worker.download_updated.connect(pb.setValueAndMax)
            worker.extracting.connect(pb.showInformationText)
            worker.destroyed.connect(pb.showDoneText)
        worker.destroyed.connect(lambda: cls.download_workers.remove(worker))
        if callback:
            worker.destroyed.connect(callback.emit)
        cls.download_workers.append(worker)
        pb.show()  # type: ignore
        worker.run()

    @classmethod
    def getChangelog(cls, local_build: int) -> str:
        """Get the changelog from the local build until the last build.

        Args:
            installed_build (int): The local build number.

        Returns:
            str: Return the formatted changelog.
        """
        cls._markdown_text = ""
        if local_build != -1 and cls._jenkins_last_build != -1:
            for current_build in range(cls._jenkins_last_build, local_build, -1):
                try:
                    response = requests.get(
                        f"{c.JENKINS_BASE_URL}/{current_build}/api/json"
                    )
                    if response.status_code == 200:
                        cls._AddChangesToMarkdown(
                            current_build, json.loads(response.content)
                        )
                except Exception:
                    cls._markdown_text = "Error during the changelog request."
            return cls._markdown_text
        else:
            return "Too long to be parsed here"

    @classmethod
    def _buildArtifactURL(cls, ndr: bool):
        if ndr:
            return f"{c.JENKINS_BASE_URL}/{cls._jenkins_last_build}/artifact/New Recompiler (beta)/Windows - x64 (64-bit)/86Box-NDR-Windows-64-b{cls._jenkins_last_build}.zip"
        else:
            return f"{c.JENKINS_BASE_URL}/{cls._jenkins_last_build}/artifact/Old Recompiler (recommended)/Windows - x64 (64-bit)/86Box-Windows-64-b{cls._jenkins_last_build}.zip"

    @classmethod
    def _AddChangesToMarkdown(cls, build: int, json_dict: dict):
        changes_set = json_dict["changeSets"]

        if changes_set:
            items = changes_set[0]["items"]
            if len(items) > 1:
                cls._markdown_text += f"[#{build}]({c.JENKINS_BASE_URL}/{build}):  \n"
                for item in items:
                    cls._markdown_text += f"-  {item["msg"]}  \n"
                cls._markdown_text += "\n"
            elif len(items) == 1:
                cls._markdown_text += (
                    f"[#{build}]({c.JENKINS_BASE_URL}/{build}): {items[0]["msg"]}\n\n"
                )
        else:
            cls._markdown_text += (
                f"[#{build}]({c.JENKINS_BASE_URL}/{build}): No changes.\n\n"
            )
