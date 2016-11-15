import threading, time

from abc import ABCMeta, abstractmethod
from functools import lru_cache
from importlib import import_module

from .Config import Config
from .Log import Log

class DynamicModule(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def _module_type(self):
        pass

    def Debug(self, message):
        Log.Debug(message, tag=self._name)

    def GetSetting(self, key):
        return self.GetSettings(key)[0].text

    def GetSettings(self, key):
        return Config._raw(f"{self._module_type}s/{self._module_type}[@name='{self._name}']/{key}")

    @staticmethod
    @lru_cache(maxsize=64)
    def _get_module(type, name):
        xModule = Config._raw(f"{type}s/{type}[@name='{name}']")
        if(len(xModule) == 1):
            xModule = xModule[0]
            module = (xModule.attrib["module"] if ('module' in xModule.attrib) else xModule.attrib["name"])

            return getattr(import_module(f".{type.title()}s.{module}", "Octothorpe"), name[name.find('.') + 1:])
        else:
            return None
