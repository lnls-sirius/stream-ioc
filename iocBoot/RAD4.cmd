#!../bin/linux-arm/streamApp

# RAD3.cmd

# This script is being used for the new ELSE Nuclear probes of LNLS Radiation Protection Group
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

# Port for the ELSE probes

drvAsynIPPortConfigure("IPPort1", "127.0.0.1:17002 UDP")

# Records of the ELSE probes

dbLoadRecords("database/ELSE-Probes-tcp.db", "PORT = IPPort1, PREFIX = RAD:ELSE:SATURN")

# Effectively initializes the IOC

cd iocBoot
iocInit
