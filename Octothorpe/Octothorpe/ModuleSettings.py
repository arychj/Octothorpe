from abc import ABCMeta, abstractmethod

from .Config import Config

class ModuleSettings(metaclass=ABCMeta):

    @property
    @abstractmethod
    def _base_key(self):
        pass

    @property
    def Settings(self):
        if("_settings" not in locals()):
            self._settings = _module_settings(self._base_key)
        
        return self._settings

class _module_settings():

    def __init__(self, base_key):
        self._base_key = base_key

    def GetInt(self, key):
        val = self._raw(key)

        if(val != None):
            val = int(val[0].text)

        return val

    def GetBool(self, key):
        val = self._raw(key)

        if(val != None):
            val = (True if val[0].text.lower() == "true" else False)

        return val

    def GetString(self, key):
        val = self._raw(key)

        if(val != None):
            val = val[0].text

        return val

    def GetMultiple(self, key):
        return self._raw(key)

    def _raw(self, key):
        return Config._raw(f"{self._base_key}/{key}")
    