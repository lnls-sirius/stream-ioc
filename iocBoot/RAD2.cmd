#!../bin/linux-arm/streamApp

# RAD2.cmd

# This script is being used for the probes connected to the new Thermo Fisher Scientific FHT 6020
# controller of LNLS Radiation Protection Group (RAD).

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

# RS-485 serial interface for the Thermo Fisher Scientific FHT 6020 controller

drvAsynSerialPortConfigure("serialPort1", "/dev/ttyUSB0")
asynSetOption("serialPort1", 0, "baud", "19200")
asynSetOption("serialPort1", 0, "bits", "7")
asynSetOption("serialPort1", 0, "parity", "even")
asynSetOption("serialPort1", 0, "stop", "2")

# Records for the two probes connected to the controller

dbLoadRecords("database/Thermo-FHT6020-Channel.db", "ADDRESS = 01, DESCRIPTION = Gamma, FH40G_PORT = 1, PORT = serialPort1, RECORD_NAME = RAD:Thermo:FHT6020:Gamma")
dbLoadRecords("database/Thermo-FHT6020-Channel.db", "ADDRESS = 01, DESCRIPTION = Neutron, FH40G_PORT = 2, PORT = serialPort1, RECORD_NAME = RAD:Thermo:FHT6020:Neutron")

# Effectively initializes the IOC

cd iocBoot
iocInit
