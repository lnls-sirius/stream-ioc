#!../bin/linux-arm/streamApp

# UVX-MBTemp.cmd

# This script will be used for MBTemp installations in UVX.

# Environment variables

epicsEnvSet("EPICS_BASE", "/opt/base-3.14.12.6")
epicsEnvSet("ASYN", "/opt/asyn4-31")
epicsEnvSet("TOP", "/root/stream-ioc")
epicsEnvSet("ARCH", "linux-arm")
epicsEnvSet ("STREAM_PROTOCOL_PATH", "$(TOP)/protocol")

# Database definition file

cd ${TOP}
dbLoadDatabase("dbd/streamApp.dbd")
streamApp_registerRecordDeviceDriver(pdbbase)

# RS-485 serial interface (19200 bps)

drvAsynSerialPortConfigure("serialPort1", "/dev/ttyUSB0")
asynSetOption("serialPort1", 0, "baud", "19200")

# Records corresponding to the eight temperature measurements given by a board at serial address 3

dbLoadRecords("database/MBTemp-Temperature.db", "RECORD_NAME = MBTemp:TAQD09A, SCAN_RATE = .5 second, MBTEMP_ADDRESS = 3, CHANNEL = 0, DESCRIPTION = UVX parameter TAQD09A, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Temperature.db", "RECORD_NAME = MBTemp:TAQF09A, SCAN_RATE = .5 second, MBTEMP_ADDRESS = 3, CHANNEL = 1, DESCRIPTION = UVX parameter TAQF09A, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Temperature.db", "RECORD_NAME = MBTemp:TACV09A, SCAN_RATE = .5 second, MBTEMP_ADDRESS = 3, CHANNEL = 2, DESCRIPTION = UVX parameter TACV09A, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Temperature.db", "RECORD_NAME = MBTemp:TADI08, SCAN_RATE = .5 second, MBTEMP_ADDRESS = 3, CHANNEL = 3, DESCRIPTION = UVX parameter TADI08, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Temperature.db", "RECORD_NAME = MBTemp:TACH08, SCAN_RATE = .5 second, MBTEMP_ADDRESS = 3, CHANNEL = 4, DESCRIPTION = UVX parameter TACH08, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Temperature.db", "RECORD_NAME = MBTemp:TASF08, SCAN_RATE = .5 second, MBTEMP_ADDRESS = 3, CHANNEL = 5, DESCRIPTION = UVX parameter TASF08, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Temperature.db", "RECORD_NAME = MBTemp:HTAA, SCAN_RATE = .5 second, MBTEMP_ADDRESS = 3, CHANNEL = 6, DESCRIPTION = UVX parameter HTAA, PORT = serialPort1")
dbLoadRecords("database/MBTemp-Temperature.db", "RECORD_NAME = MBTemp:HTAB, SCAN_RATE = .5 second, MBTEMP_ADDRESS = 3, CHANNEL = 7, DESCRIPTION = UVX parameter HTAB, PORT = serialPort1")

# Effectively initializes the IOC

cd iocBoot
iocInit
