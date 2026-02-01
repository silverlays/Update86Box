import os, sys


EXECUTABLE_PATH = (
    os.path.abspath(".")
    if not hasattr(sys.modules[__name__], "__compiled__")
    else os.path.dirname(sys.argv[0])
)


### LOCAL
EXECUTABLE_NAME = "86Box.exe"
EXECUTABLE_FILE = os.path.join(EXECUTABLE_PATH, EXECUTABLE_NAME)

ZIP_86BOX_NAME = "86Box.zip"
ZIP_86BOX_FILE = os.path.join(EXECUTABLE_PATH, ZIP_86BOX_NAME)

ZIP_ROMS_NAME = "Roms.zip"
ZIP_ROMS_FILE = os.path.join(EXECUTABLE_PATH, ZIP_ROMS_NAME)


### REMOTE
JENKINS_BASE_URL = "https://ci.86box.net/job/86Box"
ROMS_COMMITS_URL = "https://api.github.com/repos/86Box/roms/commits"
ROMS_URL = "https://github.com/86Box/roms/archive/refs/heads/master.zip"


### SETTINGS
SETTINGS_FILE = os.path.join(EXECUTABLE_PATH, "86BoxUpdater.json")
