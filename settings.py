from constants import *

from PySide6.QtCore import QSettings


class Settings:
    new_dynarec = True
    command_line = EXECUTABLE_FILE

    def __init__(self):
        self.qs = QSettings()
        self.new_dynarec = self.qs.value("new_dynarec", self.new_dynarec, type=bool)
        self.command_line = self.qs.value("command_line", self.command_line, type=str)

    def writeSettings(self):
        self.qs.setValue("new_dynarec", self.new_dynarec)
        self.qs.setValue("command_line", self.command_line)
