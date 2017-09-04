import time
import serial
import serial.tools.list_ports


def serial_fd_get():
	plist = list(serial.tools.list_ports.comports())

	if len(plist) <= 0:
		print "The Serial port can't find!"
	else:
		for i in range(len(plist)):
			serialName = list(plist[i])[0]
			serialDescription = list(plist[i])[1]
			serialHwid = list(plist[i])[2]
			print serialDescription
			if 'Silicon Labs CP210x USB to UART Bridge' in serialDescription:
				serialFd = serial.Serial(serialName,115200,timeout = 20)
				print "check which port was really used >",serialFd.name, serialDescription, serialHwid
				isOpen = serialFd.isOpen()
				if isOpen:
					return serialFd
	return False

trace_events = []

trace_events += ['/power/machine_suspend']

trace_events += ['/irq/irq_handler_entry', '/irq/irq_handler_exit']

trace_events += ['/power/wakeup_source_activate', '/power/wakeup_source_deactivate']

trace_events += ['/power/cpu_idle']

trace_events += ['/power/cpu_frequency']
			
serialFd = serial_fd_get()
while serialFd == False:
	print 'Please connect serial cable.'
	serialFd = serial_fd_get()
#Turn off tracing
result = serialFd.write('echo 0 >/sys/kernel/debug/tracing/tracing_on\n')
#Disable all traceevents
result = serialFd.write('echo 0 >/sys/kernel/debug/tracing/events/enable\n')
#Clear trace buffer
result = serialFd.write('echo > /sys/kernel/debug/tracing/trace\n')

#Enable power related trace events
for i in trace_events:
	result = serialFd.write('echo 1 >/sys/kernel/debug/tracing/events'+i+'/enable\n')

#Set tracing buffer size
result = serialFd.write('echo 4096 >/sys/kernel/debug/tracing/buffer_size_kb\n')

#Move filter function to filter.sh for temp
result = serialFd.write('echo 0 >/sys/kernel/debug/tracing/events/power/wakeup_source_activate/filter\n')
result = serialFd.write('echo 0 >/sys/kernel/debug/tracing/events/power/wakeup_source_deactivate/filter\n')
result = serialFd.write('echo \"((name!=nand))\" > /sys/kernel/debug/tracing/events/power/wakeup_source_activate/filter\n')
result = serialFd.write('echo \"((name!=nand))\" > /sys/kernel/debug/tracing/events/power/wakeup_source_deactivate/filter\n')

result = serialFd.write('echo 0 >/sys/kernel/debug/tracing/events/irq/irq_handler_entry/filter\n')
result = serialFd.write('echo 0 >/sys/kernel/debug/tracing/events/irq/irq_handler_exit/filter\n')
result = serialFd.write('echo \"((irq!=47)&&(irq!=87)&&(irq!=108))\" >/sys/kernel/debug/tracing/events/irq/irq_handler_entry/filter\n')
result = serialFd.write('echo \"((irq!=47)&&(irq!=87)&&(irq!=108))\" >/sys/kernel/debug/tracing/events/irq/irq_handler_exit/filter\n')

#Turn on tracing
result = serialFd.write('echo 1 >/sys/kernel/debug/tracing/tracing_on\n')

#Duration of capture trace
time.sleep(50)

result = serialFd.write('cat /sys/kernel/debug/tracing/buffer_size_kb\n')
serialFd.readline()
serialFd.readline()

#Disable all traceevents
result = serialFd.write('echo 0 >/sys/kernel/debug/tracing/events/enable\n')

#Save trace evnts
result = serialFd.write('cat /sys/kernel/debug/tracing/trace > /trace.txt\n')
time.sleep(5) #This is a MUST BE, or there is no time to finish the executing.

serialFd.close()
serialFd.isOpen()