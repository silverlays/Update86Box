import json

import constants as c


class Settings:
    _data = {"new_dynarec": True, "command_line": c.EXECUTABLE_FILE}

    @property
    def new_dynarec(self):
        return self._data["new_dynarec"]

    @new_dynarec.setter
    def new_dynarec(self, value: bool):
        self._data["new_dynarec"] = value

    @property
    def command_line(self):
        return self._data["command_line"]

    @command_line.setter
    def command_line(self, value: str):
        self._data["command_line"] = value

    @classmethod
    def readSettings(cls):
        try:
            with open(c.SETTINGS_FILE, "r") as fp:
                fp_json = json.load(fp)
                if "new_dynarec" in fp_json:
                    cls.new_dynarec = fp_json["new_dynarec"]
                if "command_line" in fp_json:
                    cls.new_dynarec = fp_json["command_line"]
        except FileNotFoundError:
            cls.writeSettings()

    @classmethod
    def writeSettings(cls):
        with open(c.SETTINGS_FILE, "w") as fp:
            json.dump(cls._data, fp, indent=2)
