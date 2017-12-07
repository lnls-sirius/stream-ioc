#!../bin/linux-arm/streamApp

# PRO.cmd

# This script is being used for temperature and humidity measurements at a room of LNLS Mechanical
# Designs Group (PRO).

# Environment variables

epicsEnvSet("EPICS_BASE", "/opt/base-3.15.5")
epicsEnvSet("ASYN", "/opt/asyn4-32")
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

# Port for the DCM SE-10 device

drvAsynIPPortConfigure("IPPort1", "127.0.0.1:17001 UDP")

# Records corresponding to the eight temperature measurements given by the MBTemp board

dbLoadRecords("database/MBTemp-Channel.db", "RECORD_NAME = PRO:MBTemp:Ch1, SCAN_RATE = 2 second, MBTEMP_ADDRESS = 1, CHANNEL = 0, DESCRIPTION = MBTemp Channel 1, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Channel.db", "RECORD_NAME = PRO:MBTemp:Ch2, SCAN_RATE = 2 second, MBTEMP_ADDRESS = 1, CHANNEL = 1, DESCRIPTION = MBTemp Channel 2, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Channel.db", "RECORD_NAME = PRO:MBTemp:Ch3, SCAN_RATE = 2 second, MBTEMP_ADDRESS = 1, CHANNEL = 2, DESCRIPTION = MBTemp Channel 3, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Channel.db", "RECORD_NAME = PRO:MBTemp:Ch4, SCAN_RATE = 2 second, MBTEMP_ADDRESS = 1, CHANNEL = 3, DESCRIPTION = MBTemp Channel 4, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Channel.db", "RECORD_NAME = PRO:MBTemp:Ch5, SCAN_RATE = 2 second, MBTEMP_ADDRESS = 1, CHANNEL = 4, DESCRIPTION = MBTemp Channel 5, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Channel.db", "RECORD_NAME = PRO:MBTemp:Ch6, SCAN_RATE = 2 second, MBTEMP_ADDRESS = 1, CHANNEL = 5, DESCRIPTION = MBTemp Channel 6, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Channel.db", "RECORD_NAME = PRO:MBTemp:Ch7, SCAN_RATE = 2 second, MBTEMP_ADDRESS = 1, CHANNEL = 6, DESCRIPTION = MBTemp Channel 7, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Channel.db", "RECORD_NAME = PRO:MBTemp:Ch8, SCAN_RATE = 2 second, MBTEMP_ADDRESS = 1, CHANNEL = 7, DESCRIPTION = MBTemp Channel 8, PORT = serialPort1")

# Records of the DCM SE-10 device

dbLoadRecords("database/DCM-SE10.db", "PORT = IPPort1, PREFIX = PRO:DCM_SE-10, SCAN_RATE = 2 second")

# Effectively initializes the IOC

cd iocBoot
iocInit
