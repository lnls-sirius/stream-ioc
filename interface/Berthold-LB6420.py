#!/usr/bin/python
# -*- coding: utf-8 -*-

# Berthold-LB6420.py

# UDP/IP server for communication between the EPICS IOC and a Berthold LB 6420 environment radiation
# monitoring system.

# This Python program should be executed with two parameters. The first is the port of the UDP
# server. The other is the IP address of the Berthold LB 6420 probe.

# Necessary Python modules

import datetime
import socket
import struct
import sys
import time

# UDP server port number

UDP_PORT = int(sys.argv[1])

# Probe configuration

PROBE_IP = sys.argv[2]
PROBE_PORT = 1000

# Averaging time configuration for simple moving average (s)

AVERAGING_TIME = 120

# Dose rates are initialized at 0.0 µSv/h

TOTAL_DOSE_RATE = 0.0         # Parameter 19
GAMMA = 0.0                   # Parameter 31
TOTAL_NEUTRON_RATE = 0.0      # Parameter 34
HIGH_ENERGY_NEUTRONS = 0.0    # Parameter 33

# Time series (raw data) for dose rate calculations

date_and_time = []
raw_data = []

# Time series of calculated doses

total_dose_rate = []
gamma = []
total_neutron_rate = []
high_energy_neutrons = []

# Number of probe readings already performed (this counter stops when it reaches AVERAGING_TIME + 1)

N = 0

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

    global TOTAL_DOSE_RATE
    global GAMMA
    global TOTAL_NEUTRON_RATE
    global HIGH_ENERGY_NEUTRONS

    # This creates a TCP/IP socket for communication to the probe

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((PROBE_IP, PROBE_PORT))

    # Loop

    while (True):

        # A new set of data is required. Two "recv" calls are necessary because the probe sends two
        # answer messages to the client in sequence. The second one contains the desired data.

        client_socket.send("\x0E\x04\x00\x00")
        answer = client_socket.recv(1024)
        answer = client_socket.recv(1024)

        # If the answer has 512 bytes (the expected message length), the received data is added to
        # the time series and dose rate values are updated.

        if (len(answer) == 512):

            date_and_time.append(datetime.datetime.utcnow())

            new_raw_data = []
            for parameter in range(0, 64):
                new_raw_data.append(raw_value(answer, parameter))
            raw_data.append(new_raw_data)

            if (N < AVERAGING_TIME + 1):
                N += 1

            if (len(date_and_time) > AVERAGING_TIME + 1):
                date_and_time = date_and_time[1:]
                raw_data = raw_data[1:]

            if (N >= 2):

                total_dose_rate.append(dose_rate_value(date_and_time, raw_data, 19))
                gamma.append(dose_rate_value(date_and_time, raw_data, 31))
                total_neutron_rate.append(dose_rate_value(date_and_time, raw_data, 34))
                high_energy_neutrons.append(dose_rate_value(date_and_time, raw_data, 33))

                if (len(total_dose_rate) > AVERAGING_TIME):

                    TOTAL_DOSE_RATE += (total_dose_rate[-1] - total_dose_rate[0]) / AVERAGING_TIME
                    total_dose_rate = total_dose_rate[1:]

                    GAMMA += (gamma[-1] - gamma[0]) / AVERAGING_TIME
                    gamma = gamma[1:]

                    TOTAL_NEUTRON_RATE += (total_neutron_rate[-1] - total_neutron_rate[0]) / AVERAGING_TIME
                    total_neutron_rate = total_neutron_rate[1:]

                    HIGH_ENERGY_NEUTRONS += (high_energy_neutrons[-1] - high_energy_neutrons[0]) / AVERAGING_TIME
                    high_energy_neutrons = high_energy_neutrons[1:]

                else:

                    TOTAL_DOSE_RATE = (TOTAL_DOSE_RATE * (N - 2) + total_dose_rate[-1]) / (N - 1)
                    GAMMA = (GAMMA * (N - 2) + gamma[-1]) / (N - 1)
                    TOTAL_NEUTRON_RATE = (TOTAL_NEUTRON_RATE * (N - 2) + total_neutron_rate[-1]) / (N - 1)
                    HIGH_ENERGY_NEUTRONS = (HIGH_ENERGY_NEUTRONS * (N - 2) + high_energy_neutrons[-1]) / (N - 1)

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

    # There is a simple protocol for communication to the client

    if (data):

        if (data == "TOTAL_DOSE_RATE?\n"):
            answer = "{:.10f}".format(TOTAL_DOSE_RATE)
        elif (data == "GAMMA?\n"):
            answer = "{:.10f}".format(GAMMA)
        elif (data == "TOTAL_NEUTRON_RATE?\n"):
            answer = "{:.10f}".format(TOTAL_NEUTRON_RATE)
        elif (data == "HIGH_ENERGY_NEUTRONS?\n"):
            answer = "{:.10f}".format(HIGH_ENERGY_NEUTRONS)
        else:
            continue

        answer += "\n"
        udp_server_socket.sendto(answer, address)
