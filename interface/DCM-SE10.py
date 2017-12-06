#!/usr/bin/python
# -*- coding: utf-8 -*-

# DCM-SE10.py

# UDP/IP server for communication between the EPICS IOC and a DCM SE-10 environment temperature and
# humidity monitoring system.

# This Python program should be executed with two parameters. The first is the port of the UDP
# server. The other is the IP address of the DCM SE-10 module.

# Necessary Python modules

import requests
import socket
import sys
import threading
import time

# Time interval between two successive readings (s)

TIME_INTERVAL = 2.0

# UDP server port number

UDP_PORT = int(sys.argv[1])

# DCM SE-10 IP address

DEVICE_IP_ADDRESS = sys.argv[2]

# DCM SE-10 internal temperature sensor measurement (°C)

TEMPERATURE1 = "0.0"

# DCM SE-10 external temperature sensor measurement (°C)

TEMPERATURE2 = "0.0"

# DCM SE-10 humidity measurement (%)

HUMIDITY = "0.0"

# Thread for reading data from the DCM SE-10 module

def scanThread():

    # Global variables

    global TEMPERATURE1
    global TEMPERATURE2
    global HUMIDITY

    # Loop

    while (True):

        try:

            # Here data is requested from the device and parsed

            data = requests.get("http://" + DEVICE_IP_ADDRESS + "/json").json()

            # New values for temperatures and humidity are obtained from the JSON data structure

            TEMPERATURE1 = str(data["temp"])
            TEMPERATURE2 = str(data["temp_ext"])
            HUMIDITY = str(data["umid"])

        except (Exception):

            pass

        # Time interval before the next reading

        time.sleep(TIME_INTERVAL)

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

        if (data == "T1?\n"):
            answer = TEMPERATURE1
        elif (data == "T2?\n"):
            answer = TEMPERATURE2
        elif (data == "H?\n"):
            answer = HUMIDITY
        else:
            continue

        answer += "\n"
        udp_server_socket.sendto(answer, address)
