import json

import constants as c


class Settings:
    _data = {"new_dynarec": True, "command_line": c.EXECUTABLE_FILE}

    @classmethod
    def getNewDynarec(cls):
        return cls._data["new_dynarec"]

    @classmethod
    def setNewDynarec(cls, value: bool):
        cls._data["new_dynarec"] = value

    @classmethod
    def readSettings(cls):
        try:
            with open(c.SETTINGS_FILE, "r") as fp:
                fp_json = json.load(fp)
                if "new_dynarec" in fp_json:
                    cls._data["new_dynarec"] = fp_json["new_dynarec"]
                if "command_line" in fp_json:
                    cls._data["command_line"] = fp_json["command_line"]
        except FileNotFoundError:
            cls.writeSettings()

    @classmethod
    def writeSettings(cls):
        with open(c.SETTINGS_FILE, "w") as fp:
            json.dump(cls._data, fp, indent=2)
