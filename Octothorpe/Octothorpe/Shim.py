from abc import ABCMeta, abstractmethod

class Shim(metaclass=ABCMeta):

    @abstractmethod
    def Inshimerate(self):
        pass

    @staticmethod
    def Get(name):
        pass
    