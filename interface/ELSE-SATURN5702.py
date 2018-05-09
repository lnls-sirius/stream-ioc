#!/usr/bin/python
# -*- coding: utf-8 -*-

# Módulo necessário

import serial
import requests
import socket
import sys
import threading
import time
import datetime
import logging

# Definindo as viaveis

dataGamma = 0.0
dataNeutron = 0.0
dataTotal = 0.0
dataG = 0.0
dataN = 0.0
ipGamma = "192.168.0.100"
ipNeutron = "192.168.0.200"

UDP_PORT = int(sys.argv[1])

client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket1.connect((ipGamma, 10001))

client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket2.connect((ipNeutron, 10001))

# Log File for exceptions

logging.basicConfig(filename='app.log',level=logging.INFO)

# Função que inclui o checksum e o caractere <ETX> a qualquer mensagem que se deseja enviar

def format_message(message):

    checksum = ord(message[3]) ^ ord(message[4])
    for character in message[5:]:
        checksum ^= ord(character)
    return (message + "{0:02X}".format(checksum) + "\x03")


# Cria socket TCP/IP para comunicação com o SATURN I 5700 RTM da sonda de gamma

def cnct1(ip):

    # Requisita os valores das janelas de tempo para cáculo da média móvel
    # COLOCAR TB O VALOR O THRESHOLD LEVEL 01001GL RESPOSTA: (STX)01024GL1234.56:1234.56:1234.56
    # (CS)(CS) (ETX)

    client_socket1.send(format_message("\x0201001MI"))
    data = client_socket1.recv(1024)
    if data.find("K") != -1 or data.find("P") != -1 or data.find("B") != -1 or data.find("A") != -1 or  data.find("E") != -1 or  data.find("D") != -1 or  data.find("C") != -1 or  data.find("H") != -1:
        if data[9: len(data) - 3] != "" and data[0] == "\x02":
            return float(data[9: 15])
    else:
        pass

def cnct2(ip):

    # Requisita os valores das janelas de tempo para cáculo da média móvel
    # COLOCAR TB O VALOR O THRESHOLD LEVEL 01001GL RESPOSTA: (STX)01024GL1234.56:1234.56:1234.56
    # (CS)(CS) (ETX)

    client_socket2.send(format_message("\x0201001MI"))
    data = client_socket2.recv(1024)
    if data.find("K") != -1 or data.find("P") != -1 or data.find("B") != -1 or data.find("A") != -1 or data.find("E") != -1 or data.find("D") != -1 or data.find("C") != -1 or data.find("H") != -1:
        if data[9: len(data) - 3] != "" and data[0] == "\x02":
            return float(data[9: 15])
    else:
        pass

        # Funcao para calcular o delta time para integral

# Thread Principal

def scanThread():

    # Global Variables

    global SERIAL_PORT
    global dataGamma
    global dataNeutron
    global dataTotal
    global dataN
    global dataG
    global ipNeutron
    global ipGamma
    global client_socket1
    global client_socket2

    # Main Loop

    while (True) :

        try:
            # Delay de 0.5s ============ Testar

            time.sleep(1)

            # Send the pct for ELSE SATURN
            dataGamma = cnct1(ipGamma)

            dataNeutron = cnct2(ipNeutron)

            # If receiver void menssage do nothing

            if dataNeutron != None and dataGamma != None:

                dataTotal = dataGamma + dataNeutron

        except Exception as e:
            print(e)
            logging.error("Error occurred" + str(e))
            pass


# Inicializa a Main Thread

auxiliary_thread = threading.Thread(target = scanThread)
auxiliary_thread.setDaemon(True)
auxiliary_thread.start()

# O programa em sua verção final irá dormir 500s para garantir a leitura certa da sonda

udp_server_address = ("0.0.0.0", UDP_PORT)
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server_socket.bind(udp_server_address)

# Loop Principal

while (True):

    # Client (EPICS IOC) input data and address

    data, address = udp_server_socket.recvfrom(512)

    # There is a simple protocol for communication to the client

    if (data):

        if (data == "RAD_E_Gamma?\n" and dataNeutron != None and dataGamma != None):
            answer = "{:.10f}".format(dataGamma)

        elif (data == "RAD_E_Neutron?\n" and dataNeutron != None and dataGamma != None):
            answer = "{:.10f}".format(dataNeutron)

        elif (data == "RAD_E_Total?\n" and dataNeutron != None and dataGamma != None):
            answer = "{:.10f}".format(dataTotal)

        else:
            continue

        answer += "\n"
        udp_server_socket.sendto(answer, address)

        # The end

