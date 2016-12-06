import datetime, croniter

from ..Injector import Injector
from ..Log import Log

class Schedule(Injector):
    def _injcetor_start(self):
        now = datetime.datetime.now()
        sched = '1 15 1,15 * *'
        cron = croniter.croniter(sched, now)
        
        Log.Debug(cron.get_next(datetime.datetime))

    def _injector_stop(self):
        pass

