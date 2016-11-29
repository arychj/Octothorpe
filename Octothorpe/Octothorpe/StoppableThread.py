from abc import ABCMeta, abstractmethod
from threading import Thread
import time

from .Log import Log

class StoppableThread(Thread, metaclass=ABCMeta):
    _master_running = True
    _active_threads = {}

    @property
    @abstractmethod
    def Group(self):
        pass

    @property
    @abstractmethod
    def Name(self):
        pass

    @property
    def Running(self):
        return self._running

    @property
    def Interval(self):
        return 1

    def __init__(self, is_daemon=False):
        Thread.__init__(self)

        self._running = True
        self.daemon = is_daemon

        StoppableThread._track(self)

        self.start()

    @abstractmethod
    def Run(self):
        pass

    def Stop(self):
        self._running = False

    def run(self):
        while StoppableThread._master_running and self.Running:
            self.Run()

            if(self.Interval)
                time.sleep(self.Interval)

    @staticmethod
    def StopThread(group=None, name=None):
        if(group and name):
            StoppableThread._active_threads[group][name].Stop()
        elif(group):
            Log.Debug(f"Stopping thread group {group}...")
            for thread in StoppableThread._active_threads[group]:
                thread.Stop()
        else:
            raise Exception("Thread group or group/name must be specified")

    @staticmethod
    def StopAll():
        StoppableThread._running = False
        time.sleep(1)

        for group in StoppableThread._active_threads:
            StoppableThread.StopThread(group=group)

    @staticmethod
    def _track(thread):
        if(group not in StoppableThread._active_threads)
            StoppableThread._active_threads[Thread.Group] = {}

        StoppableThread._active_threads[Thread.Group][Thread.Name] = thread
        