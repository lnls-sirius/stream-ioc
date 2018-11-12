#!/opt/epics-R3.15.5/modules/StreamDevice-2.7.11/bin/linux-arm/streamApp

# VBC.cmd
# This script is being used for controlling the vacuum nitrogen insertion system
#=============================================================================
# Environment variables
#=============================================================================
epicsEnvSet("EPICS_CA_SERVER_PORT", "5064")
epicsEnvSet("EPICS_BASE", "/opt/epics-R3.15.5/base")
epicsEnvSet("ASYN", "/opt/epics-R3.15.5/modules/asyn4-33")
epicsEnvSet("TOP", "/opt/epics-R3.15.5/modules/StreamDevice-2.7.11")
epicsEnvSet("ARCH", "linux-arm")
epicsEnvSet("STREAM_PROTOCOL_PATH", "/root/stream-ioc/protocol")
#=============================================================================
# Database definition file
#=============================================================================
cd ${TOP}
dbLoadDatabase("dbd/streamApp.dbd")
streamApp_registerRecordDeviceDriver(pdbbase)
#=============================================================================
# Unix Socket used to communicate with BBB for valves controls
#=============================================================================
drvAsynIPPortConfigure("socket_vbc", "unix:///tmp/socket_vbc")
#=============================================================================
# Records for BBB, ACP15 and TURBOVAC pumps
#=============================================================================
cd /root/stream-ioc
dbLoadRecords("database/VBC-ACP.db", "PORT = socket_vbc, SCAN_RATE = 1 second, PREFIX = VBC1:ACP")
dbLoadRecords("database/VBC-TURBOVAC.db", "PORT = socket_vbc, SCAN_RATE = 1 second, PREFIX = VBC1:TURBOVAC")
dbLoadRecords("database/VBC-BBB.db", "PORT = socket_vbc, SCAN_RATE = 1 second, PREFIX = VBC1:BBB")
dbLoadRecords("database/VBC-SYSTEM.db", "PORT = socket_vbc, SCAN_RATE = 1 second, PREFIX = VBC1:SYSTEM")
#=============================================================================
# Effectively initializes the IOC
cd iocBoot
iocInit
