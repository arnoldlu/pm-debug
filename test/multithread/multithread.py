import random
import time
import os
 
from threading import Thread
 
class MyThread(Thread):
	"""
	A threading example
	"""

	#----------------------------------------------------------------------
	def __init__(self, name):
		"""Initialize the thread"""
		Thread.__init__(self)
		self.name = name
		self.duration = 20
		self.start()
 
    #----------------------------------------------------------------------
	def run(self):
		"""Run the thread"""

		time.sleep(random.uniform(10, 20))
		print self.name
 
#----------------------------------------------------------------------
def create_threads():
    """
    Create a group of threads
    """
    name = "Thread trace"
    for i in range(5):
        MyThread(name=name+str(i))
 
if __name__ == "__main__":
    create_threads()
