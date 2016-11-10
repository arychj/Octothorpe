import xml.etree.ElementTree as ET

from functools import lru_cache

class Config():
    _configfile = None
    _config = None

    @classmethod
    def SetConfigFile(cls, f):
        cls._configfile = f

    @classmethod
    @lru_cache(maxsize=32)
    def GetString(cls, key):
        return cls._get_setting(key)

    @classmethod
    @lru_cache(maxsize=32)
    def GetInt(cls, key):
        val = cls._get_setting(key)

        if(val != None):
            val = int(val)

        return val

    @classmethod
    @lru_cache(maxsize=32)
    def GetBool(cls, key):
        val = cls._get_setting(key)

        if(val != None):
            val = (True if val.lower() == "true" else False)

        return val

    @classmethod
    def _get_setting(cls, key):
        if(cls._config == None):
            cls._load_config()

        return cls._config.find(key).text
    
    @classmethod
    def _raw(cls, key):
        if(cls._config == None):
            cls._load_config()

        return cls._config.findall(key)

    @classmethod
    def _load_config(cls):
        if(cls._configfile == None):
            raise Exception("no config file specified.")
        else:
            with open(cls._configfile) as _configfile:
                tree = ET.parse(_configfile)
                cls._config = tree.getroot()

