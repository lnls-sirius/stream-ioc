#!/opt/epics-R3.15.5/modules/StreamDevice-2.7.11/bin/linux-arm/streamApp

# con-bbb-1.cmd

# This script is being used for the Berthold LB 6420 probe of LNLS Radiation Protection Group (RAD)

# Environment variables

epicsEnvSet("STREAMDEVICE", "/opt/epics-R3.15.5/modules/StreamDevice-2.7.11")
epicsEnvSet("IOC", "/root/streamdevice-ioc")
epicsEnvSet("STREAM_PROTOCOL_PATH", "$(IOC)/protocol")

# Database definition file

cd ${STREAMDEVICE}
dbLoadDatabase("dbd/streamApp.dbd")
streamApp_registerRecordDeviceDriver(pdbbase)

# Port for the Berthold LB 6420 probe

drvAsynIPPortConfigure("IPPort1", "127.0.0.1:17000 UDP")

# Records of the Berthold LB 6420 probe

cd ${IOC}
dbLoadRecords("database/Berthold-LB6420.db", "PORT = IPPort1, PREFIX = RAD:Berthold")

# Effectively initializes the IOC

cd iocBoot
iocInit
