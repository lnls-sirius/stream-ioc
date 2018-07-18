#!/opt/epics-R3.15.5/modules/StreamDevice-2.7.11/bin/linux-arm/streamApp

# RAD2.cmd

# This script is being used for the probes connected to the new Thermo Fisher Scientific FHT 6020
# controller of LNLS Radiation Protection Group (RAD).

# Environment variables

#epicsEnvSet("EPICS_CAS_INTF_ADDR_LIST", "10.0.38.24") 

epicsEnvSet("STREAM_IOC", "/root/stream-ioc")
epicsEnvSet("EPICS_BASE", "/opt/epics-R3.15.5/base")
epicsEnvSet("ASYN", "/opt/epics-R3.15.5/modules/asyn4-33")
epicsEnvSet("TOP", "/opt/epics-R3.15.5/modules/StreamDevice-2.7.11")
epicsEnvSet("ARCH", "linux-arm")
epicsEnvSet("STREAM_PROTOCOL_PATH", "/root/stream-ioc/protocol")

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

cd ${STREAM_IOC}
dbLoadRecords("database/Thermo-FHT6020.db", "PORT = serialPort1, PREFIX = RAD:THERMO")

# Effectively initializes the IOC

cd iocBoot
iocInit

