import threading, time

from abc import ABCMeta, abstractmethod
from functools import lru_cache
from importlib import import_module

from .Config import Config
from .Log import Log
from .ModuleSettings import ModuleSettings
from .NamedInstance import NamedInstance

class DynamicModule(NamedInstance, ModuleSettings, metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def _module_type(self):
        pass

    @property
    def _base_key(self):
        return f"{self._module_type}s/{self._module_type}[@name='{self.Name}']"

    def Debug(self, message):
        Log.Debug(message, tag=self.Name)

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
