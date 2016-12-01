from abc import ABCMeta, abstractmethod
from enum import Enum
import time, threading, uuid

class Task(metaclass=ABCMeta):

    @property
    @abstractmethod
    def TaskType(self):
        pass

    @property
    @abstractmethod
    def Priority(self):
        pass

    @property
    def Ident(self):
        if(self._ident == None):
            self._ident = Task._generate_ident()

        return self._ident

    @property
    def ShortIdent(self):
        if(self.Ident == None):
            return None
        else:
            return self.Ident[:8]

    @property
    def Identity(self):
        return f"{self.TaskType}:{self.Id}"

    @property
    def ProcessingTime(self):
        if(self.ProcessingOn == None or self.CompletedOn == None):
            return None
        else:
            return self.CompletedOn - self.ProcessingOn

    @property
    def WaitingTime(self):
        if(self.GivenOn == None or self.ProcessingOn == None):
            return None
        else:
            return self.ProcessingOn - self.GivenOn

    @property
    def IsComplete(self):
        return (self.CompletedOn != None)

    def __init__(self, given_on, processing_on, completed_on, ident = None):
        self.GivenOn = given_on
        self.ProcessingOn = processing_on
        self.CompletedOn = completed_on

        self._ident = ident

        self._lock = threading.Lock()
        if(self.CompletedOn == None):
            self._lock.acquire()

    def __lt__(self, other):
        if(self.TaskType == TaskType.Stop):
            return True
        elif(other.TaskType == TaskType.Stop):
            return False
        else:
            sp = self.Priority
            op = other.Priority

            if(sp == op):
                return self.GivenOn < other.GivenOn
            else:
                return  sp < op

    def WaitUntilComplete(self):
        if(self._lock.locked()):
            self._lock.acquire()
            self._lock.release()
    
    @abstractmethod
    def Process(self):
        pass

    @abstractmethod
    def Save(self):
        pass

    def Processing(self):
        self.ProcessingOn = time.time()

    def Complete(self):
        self.CompletedOn = time.time()
        self.Save()

        self._lock.release()

    def Fail(self):
        self.Complete()

    @staticmethod
    def _generate_ident():
        ident = uuid.uuid4()
        return ident.hex

class StopTask(Task):
    @property
    def TaskType(self):
        return TaskType.Stop
    
    @property
    def Tag(self):
        return "STOP"
    
    @property
    def Priority(self):
        return 0

    def __init__(self):
        super().__init__(None, None, None, None)

    def Process(self):
        pass

    def Save(self):
        pass

class TaskType(Enum):
    Stop = 0
    Instruction = 1
    Event = 2

    def __str__(self):
        return self.name