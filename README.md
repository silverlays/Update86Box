# Auto Updater for 86Box with GUI (Qt)

<p align="center">
  <img src="https://github.com/user-attachments/assets/24408e2d-ec27-40a9-a7c4-58acb8962ed3"/>
</p>

## Features
- Update or download 86Box executable from the last available artifact (you can choose between Old and New dynarec). Only the 64 bits version for now.
- Update or download with the last Roms repository. (mandatory for 86Box)
- Show a changelog between the installed and the last version.
- Auto detect if Roms must be updated too. (based on modification date Vs the last commit date)
- Only show GUI if executable or Roms must be updated, otherwise it just try the feature below.
- Execute `86Manager.exe` ([https://github.com/86Box/86BoxManager](https://github.com/86Box/86BoxManager)) or `Avalonia86.exe` ([https://github.com/notBald/Avalonia86](https://github.com/notBald/Avalonia86)) (if found in the same folder) after update or just close itself.

## Requirements
- [Python 3.5+](https://www.python.org/downloads/)
- [PySide6-Essentials](https://pypi.org/project/PySide6-Essentials/)
- [requests](https://pypi.org/project/requests/)
- [pywin32](https://pypi.org/project/pywin32/) (only for Windows)
- [Nuitka](https://pypi.org/project/Nuitka/) (for building only)

---

## Running
### (Windows) Install dependecies first !
`python3 -m pip install --user -r requirements-win.txt`
### (Linux)
`python3 -m pip install --user -r requirements-linux.txt`
### (Windows/Linux) Run the program
`python3 main.py`

---

## Building (Windows)
```
python3 -m pip install --user -r requirements-win.txt && python3 -m nuitka --onefile --windows-console-mode=disable --enable-plugin=pyside6 --windows-icon-from-ico=app.ico --output-filename=86BoxUpdater --deployment --remove-output app.pyw
```
(A file named **86BoxUpdater.exe** file should be created in the project directory)

## Building (Linux)
### Not tested yet. It can broke. Let me know if you have issues.
```
python3 -m pip install --user -r requirements-linux.txt && python3 -m nuitka --onefile --windows-console-mode=disable --enable-plugin=pyside6 --windows-icon-from-ico=app.ico --output-filename=86BoxUpdater --deployment --remove-output app.pyw
```
(A file named **86BoxUpdater.bin** file should be created in the project directory)
