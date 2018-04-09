#!../../bin/linux-arm/streamApp

# SPIxCONV.cmd

# This script will be used for SPIxCONV installations alongside with EPP hardware and power supplies.

# Environment variables
epicsEnvSet("EPICS_BASE", "/opt/base-3.15.5")
epicsEnvSet("ASYN", "/opt/asyn4-32")
epicsEnvSet("TOP", "/root/stream-ioc")
epicsEnvSet("ARCH", "linux-arm")
epicsEnvSet ("STREAM_PROTOCOL_PATH", "$(TOP)/protocol")

# Database definition file
cd ${TOP}
dbLoadDatabase("dbd/streamApp.dbd")
streamApp_registerRecordDeviceDriver(pdbbase)

#==========================================================================
#                                       --prefix--
# Kicker:
#  - Ejection Kicker:                BO-48D:PM-EjeK
#  - Injection Kicker:               BO-01D:PM-InjK
#  - Injection Dipolar Kicker:       SI-01SA:PM-InjDpK
#  - Injection Non-Linear Kicker:    SI-01SA:PM-InjNLK
#
# Pinger:
#  - Vertical Pinger:                SI-19C4:PM-VPing
#
#  - Septum:
#  - Injection Septum:               TB-04:PM-InjS
#  - Ejection Thick Septum:          TS-01:PM-EjeSG
#  - Ejection Thin Septum:           TS-01:PM-EjeSF
#  - Injection Thick Septum:         TS-04:PM-InjSG-1
#                                    TS-04:PM-InjSG-2
#  - Injection Thin Septum:          TS-04:PM-InjSF
#
#==========================================================================
drvAsynIPPortConfigure("socket_spixconv", "unix:///tmp/socket_spixconv")

# database for 10 kV Voltage source:
dbLoadRecords("database/SPIxCONV.db", "PREFIX = BO-48D:PM-EjeK, SCAN_RATE = .1 second, SPIxCONV_ADDRESS = 1, VOLTAGE_FACTOR = 1000.0")

# Effectively initializes the IOC
cd iocBoot
iocInit
