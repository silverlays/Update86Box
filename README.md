# Auto Updater for 86Box with GUI (Qt)

## Features
- Update or download 86Box executable from the last available artifact.
- Update or download the last ROMS package (mandatory for 86Box)
- Show a changelog between the installed and the last version
- Execute `86Manager.exe` (if found in the same folder) after update or close itself.

## Requirements
- [PySide6](https://pypi.org/project/PySide6/)
- [Requests](https://pypi.org/project/requests/)

## Running
### (Require Python 3.x)
- Just execute `python app.pyw` in a terminal.

## Building (Windows)
### (Require [Nuitka](https://pypi.org/project/Nuitka/) package)
- Just execute `build.bat`. A file named **86BoxUpdater.exe** file should be created in the project directory.
