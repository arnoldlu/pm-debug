import visa
import time
import datetime
import numpy
import pandas as pd

duration = 50
data_array = []

rm = visa.ResourceManager()
res = rm.list_resources()
print "Find following resources: ", res
print("Opening " + res[-1])

inst = rm.open_resource(res[-1])
#The following command is implicity after poweron.
#inst.write("*RST")
#inst.write("*CLS")
#inst.write("STAT:PRES")
#inst.write("*SRE 0")
#inst.write("*ESE")


#Set the power supply output
inst.write("INST P6V") # Select +6V output
inst.write("VOLT 4.0") # Set output voltage to 4.0 V
inst.write("CURR 2.0") # Set output current to 2.0 A

# Power off then power on, delay 1 second for stable
inst.write("OUTP OFF")
inst.write("OUTP ON")
time.sleep(1) #Add a delay , wait for stable output

inst.timeout = 6000
#Sample count
#inst.write('SENS:SWE:TINT 15.6E-6')
#inst.write('SENS:SWE:TINT 1E-3')
inst.write('SENS:SWE:POIN 60')

# Check if device avaiable
measure_start = time.time()
inst.query("*IDN?")
measure_end = time.time()
#print 'Duration of IDN query:', str((measure_end-measure_start)*1000), 'ms'

measure_start = time.time()
while True:
	start = (time.time() - measure_start)*1000
	if start > duration*1000:
		break
	current = inst.query_ascii_values('MEAS:ARR:CURR?', container=numpy.array)[0]*1000
	data_array.append({'start':start, 'current':current})
measure_end = time.time()
print 'Measurement(%d) ending: %.6f s' % (len(data_array), (measure_end-measure_start))

inst.write("OUTP OFF")