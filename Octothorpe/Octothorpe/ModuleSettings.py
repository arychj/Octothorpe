from abc import ABCMeta, abstractmethod

from .Config import Config

class ModuleSettings(metaclass=ABCMeta):

    @property
    @abstractmethod
    def _base_key(self):
        pass

    def GetInt(self, key):
        val = self._raw(key)[0].text

        if(val != None):
            val = int(val)

        return val

    def GetBool(self, key):
        val = self._raw(key)[0].text

        if(val != None):
            val = (True if val.lower() == "true" else False)

        return val

    def GetString(self, key):
        return self._raw(key)[0].text

    def GetMultiple(self, key):
        return self._raw(key)

    def _raw(self, key):
        return Config._raw(f"{self._base_key}/{key}")
    