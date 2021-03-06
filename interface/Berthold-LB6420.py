#!/usr/bin/python
# -*- coding: utf-8 -*-

# Berthold-LB6420.py

# UDP/IP server for communication between the EPICS IOC and a Berthold LB 6420 environment radiation
# monitoring system.

# This Python program should be executed with two arguments. The first is the port of the UDP
# server. The other is the IP address of the Berthold LB 6420 probe. After launching this program,
# the user should wait at least 120 s before running the EPICS IOC.

# Tested with Python 2.7.13

# Necessary Python modules

import datetime
import math
import os
import pickle
import socket
import struct
import sys
import threading
import time

# UDP server port

UDP_PORT = int(sys.argv[1])

# Probe configuration

PROBE_IP = sys.argv[2]
PROBE_PORT = 1000

# Maximum averaging time configuration for simple moving average (s)

MAXIMUM_AVERAGING_TIME = 120

# Averaging time configuration for simple moving average. If there is a configuration file, this
# parameter is loaded from it. Otherwise, it is set to MAXIMUM_AVERAGING_TIME and stored in a new
# configuration file.

CONFIGURATION_FILE = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/Berthold-LB6420.data"

if (os.path.isfile(CONFIGURATION_FILE) == True):
    AVERAGING_TIME = pickle.load(open(CONFIGURATION_FILE, "rb"))
else:
    AVERAGING_TIME = MAXIMUM_AVERAGING_TIME
    pickle.dump(AVERAGING_TIME, open(CONFIGURATION_FILE, "wb"))

# Time series (raw data) for dose rate calculations

date_and_time = []
raw_data = []

# Time series of calculated dose rates

total_dose_rate = []         # Parameter 19
gamma = []                   # Parameter 31
total_neutron_rate = []      # Parameter 34
high_energy_neutrons = []    # Parameter 33

# This function returns one of the 64 parameters of the probe, converting the byte stream into an
# integer.

def raw_value(stream, parameter):
    base_index = 8 * parameter
    return(struct.unpack(">q", stream[base_index:(base_index + 8)])[0])

# Function for calculating a new dose rate value

def dose_rate_value(date_and_time, raw_data, parameter):

    time_difference = (date_and_time[-1] - date_and_time[-2]).total_seconds()
    raw_difference = raw_data[-1][parameter] - raw_data[-2][parameter]
    new_dose_rate = (raw_difference / time_difference) * 3600 * 1E-6

    return(new_dose_rate)

# Thread for reading data from the Berthold LB 6420 probe

def scanThread():

    # Global variables

    global date_and_time
    global raw_data

    global total_dose_rate
    global gamma
    global total_neutron_rate
    global high_energy_neutrons

    # This creates a TCP/IP socket for communication to the probe

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((PROBE_IP, PROBE_PORT))
    client_socket.settimeout(0.5)

    # Loop

    while (True):

        # A new set of data is required

        client_socket.send("\x0E\x04\x00\x00")
        answer = ""
        try:
            while (True):
                answer += client_socket.recv(1024)
                if (len(answer) == 524):
                    break
        except (socket.timeout):
            pass

        # If the answer has 524 bytes (the expected message length), received data is added to the
        # time series and dose rate values are updated.

        if (len(answer) == 524):

            answer = answer[12:]

            date_and_time.append(datetime.datetime.utcnow())

            new_raw_data = []
            for parameter in range(0, 64):
                new_raw_data.append(raw_value(answer, parameter))
            raw_data.append(new_raw_data)

            if (len(date_and_time) > MAXIMUM_AVERAGING_TIME + 1):
                date_and_time = date_and_time[1:]
                raw_data = raw_data[1:]

            if (len(date_and_time) >= 2):

                total_dose_rate.append(dose_rate_value(date_and_time, raw_data, 19))
                gamma.append(dose_rate_value(date_and_time, raw_data, 31))
                total_neutron_rate.append(dose_rate_value(date_and_time, raw_data, 34))
                high_energy_neutrons.append(dose_rate_value(date_and_time, raw_data, 33))

                if (len(total_dose_rate) > MAXIMUM_AVERAGING_TIME):

                    total_dose_rate = total_dose_rate[1:]
                    gamma = gamma[1:]
                    total_neutron_rate = total_neutron_rate[1:]
                    high_energy_neutrons = high_energy_neutrons[1:]

        time.sleep(1)

# This launches the auxiliary thread of the program

auxiliary_thread = threading.Thread(target = scanThread)
auxiliary_thread.setDaemon(True)
auxiliary_thread.start()

# The program will sleep for 5 seconds before listening to requests from the EPICS IOC

time.sleep(5)

# This creates the UDP/IP socket

udp_server_address = ("0.0.0.0", UDP_PORT)
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server_socket.bind(udp_server_address)

# Loop

while (True):

    # Client (EPICS IOC) input data and address

    data, address = udp_server_socket.recvfrom(512)

    # Input processing. There is a simple protocol for communication to the client.

    if (data):

        # This software will not answer to any request until all its buffers are filled

        if (len(total_dose_rate) < MAXIMUM_AVERAGING_TIME):
            answer = "INITIALIZING\n"
            udp_server_socket.sendto(answer, address)
            continue

        if ((data[:14] == "AVERAGING_TIME") and (data[-1] == "\n")):
            if (len(data[:-1].split(" ")) == 2):
                try:
                    NEW_AVERAGING_TIME = int(data[:-1].split(" ")[1])
                except (ValueError):
                    answer = "INVALID_INPUT\n"
                    udp_server_socket.sendto(answer, address)
                    continue
                if ((NEW_AVERAGING_TIME >= 1) and (NEW_AVERAGING_TIME <= MAXIMUM_AVERAGING_TIME)):
                    AVERAGING_TIME = NEW_AVERAGING_TIME
                    pickle.dump(AVERAGING_TIME, open(CONFIGURATION_FILE, "wb"))
                    answer = "OK\n"
                else:
                    answer = "INVALID_INPUT\n"
                udp_server_socket.sendto(answer, address)
                continue

        if (data == "AVERAGING_TIME?\n"):
            answer = str(AVERAGING_TIME)
        elif (data == "TOTAL_DOSE_RATE?\n"):
            dose_rate = math.fsum(total_dose_rate[-AVERAGING_TIME:]) / AVERAGING_TIME
            answer = "{:.10f}".format(dose_rate)
        elif (data == "GAMMA?\n"):
            dose_rate = math.fsum(gamma[-AVERAGING_TIME:]) / AVERAGING_TIME
            answer = "{:.10f}".format(dose_rate)
        elif (data == "TOTAL_NEUTRON_RATE?\n"):
            dose_rate = math.fsum(total_neutron_rate[-AVERAGING_TIME:]) / AVERAGING_TIME
            answer = "{:.10f}".format(dose_rate)
        elif (data == "HIGH_ENERGY_NEUTRONS?\n"):
            dose_rate = math.fsum(high_energy_neutrons[-AVERAGING_TIME:]) / AVERAGING_TIME
            answer = "{:.10f}".format(dose_rate)
        else:
            answer = "INVALID_INPUT"

        answer += "\n"
        udp_server_socket.sendto(answer, address)
