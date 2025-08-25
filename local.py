import os
from datetime import datetime


ZIPFILE_86BOX = "86Box.zip"
ZIPFILE_ROMS = "Roms.zip"

build = -1
roms_mtime = datetime(1970, 1, 1, 0, 0, 0, 0)


# Executable version
try:
    import win32api

    version = win32api.GetFileVersionInfo(
        os.path.join(os.path.abspath("."), "86Box.exe"), "\\"
    )
    build = version["FileVersionLS"] & 0xFFFF
except:
    pass

# Roms modification date
try:
    modification_time = os.path.getmtime(r"roms\README.md")
    roms_mtime = datetime.fromtimestamp(modification_time)
except:
    pass
