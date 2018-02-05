#!../bin/linux-arm/streamApp

# RAD1.cmd

# This script is being used for the new Berthold LB 6420 probe of LNLS Radiation Protection Group
# (RAD).

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

# Port for the Berthold LB 6420 probe

drvAsynIPPortConfigure("IPPort1", "127.0.0.1:17001 UDP")

# Records of the Berthold LB 6420 probe

dbLoadRecords("database/Berthold-LB6420.db", "PORT = IPPort1, PREFIX = RAD:Berthold")

# Effectively initializes the IOC

cd iocBoot
iocInit
