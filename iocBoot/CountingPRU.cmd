#!../bin/linux-arm/streamApp
# CountingPRU.cmd
# CountingPRU example

# Environment variables

epicsEnvSet("EPICS_BASE", "/root/base-3.15.5")
epicsEnvSet("ASYN", "/root/asyn4-33")
epicsEnvSet("TOP", "/root/stream-ioc")
epicsEnvSet("ARCH", "linux-arm")
epicsEnvSet ("STREAM_PROTOCOL_PATH", "$(TOP)/protocol")

# Database definition file
cd ${TOP}
dbLoadDatabase("dbd/streamApp.dbd")
streamApp_registerRecordDeviceDriver(pdbbase)

# Port for the device
drvAsynIPPortConfigure("IPPort1", "10.0.6.34:5000")

# Record for configuration of TimeBase
dbLoadRecords("database/CountingPRU-Device.db", "PORT = IPPort1, PREFIX = CountingPRU")

# Records corresponding to the eight countings
dbLoadRecords("database/CountingPRU-Channel.db", "CHANNEL = 1, DESCRIPTION = Channel 1, PORT = IPPort1, RECORD_NAME = CountingPRU:Ch1, SCAN_RATE = 2 second")
dbLoadRecords("database/CountingPRU-Channel.db", "CHANNEL = 2, DESCRIPTION = Channel 2, PORT = IPPort1, RECORD_NAME = CountingPRU:Ch2, SCAN_RATE = 2 second")
dbLoadRecords("database/CountingPRU-Channel.db", "CHANNEL = 3, DESCRIPTION = Channel 3, PORT = IPPort1, RECORD_NAME = CountingPRU:Ch3, SCAN_RATE = 2 second")
dbLoadRecords("database/CountingPRU-Channel.db", "CHANNEL = 4, DESCRIPTION = Channel 4, PORT = IPPort1, RECORD_NAME = CountingPRU:Ch4, SCAN_RATE = 2 second")
dbLoadRecords("database/CountingPRU-Channel.db", "CHANNEL = 5, DESCRIPTION = Channel 5, PORT = IPPort1, RECORD_NAME = CountingPRU:Ch5, SCAN_RATE = 2 second")
dbLoadRecords("database/CountingPRU-Channel.db", "CHANNEL = 6, DESCRIPTION = Channel 6, PORT = IPPort1, RECORD_NAME = CountingPRU:Ch6, SCAN_RATE = 2 second")
dbLoadRecords("database/CountingPRU-Channel.db", "CHANNEL = 7, DESCRIPTION = Channel 7, PORT = IPPort1, RECORD_NAME = CountingPRU:Ch7, SCAN_RATE = 2 second")
dbLoadRecords("database/CountingPRU-Channel.db", "CHANNEL = 8, DESCRIPTION = Channel 8, PORT = IPPort1, RECORD_NAME = CountingPRU:Ch8, SCAN_RATE = 2 second")


# Effectively initializes the IOC
cd iocBoot
iocInit
