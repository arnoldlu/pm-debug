import threading, time, random
count = 0
lock = threading.Lock()
def doAdd():
    global count, lock
    lock.acquire()
    print threading.currentThread().getName(), 'start'
    for i in xrange(10000):
        count = count + 1
    lock.release()
    print threading.currentThread().getName(), 'end'
for i in range(5):
    threading.Thread(target = doAdd, args = (), name = 'thread-' + str(i)).start()
time.sleep(2)
print count
