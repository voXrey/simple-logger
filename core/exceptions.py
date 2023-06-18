class SettingsExceptions(Exception):
    pass

class BadSettings(SettingsExceptions):
    pass

class BadSettingValue(SettingsExceptions):
    def __init__(self, setting:str, value:str, *args: object):
        self.setting, self.value = setting, value
        super().__init__(*args)

class MissingSetting(SettingsExceptions):
    def __init__(self, setting:str, *args: object):
        self.setting = setting
        super().__init__(*args)

class UnknowSetting(SettingsExceptions):
    def __init__(self, setting:str, *args: object):
        self.setting = setting
        super().__init__(*args)


class MissingSimpleLoggerChannel(Exception):
    pass

class UnknowLangage(Exception):
    def __init__(self, langage:str, *args: object):
        self.langage = langage
        super().__init__(*args)

class UnknowText(Exception):
    def __init__(self, langage:str, text_id:str, *args: object):
        self.langage, self.text_id = langage, text_id
        super().__init__(*args)

class CommandNotReferenced(Exception):
    def __init__(self, command_name, *args: object):
        self.command_name = command_name
        super().__init__(*args)

class CommandUnknow(Exception):
    def __init__(self, command_name, *args: object):
        self.command_name = command_name
        super().__init__(*args)

class ForbiddenMissingPermissions:
    pass

class ForbiddenMissingAccess:
    pass