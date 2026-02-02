import platform, os, re, win32api
from contextlib import suppress
from datetime import datetime
from pathlib import Path

from constants import *


class Local:
    build = -1
    roms_mtime = datetime(1970, 1, 1, 0, 0, 0, 0)

    @classmethod
    def load(cls, command_line: str):
        system = platform.system()
        path = Path(command_line)

        # --- WINDOWS ---
        if system == "Windows":
            with suppress(Exception):
                version = win32api.GetFileVersionInfo(path.__str__(), "\\")
                cls.build = version["FileVersionLS"] & 0xFFFF

        # --- MACOS (Info.plist) ---
        elif system == "Darwin":
            with suppress(Exception):
                plist_path = path.parents[1] / "Info.plist"
                if plist_path.exists():
                    import plistlib

                    with open(plist_path, "rb") as f:
                        pl = plistlib.load(f)
                        full_version = pl.get("CFBundleVersion", "")
                        cls.build = int(full_version.split(".")[-1])

        # --- LINUX (AppImage) ---
        elif system == "Linux":
            with suppress(Exception):
                match = re.search(r"-b(\d+)\.AppImage$", path.name)
                if match:
                    cls.build = int(match.group(1))
                else:
                    import subprocess

                    output = subprocess.check_output(
                        [command_line, "--version"]
                    ).decode()
                    match_v = re.search(r"build (\d+)", output)
                    if match_v:
                        cls.build = int(match_v.group(1))

        # Roms modification date
        with suppress(Exception):
            roms_path = os.path.join(os.path.dirname(command_line), "roms", "README.md")
            modification_time = os.path.getmtime(roms_path)
            cls.roms_mtime = datetime.fromtimestamp(modification_time)
