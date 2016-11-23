import datetime, croniter

from ..Injector import Injector
from ..Log import Log

class ScheduleInjector(Injector):
    def Start(self):
        now = datetime.datetime.now()
        sched = '1 15 1,15 * *'
        cron = croniter.croniter(sched, now)
        
        Log.Debug(cron.get_next(datetime.datetime))

    def Stop(self):
        pass

