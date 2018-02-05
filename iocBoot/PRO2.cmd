#!../bin/linux-arm/streamApp

# PRO2.cmd

# This script is being used for temperature measurements of a machine of LNLS Mechanical Designs
# Group (PRO).

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

# RS-485 serial interface for the MBTemp board (115200 bps)

drvAsynSerialPortConfigure("serialPort1", "/dev/ttyUSB0")
asynSetOption("serialPort1", 0, "baud", "115200")

# Record for configuration of MBTemp exponential moving average smoothing factor

dbLoadRecords("database/MBTemp-Device.db", "MBTEMP_ADDRESS = 1, PORT = serialPort1, PREFIX = PRO:MBTemp2")

# Records corresponding to the eight temperature measurements given by the MBTemp board

dbLoadRecords("database/MBTemp-Channel.db", "CHANNEL = 0, DESCRIPTION = MBTemp Channel 1, MBTEMP_ADDRESS = 1, PORT = serialPort1, RECORD_NAME = PRO:MBTemp2:Ch1, SCAN_RATE = 2 second")
dbLoadRecords("database/MBTemp-Channel.db", "CHANNEL = 1, DESCRIPTION = MBTemp Channel 2, MBTEMP_ADDRESS = 1, PORT = serialPort1, RECORD_NAME = PRO:MBTemp2:Ch2, SCAN_RATE = 2 second")
dbLoadRecords("database/MBTemp-Channel.db", "CHANNEL = 2, DESCRIPTION = MBTemp Channel 3, MBTEMP_ADDRESS = 1, PORT = serialPort1, RECORD_NAME = PRO:MBTemp2:Ch3, SCAN_RATE = 2 second")
dbLoadRecords("database/MBTemp-Channel.db", "CHANNEL = 3, DESCRIPTION = MBTemp Channel 4, MBTEMP_ADDRESS = 1, PORT = serialPort1, RECORD_NAME = PRO:MBTemp2:Ch4, SCAN_RATE = 2 second")
dbLoadRecords("database/MBTemp-Channel.db", "CHANNEL = 4, DESCRIPTION = MBTemp Channel 5, MBTEMP_ADDRESS = 1, PORT = serialPort1, RECORD_NAME = PRO:MBTemp2:Ch5, SCAN_RATE = 2 second")
dbLoadRecords("database/MBTemp-Channel.db", "CHANNEL = 5, DESCRIPTION = MBTemp Channel 6, MBTEMP_ADDRESS = 1, PORT = serialPort1, RECORD_NAME = PRO:MBTemp2:Ch6, SCAN_RATE = 2 second")
dbLoadRecords("database/MBTemp-Channel.db", "CHANNEL = 6, DESCRIPTION = MBTemp Channel 7, MBTEMP_ADDRESS = 1, PORT = serialPort1, RECORD_NAME = PRO:MBTemp2:Ch7, SCAN_RATE = 2 second")
dbLoadRecords("database/MBTemp-Channel.db", "CHANNEL = 7, DESCRIPTION = MBTemp Channel 8, MBTEMP_ADDRESS = 1, PORT = serialPort1, RECORD_NAME = PRO:MBTemp2:Ch8, SCAN_RATE = 2 second")

# Effectively initializes the IOC

cd iocBoot
iocInit
