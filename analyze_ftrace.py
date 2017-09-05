#!/usr/bin/python

import sys
import time
import os
import string
import re
import platform
import shutil
import csv
from datetime import datetime, timedelta
from subprocess import call, Popen, PIPE

# ----------------- CLASSES --------------------

# Class: SystemValues
# Description:
#	 A global, single-instance container used to
#	 store system values and test parameters
class SystemValues():
	version = '2.1a'
	hostname = 'localhost'
	testtime = ''
	ftracefile = ''
	embedded = False
	timeformat = '%.6f'

	#Output data to csv files
	csv_output_enable = False

	trace_resume = True
	csv_resume = 'resume.csv'
	first_resume = 0.0
	trace_wakeup_source = True
	csv_wakeup = 'wakeup.csv'
	trace_wakelock = True
	trace_cpuidle = True
	csv_cpuidle = 'cpuidle.csv'
	trace_cpufreq = True
	csv_cpufreq = 'cpufreq.csv'
	trace_irq = True
	csv_irq = 'irq.csv'
	
	kernel_suspend = False
	kernel_resume = False
	def __init__(self):
		if('LOG_FILE' in os.environ and 'TEST_RESULTS_IDENTIFIER' in os.environ):
			self.embedded = True
			self.outfile = os.environ['LOG_FILE']
			self.htmlfile = os.environ['LOG_FILE']
		self.hostname = platform.node()
		self.testtime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
		self.testdir = datetime.now().strftime('boot-%y%m%d-%H%M%S')

sysvals = SystemValues()

# Class: Data
# Description:
#	 The primary container for test data.
class Data():
	valid = False
	start = 0.0
	end = 0.0
	power_state = False
	last_resume = 0.0
	suspend_valid = False
	boottime = ''
	phases = ['boot']
	do_one_initcall = False
	def __init__(self, num):
		self.run = []
		self.irq = []
		self.wakesource = []
		self.cpuidle = []
		self.cpufreq = []

# Function: parseFtraceLog
# Description:
#	 parse a ftrace log for power analysis
def parseFtraceLog():
	data = Data(0)
	sysvals.stamp = {
		'time': datetime.now().strftime('%B %d %Y, %I:%M:%S %p'),
		'host': sysvals.hostname,
		'mode': 'boot', 'kernel': ''}

	devtemp = dict()
	irq_name = dict()

	if(sysvals.ftracefile):
		lf = open(sysvals.ftracefile, 'r')
	else:
		lf = Popen('dmesg', stdout=PIPE).stdout

	suspend_resume_list = []
	
	for line in lf:
		line = line.replace('\r\n', '')
		line = line.replace('\n', '')

		ftrace_line_fmt = \
		' *(?P<proc>.*)-(?P<pid>[0-9]*) *\[(?P<cpu>[0-9]*)\] *'+\
		'(?P<flags>.{4}) *(?P<ktime>[0-9\.]*): *'+\
		'(?P<msg>.*)'
		m = re.match(ftrace_line_fmt, line)
		if(not m):
			continue
			
		proc = m.group('proc')
		pid = m.group('pid')
		cpu = m.group('cpu')
		flags = m.group('flags')
		ktime = float('%.6f' % float(m.group('ktime')))
		msg = m.group('msg')
		if data.start == 0.0:
			data.start = ktime

	#Suspend resume processing
		if(sysvals.trace_resume):
			if sysvals.first_resume == 0.0:
				sysvals.first_resume = ktime
				
			m = re.match('^machine_suspend: state=(?P<state>[0-9]*)', msg)
			if(m):
				state = int(m.group('state'))
				r = 0
				if state < 4:
					if state == 3:
						suspend_state = 'MEM'
					else:
						suspend_state = 'MEM'
					t = ktime - data.last_resume
					suspend_resume_list.append({'resume':data.last_resume, 'suspend':ktime, 'duration': float('%.3f' % (t*1000)), 'state':suspend_state})
					data.power_state = False
				else:
					data.last_resume = ktime
					data.power_state = True

	#Wakeup source processing
		if (sysvals.trace_wakeup_source):

			m = re.match('^wakeup_source_activate: *(?P<f>.*) .*', msg)
			if(m):
				devtemp[m.group('f')] = ktime
				continue

			m = re.match('^wakeup_source_deactivate: *(?P<f>.*) .*', msg)
			if(m):
				data.valid = True
				f = m.group('f')
				r = 0
				if(f in devtemp):
					t = ktime - devtemp[m.group('f')]
					data.wakesource.append({'name': f, 'start': devtemp[m.group('f')]*1000, 'duration': float('%.3f' % (t*1000)), 'process': proc+'-'+pid})
					del devtemp[f]
				continue
	


		#Cpuidle start/end processing
		if (sysvals.trace_cpuidle):
			m = re.match('^cpu_idle: state=(?P<state>[0-9]*) *cpu_id=(?P<f>.*)', msg)
			if(m):
				state = int(m.group('state'))
				if state < 2:
					if state == 0:
						idle_state = 'WFI'
					elif state == 1:
						idle_state = 'OFF'
					devtemp[m.group('f')] = ktime
					#print (m.group('f'), idle_state, 'start')
					continue
				else:
					data.valid = True
					f = m.group('f')
					r = 0
					if(f in devtemp):
						t = ktime - devtemp[m.group('f')]
						data.cpuidle.append({'state': idle_state, 'start': devtemp[f]*1000, 'duration': float('%.3f' % (t*1000)), 'cpu': int(cpu)})
						del devtemp[f]
					continue

	#cpufreq processing
		if (sysvals.trace_cpufreq):
			m = re.match('^cpu_frequency: state=(?P<freq>[0-9]*) *cpu_id=(?P<f>.*)', msg)
			if(m):
				r = 0
				t = 0.01
				f = m.group('f')
				freq = int(m.group('freq'))
				data.cpufreq.append({'freq': freq, 'start': ktime*1000, 'cpu': f})

	#irq processing
		if (sysvals.trace_irq):
			m = re.match('^irq_handler_entry: irq=(?P<irq_no>[0-9]*) *name=(?P<irq>.*)', msg)
			if(m):
				devtemp[m.group('irq_no')] = ktime
				irq_name[m.group('irq_no')] = m.group('irq')
				continue

			m = re.match('^irq_handler_exit: irq=(?P<irq_no>[0-9]*) *ret=(?P<result>.*)', msg)
			if(m):
				data.valid = True
				irq_no = m.group('irq_no')
				r = 0
				if(irq_no in devtemp):
					t = ktime - devtemp[m.group('irq_no')]
					data.irq.append({'irq': irq_no, 'name':irq_name[m.group('irq_no')], 'start': devtemp[irq_no]*1000, 'duration': float('%.3f' % (t*1000)), 'process': proc+'-'+pid})
					del devtemp[irq_no]
				continue
	data.start *= 1000.0
	data.end = ktime*1000.0
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	for name in devtemp:
		data.wakesource.append({'name': name, 'start': devtemp[name]*1000, 'duration': data.end-devtemp[name]*1000, 'process': ''})

	if data.power_state and data.last_resume != 0.0:
		suspend_resume_list.append({'resume':data.last_resume, 'suspend':data.end/1000, 'duration':int(data.end - data.last_resume*1000), 'state':suspend_state, })
	for suspend_resume in suspend_resume_list:
		if suspend_resume['resume'] == 0.0:
			suspend_resume['resume'] = data.start/1000
			suspend_resume['duration'] = (suspend_resume['suspend'] - suspend_resume['resume'])*1000
		data.run.append({'start': suspend_resume['resume']*1000, 'duration': suspend_resume['duration']})

	if sysvals.csv_output_enable:
		#Suspend-Resume related local variable
		csv_file_resume = open(sysvals.csv_resume, 'wb')
		csv_writer_resume = csv.writer(csv_file_resume)
		csv_writer_resume.writerow(['start(ms)', 'duration(ms)'])
		for i in data.run:
			csv_writer_resume.writerow([i['start'], i['duration']])

		#irq related local variable
		csv_file_irq = open(sysvals.csv_irq, 'wb')
		csv_writer_irq = csv.writer(csv_file_irq)
		csv_writer_irq.writerow(['irq', 'name', 'start(ms)', 'duration(ms)', 'process'])
		for i in data.irq:
			csv_writer_irq.writerow([i['irq'], i['name'], i['start'], i['duration'], i['process']])
		
		#wakeup local variable
		csv_file_wakeup = open(sysvals.csv_wakeup, 'wb')
		csv_writer_wakeup = csv.writer(csv_file_wakeup)
		csv_writer_wakeup.writerow(['name', 'start(ms)', 'duration(ms)', 'process'])
		for i in data.wakesource:
			csv_writer_wakeup.writerow([i['name'], i['start'], i['duration'], i['process']])
			
		#cpudile related local variable
		csv_file_cpuidle = open(sysvals.csv_cpuidle, 'wb')
		csv_writer_cpuidle = csv.writer(csv_file_cpuidle)
		csv_writer_cpuidle.writerow(['state','start(ms)', 'duration(ms)', 'cpu'])
		for i in data.cpuidle:
			csv_writer_cpuidle.writerow([i['state'],i['start'], i['duration'], i['cpu']])


		#cpufreq related local variable
		csv_file_cpufreq = open(sysvals.csv_cpufreq, 'wb')
		csv_writer_cpufreq = csv.writer(csv_file_cpufreq)
		csv_writer_cpufreq.writerow(['freq', 'start(ms)', 'cpu'])
		for i in data.cpufreq:
			csv_writer_cpufreq.writerow([i['freq'], i['start'], i['cpu']])

		csv_file_cpuidle.close()
		csv_file_irq.close()
		csv_file_cpufreq.close()
		csv_file_resume.close()
		csv_file_wakeup.close()
	
	del irq_name
	
	lf.close()
	return data



# Function: doError Description:
#	 generic error function for catastrphic failures
# Arguments:
#	 msg: the error message to print
#	 help: True if printHelp should be called after, False otherwise
def doError(msg, help=False):
	if help == True:
		printHelp()
	print 'ERROR: %s\n' % msg
	sys.exit()

# Function: printHelp
# Description:
#	 print out the help text
def printHelp():
	print('')
	print('Usage: bootgraph <options> <command>')
	print('')
	print('Description:')
	print('  This tool reads in a dmesg log of linux kernel boot and')
	print('  creates an html representation of the boot timeline up to')
	print('  the start of the init process.')
	print('Options:')
	print('  -h            Print this help text')
	print('  -v            Print the current tool version')
	print('  -ftrace file  Load a stored ftrace file (used with -dmesg)')
	print('')
	return True

# ----------------- MAIN --------------------
# exec start (skipped if script is loaded as library)
if __name__ == '__main__':
	# loop through the command line arguments
	cmd = ''
	testrun = True
	simplecmds = ['-updategrub', '-flistall']
	args = iter(sys.argv[1:])
	for arg in args:
		if(arg == '-h'):
			printHelp()
			sys.exit()
		elif(arg == '-v'):
			print("Version %s" % sysvals.version)
			sys.exit()
		elif(arg == '-ftrace'):
			try:
				val = args.next()
			except:
				doError('No ftrace file supplied', True)
			testrun = False
			sysvals.ftracefile = val
		else:
			doError('Invalid argument: '+arg, True)

	# process the log data
	if sysvals.ftracefile:
		data = parseFtraceLog()
	else:
		doError('ftrace file required')

	print('          Host: %s' % sysvals.hostname)
	print('     Test time: %s' % sysvals.testtime)
	print(' Measure start: %.3f' % (data.start))
	print('   Measure end: %.3f' % (data.end))