import time
from roboclaw import Roboclaw

#Windows comport name
#rc = Roboclaw("COM11",115200)
#Linux comport name
rc = Roboclaw("/dev/ttyTHS2",115200)

rc.Open()

while 1:
	#Get version string
	version = rc.ReadVersion(0x81)
	if version[0]==False:
		print "GETVERSION Failed"
	else:
		print repr(version[1])
	time.sleep(1)
