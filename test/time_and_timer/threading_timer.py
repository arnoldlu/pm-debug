#!/usr/bin/python
import time
import datetime
import threading

threading_expires = 0.001
threading_count = 0
threading_max = 1000

def threading_func(timer_start):
    global threading_count

    #now = datetime.datetime.utcnow()
    #print 'count-', threading_count, 'duration-', (now - start).total_seconds(), 'expire-', (now - timer_start).total_seconds()
    threading_count += 1
    if threading_count < threading_max:
        threading.Timer(threading_expires, threading_func, (datetime.datetime.utcnow(),)).start()
    else:
	end = datetime.datetime.utcnow()

        print 'Threading total=', (end -start).total_seconds(), 'Expires=', threading_expires, 'Count=', threading_max
 

start = datetime.datetime.utcnow()
threading.Timer(threading_expires, threading_func, (datetime.datetime.utcnow(),)).start()
