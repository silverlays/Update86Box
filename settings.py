from constants import *

from PySide6.QtCore import QSettings


class Settings:
    _new_dynarec = True
    _command_line = EXECUTABLE_FILE

    def __init__(self):
        self.qs = QSettings()
        self._new_dynarec = self.qs.value("new_dynarec", self._new_dynarec, type=bool)
        self._command_line = self.qs.value("command_line", self._command_line, type=str)

    @property
    def new_dynarec(self):
        return self._new_dynarec

    @new_dynarec.setter
    def new_dynarec(self, value: bool):
        self._new_dynarec = value
        self.qs.setValue("new_dynarec", self._new_dynarec)

    @property
    def command_line(self):
        return self._command_line

    @command_line.setter
    def command_line(self, value: str):
        if value and os.path.exists(value):
            self._command_line = value
            self.qs.setValue("command_line", self._command_line)
        else:
            raise FileNotFoundError()
