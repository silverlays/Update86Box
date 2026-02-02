import os
import win32api
from datetime import datetime
from contextlib import suppress

from constants import *


class Local:
    build = -1
    roms_mtime = datetime(1970, 1, 1, 0, 0, 0, 0)

    @classmethod
    def load(cls):
        # Executable version
        with suppress(Exception):
            version = win32api.GetFileVersionInfo(EXECUTABLE_FILE, "\\")
            cls.build = version["FileVersionLS"] & 0xFFFF

        # Roms modification date
        with suppress(Exception):
            modification_time = os.path.getmtime(r"roms\README.md")
            cls.roms_mtime = datetime.fromtimestamp(modification_time)
