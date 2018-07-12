#!/opt/epics-R3.15.5/modules/StreamDevice-2.7.11/bin/linux-arm/streamApp

# RAD1.cmd

# This script is being used for the new Berthold LB 6420 probe of LNLS Radiation Protection Group
# (RAD).

# Environment variables

epicsEnvSet ("STREAM_IOC", "/root/stream-ioc")
epicsEnvSet("EPICS_BASE", "/opt/epics-R3.15.5/base")
epicsEnvSet("ASYN", "/opt/epics-R3.15.5/modules/asyn4-33")
epicsEnvSet("TOP", "/opt/epics-R3.15.5/modules/StreamDevice-2.7.11")
epicsEnvSet("ARCH", "linux-arm")
epicsEnvSet ("STREAM_PROTOCOL_PATH", "$(STREAM_IOC)/protocol")

# Database definition file

cd ${TOP}
dbLoadDatabase("dbd/streamApp.dbd")
streamApp_registerRecordDeviceDriver(pdbbase)

# Port for the Berthold LB 6420 probe

drvAsynIPPortConfigure("IPPort1", "127.0.0.1:17001 UDP")

# Records of the Berthold LB 6420 probe

cd ${STREAM_IOC}
dbLoadRecords("database/Berthold-LB6420.db", "PORT = IPPort1, PREFIX = RAD:Berthold")

# Effectively initializes the IOC
cd iocBoot
iocInit


