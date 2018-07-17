#!/opt/epics-R3.15.5/modules/StreamDevice-2.7.11/bin/linux-arm/streamApp

# RAD3.cmd

# This script is being used for the new ELSE Nuclear probes of LNLS Radiation Protection Group
# (RAD).

# Environment variables

epicsEnvSet("EPICS_CAS_INTF_ADDR_LIST", "10.0.38.23")

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

# Port for the ELSE probes

drvAsynIPPortConfigure("IPPort1", "192.168.0.100:10001")
drvAsynIPPortConfigure("IPPort2", "192.168.0.200:10001")

# Records of the ELSE probe

cd ${STREAM_IOC}
dbLoadRecords("database/ELSE-SATURN5702.db", "PORT1 = IPPort1, PORT2 = IPPort2, PREFIX = RAD:ELSE")
 
# Effectively initializes the IOC
cd iocBoot
iocInit
