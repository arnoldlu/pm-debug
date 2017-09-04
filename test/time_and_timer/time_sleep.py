#!/usr/bin/python

import time
import datetime
import sched
import threading

sleep_duration = 0.001
sleep_count = 1000
start = datetime.datetime.utcnow()
for i in range(sleep_count):
    time.sleep(sleep_duration)
#    print i, datetime.datetime.utcnow()
end = datetime.datetime.utcnow()
print 'Time sleep total=', (end - start).total_seconds(), 'Sleep=', sleep_duration, 'Count=', sleep_count
