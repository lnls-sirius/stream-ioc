#!../bin/linux-arm/streamApp
###!/opt/epics-R3.15.5/modules/StreamDevice-2.7.11/bin/linux-x86_64/streamApp

# VBC.cmd
# This script is being used for controlling the vacuum nitrogen insertion system
#=============================================================================
# Environment variables
#=============================================================================
#epicsEnvSet "EPICS_CA_SERVER_PORT", "5064"
#epicsEnvSet("EPICS_BASE", "/opt/epics-R3.15.5/base")
#epicsEnvSet("TOP", "/home/lnls-136/rafael/RAFAEL/git_CNPEM/stream-ioc")
#epicsEnvSet("TOP", "/opt/epics-R3.15.5/modules/StreamDevice-2.7.11")
#epicsEnvSet("ARCH", "linux-x86_64")
#epicsEnvSet ("STREAM_PROTOCOL_PATH", "/home/lnls-136/rafael/RAFAEL/git_CNPEM/stream-ioc/protocol")

epicsEnvSet "EPICS_CA_SERVER_PORT", "5064"
epicsEnvSet("EPICS_BASE", "/opt/base-3.15.5")
epicsEnvSet("ASYN", "/opt/asyn4-33")
epicsEnvSet("TOP", "/root/stream-ioc")
epicsEnvSet("ARCH", "linux-arm")
epicsEnvSet ("STREAM_PROTOCOL_PATH", "$(TOP)/protocol")
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
#cd /home/lnls-136/rafael/RAFAEL/git_CNPEM/stream-ioc
cd ${TOP}
dbLoadRecords("database/VBC-ACP.db", "ADDRESS = 0, PORT = socket_vbc, SCAN_RATE = 1 second, PREFIX = VBC:ACP")
dbLoadRecords("database/VBC-TURBOVAC.db", "ADDRESS = 0, PORT = socket_vbc, SCAN_RATE = 1 second, PREFIX = VBC:TURBOVAC")
dbLoadRecords("database/VBC-BBB.db", "ADDRESS = 0, PORT = socket_vbc, SCAN_RATE = 1 second, PREFIX = VBC:BBB")
#=============================================================================
# Effectively initializes the IOC
cd iocBoot
iocInit
