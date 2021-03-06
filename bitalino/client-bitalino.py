import sys; sys.path.append('lib') # help python find pylsl relative to this example program
# simulate BioSemi a 4 channels EEG at 100hz
from pylsl import StreamInfo, StreamOutlet, local_clock
from scipy import *
import random
import time
import timeit
from bitalino import BITalino


macAddress = "98:D3:31:B2:12:01"
#macAddress = "98:D3:31:70:3D:CE"
batteryThreshold = 30
acqChannels = [0,1,2,3,4,5]
defaultChannel=4;
samplingRate = 100
nSamples = 1
digitalOutput = [1,1,0,0]
# Connect to BITalino
connection=0
while connection is 0:
	try:
		print "connecting to BITalino(%s)..." %macAddress
		device = BITalino(macAddress)
		connection=1;
		break
	except TypeError:
		print "MAC address (%s) is not defined..." %macAddress
		print "connecting to BITalino(%s)..." 
	except ValueError:
		print "MAC address (%s) is not defined..." %macAddress
		print "connecting to BITalino(%s)..." 
	
# Set battery threshold
device.battery(batteryThreshold)
# Read BITalino version
print device.version()
print "connected to BITalino(%s)" %macAddress
print "creating Signal stream..."
info = StreamInfo('BiTalino','BiTalino',+len(acqChannels),samplingRate,'float32','myuid34234');
# next make an outlet
outlet = StreamOutlet(info)
print"created Signal stream : %s" %info.name()
print("starting acquisition...")
# Start Acquisition
device.start(samplingRate, acqChannels)
# Read samples
while 1:
	data=device.read(nSamples)
	print data
 	outlet.push_sample(data[0][defaultChannel+1:])

# Turn BITalino led on
device.trigger(digitalOutput)
# Stop acquisition
device.stop()
# Close connection
outlet.close()
info.close()
device.close()
