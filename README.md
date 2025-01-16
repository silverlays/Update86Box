# Auto Updater for 86Box with GUI (Qt)

<p align="center">
  <img src="https://github.com/user-attachments/assets/24408e2d-ec27-40a9-a7c4-58acb8962ed3"/>
</p>

## Features
- Update or download 86Box executable from the last available artifact (you can choose between Old and New dynarec). Only the 64 bits version for now.
- Update or download the last ROMS package. (mandatory for 86Box)
- Show a changelog between the installed and the last version.
- Auto detect if ROMS must be updated too. (based on modification date Vs the last commit date)
- Only show GUI if executable or roms must be updated, otherwise it just try the feature below.
- Execute `86Manager.exe` (if found in the same folder) after update or it just close itself.

## Requirements
- [Python 3.5+](https://www.python.org/downloads/)
- [PySide6-Essentials](https://pypi.org/project/PySide6-Essentials/)
- [requests](https://pypi.org/project/requests/)
- [pywin32](https://pypi.org/project/pywin32/) (only for Windows)
- [Nuitka](https://pypi.org/project/Nuitka/) (for building only)

## Running
- Just execute `python app.pyw` in a terminal.

## Building (Windows)
- Just execute `build.bat` in a terminal. (A file named **86BoxUpdater.exe** file should be created in the project directory)
