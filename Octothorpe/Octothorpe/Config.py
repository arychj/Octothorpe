import xml.etree.ElementTree as ET

class Config():
    _configfile = None
    _config = None

    @classmethod
    def SetConfigFile(cls, f):
        cls._configfile = f

    @classmethod
    def GetString(cls, key):
        if(cls._config == None):
            cls.LoadConfig()

        return cls._config.find(key).text

    @classmethod
    def GetInt(cls, key):
        val = cls.GetString(key)

        if(val != None):
            val = int(val)

        return val

    @classmethod
    def GetBool(cls, key):
        val = cls.GetString(key)

        if(val != None):
            val = bool(val)

        return val

    @classmethod
    def LoadConfig(cls):
        if(cls._configfile == None):
            raise Exception("no config file specified.")
        else:
            with open(cls._configfile) as _configfile:
                tree = ET.parse(_configfile)
                cls._config = tree.getroot()
