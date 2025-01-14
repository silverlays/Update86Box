import json
import os
import requests
from datetime import datetime
from zipfile import ZipFile

from PySide6.QtCore import Signal, QFile, QObject
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

import local
from progressbar import ProgressBarCustom

JENKINS_BASE_URL = "https://ci.86box.net/job/86Box"
ROMS_COMMITS_URL = "https://api.github.com/repos/86Box/roms/commits"
ROMS_URL = "https://github.com/86Box/roms/archive/refs/heads/master.zip"

last_build = -1
roms_mtime = datetime(2000, 1, 1, 0, 0, 0, 0)
download_workers: list[QObject] = []


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
    self.initiated.emit("Please wait...")
    request = QNetworkRequest(self._source_url)
    self.reply = self._nam.get(request)
    self.reply.downloadProgress.connect(self.on_download_progress)
    self.reply.errorOccurred.connect(self.on_error_occured)
    self.reply.finished.connect(self.on_finished)
  
  def on_error_occured(self, error: QNetworkReply.NetworkError):
    print(error.value)
    self.aborted.emit(str(error.value))

  def on_finished(self):
    self.extracting.emit("Extracting...")
    self._target_file.open(QFile.OpenModeFlag.WriteOnly)
    self._target_file.write(self.reply.readAll())
    self._target_file.close()
    try:
      if local.ZIPFILE_86BOX in self._target_file.fileName():
        with ZipFile(self._target_file.fileName()) as zf:
          zf.extractall()
        os.remove(self._target_file.fileName())
      elif local.ZIPFILE_ROMS in self._target_file.fileName():
        with ZipFile(self._target_file.fileName()) as zf:
          for zip_info in zf.filelist:
            if zip_info.filename != "roms-master/":
              zip_info.filename = zip_info.filename.replace("roms-master/", "roms/")
              zf.extract(zip_info)
        os.remove(self._target_file.fileName())
    except Exception as e:
      print(e)
      self.aborted.emit(e.args[0])
    finally:
      self.deleteLater()

  def on_download_progress(self, bytes_received: int, bytes_total: int):
    if bytes_total == -1: bytes_total = bytes_received
    self.download_updated.emit(bytes_received, bytes_total)
  ### DOWNLOAD THREAD END ###



try:
  # Jenkins get last successful build
  response = requests.get(f"{JENKINS_BASE_URL}/api/json")
  if response.status_code == 200:
    json_data = json.loads(response.content)
    last_build = int(json_data['lastSuccessfulBuild']['number'])
except: pass

try:
  # Github get roms last commit date
  response = requests.get(ROMS_COMMITS_URL)
  if response.status_code == 200:
    json_data = json.loads(response.content)
    date_str = json_data[0]['commit']['verification']['verified_at']
    roms_mtime = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
except: pass

def download86Box(ndr: bool, pb: ProgressBarCustom, callback: Signal):
  assert last_build != -1, "No remote build found."
  artifact_url = f"{JENKINS_BASE_URL}/{last_build}/artifact/"
  if ndr:
    artifact_url += f"New Recompiler (beta)/Windows - x64 (64-bit)/86Box-NDR-Windows-64-b{last_build}.zip"
  else:
    artifact_url += f"Old Recompiler (recommended)/Windows - x64 (64-bit)/86Box-Windows-64-b{last_build}.zip"
  worker = DownloadWorker(artifact_url, os.path.join(".", local.ZIPFILE_86BOX))
  worker.aborted.connect(pb.showErrorText)
  worker.initiated.connect(pb.showInformationText)
  worker.download_updated.connect(pb.setValueAndMax)
  worker.extracting.connect(pb.showInformationText)
  worker.destroyed.connect(pb.showDoneText)
  worker.destroyed.connect(lambda: download_workers.remove(worker))
  worker.destroyed.connect(callback.emit)
  download_workers.append(worker)
  pb.show()
  worker.run()

def downloadRoms(pb: ProgressBarCustom, callback: Signal):
  worker = DownloadWorker(ROMS_URL, os.path.join(".", local.ZIPFILE_ROMS))
  worker.aborted.connect(pb.showErrorText)
  worker.initiated.connect(pb.showInformationText)
  worker.download_updated.connect(pb.setValueAndMax)
  worker.extracting.connect(pb.showInformationText)
  worker.destroyed.connect(pb.showDoneText)
  worker.destroyed.connect(lambda: download_workers.remove(worker))
  worker.destroyed.connect(callback.emit)
  download_workers.append(worker)
  pb.show()
  worker.run()

def getChangelog(installed_build: int) -> str:
  plain_text = ""
  if installed_build != -1 and last_build != -1:
    try:
      for build in range(installed_build + 1, last_build + 1):
        response = requests.get(f"{JENKINS_BASE_URL}/{build}/api/json")
        if response.status_code == 200:
          json_dict = json.loads(response.content)
          items = json_dict['changeSets'][0]['items']
          for item in items:
            plain_text += f"(#{build}) {item['msg'] }\n"
      return plain_text
    except: pass
  else: return "Too long to be parsed here"
