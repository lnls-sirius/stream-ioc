#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importing libraries

import serial
import socket
import sys
import threading
import datetime
import logging

dataGamma = 0.0
dataNeutron = 0.0
dataTotal = 0.0
dataG = 0.0
dataN = 0.0

SERIAL_PORT = str(sys.argv[1])

UDP_PORT = int(sys.argv[2])

# Log File for exceptions
logging.basicConfig(filename='app.log',level=logging.INFO)

# Function to include the checksum in the package

def incluirChecksum(entrada):
    soma = 0
    for elemento in entrada:
        soma += ord(elemento)
    soma = soma % 256
    return(entrada + "{0:02X}".format(soma) + "\x03")

# Main Thread 

def scanThread():

    # Global Variables

    global SERIAL_PORT
    global dataGamma
    global dataNeutron
    global dataTotal
    global dataN
    global dataG

    # Serial interface initialization

    serial_interface = serial.Serial(port = "{}".format(SERIAL_PORT),
                                     baudrate = 19200,
                                     bytesize = serial.SEVENBITS,
                                     parity = serial.PARITY_EVEN,
                                     stopbits = serial.STOPBITS_TWO,
                                     timeout = 0.5
                                    )

    # 01 Gamma ----------- 02 Neutron

    while (True):

        time.sleep(0.5)

        # Ships the pack for Gamma reading
        try:

            pct1 = incluirChecksum("\x07" + "01RM1")

            serial_interface.write(pct1)

            dataGamma = serial_interface.read(50)

        # Ships the pack for Neutron reading

            pct2 = incluirChecksum("\x07" + "01RM2")

            serial_interface.write(pct2)

            dataNeutron = serial_interface.read(50)

        # Conditional if the received message is empty due to problem in the probe the algorithm does nothing

            if dataGamma != "" and dataNeutron != "":
                dataG = float(dataGamma.split(" ")[1])
                dataN = float(dataNeutron.split(" ")[1])

            dataTotal = dataG + dataN

        except Exception as e:
            print(e)
            logging.error("Error occurred" + str(e))
            pass


auxiliary_thread = threading.Thread(target = scanThread)
auxiliary_thread.setDaemon(True)
auxiliary_thread.start()

# The program in its final version will sleep 500s to ensure the right reading of the probe

udp_server_address = ("0.0.0.0", UDP_PORT)
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server_socket.bind(udp_server_address)

# Main Loop

while (True):

    # Client (EPICS IOC) input data and address

    data, address = udp_server_socket.recvfrom(512)

    # There is a simple protocol for communication to the client

    if (data):

        if (data == "RAD_G?\n"):
            answer = "{:.10f}".format(dataG)

        elif (data == "RAD_N?\n"):
            answer = "{:.10f}".format(dataN)

        elif (data == "RAD_T?\n"):
            answer = "{:.10f}".format(dataTotal)

        else:
            continue

        answer += "\n"
        udp_server_socket.sendto(answer, address)

