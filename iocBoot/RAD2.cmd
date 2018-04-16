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

# UDP/IP socket for the Thermo Fisher Scientific FHT 6020 controller

drvAsynIPPortConfigure("IPPort1", "127.0.0.1:17002 UDP")

# Records for the two probes connected to the controller

dbLoadRecords("database/Thermo-FHT6020.db", "PORT = IPPort1, PREFIX = RAD:THERMO")

# Effectively initializes the IOC

cd iocBoot
iocInit
