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
- [PySide6](https://pypi.org/project/PySide6/)
- [Requests](https://pypi.org/project/requests/)

## Running
### (Require Python 3.x)
- Just execute `python app.pyw` in a terminal.

## Building (Windows)
### (Require [Nuitka](https://pypi.org/project/Nuitka/) package)
- Just execute `build.bat`. A file named **86BoxUpdater.exe** file should be created in the project directory.
