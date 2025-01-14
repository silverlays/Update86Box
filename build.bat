@echo off
python -m nuitka --onefile ^
 --windows-console-mode=disable ^
 --enable-plugin=pyside6 ^
 --windows-icon-from-ico=app.ico ^
 --output-filename=86BoxUpdater.exe ^
 --deployment ^
 --remove-output ^
 app.pyw
