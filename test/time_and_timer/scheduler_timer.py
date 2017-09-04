#!/usr/bin/python
import time
import datetime
import sched

schedule = sched.scheduler(time.time, time.sleep)
schedule_expires = 0.001
schedule_count = 0 
schedule_max = 1000

def schedule_func(timer_start):
    global schedule_count

    #now = datetime.datetime.utcnow()
    #print 'count-', schedule_count, 'duration-', (now - start).total_seconds(), 'expire-', (now - timer_start).total_seconds()
    schedule_count += 1
    if schedule_count < schedule_max:
        schedule.enter(schedule_expires, 0, schedule_func, (datetime.datetime.utcnow(),))

start = datetime.datetime.utcnow()
schedule.enter(schedule_expires, 0, schedule_func, (datetime.datetime.utcnow(),))
schedule.run()
end = datetime.datetime.utcnow()
print 'Scheduler total=', (end - start).total_seconds(), 'Expire=', schedule_expires, 'Count=', schedule_max
