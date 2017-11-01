#!../bin/linux-arm/streamApp

# UVX-Agilent-4UHV.cmd

# This script in being used for new Agilent 4UHV installations in UVX.

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

# RS-485 serial interface (38400 bps)

drvAsynSerialPortConfigure("serialPort1", "/dev/ttyUSB0")
asynSetOption("serialPort1", 0, "baud", "38400")

# Records corresponding to the second Agilet 4UHV device installed in UVX

dbLoadRecords("database/Agilent-4UHV-Device.db", "PORT = serialPort1, PREFIX = VAC:AgilentController2, SERIAL_ADDRESS = 129")

# Records corresponding to UVX parameter F-ABI09F

dbLoadRecords("database/Agilent-4UHV-Channel.db", "CHANNEL_NUMBER = 1, PORT = serialPort1, PREFIX = VAC:F-ABI09F, SERIAL_ADDRESS = 129")

# Effectively initializes the IOC

cd iocBoot
iocInit
