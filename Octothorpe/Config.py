import xml.etree.ElementTree as ET

class Config():
    config = None

    @classmethod
    def GetString(cls, key):
        if(cls.config == None):
            cls.LoadConfig()

        return cls.config.find(key).text

    @classmethod
    def GetInt(cls, key):
        val = cls.GetString(key)

        if(val != None):
            val = int(val)

        return val

    @classmethod
    def LoadConfig(cls):
        with open("config.xml") as configfile:
            tree = ET.parse(configfile)
            cls.config = tree.getroot()
