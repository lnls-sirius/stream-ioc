#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importando as bibliotecas

import serial
import socket
import sys
import threading
import datetime
import logging

# Definindo o pino do P9 14 como saída para o osciloscópio

dataGamma = 0.0
dataNeutron = 0.0
dataTotal = 0.0
dataG = 0.0
dataN = 0.0

SERIAL_PORT = str(sys.argv[1])

UDP_PORT = int(sys.argv[2])

# Log File for exceptions
logging.basicConfig(filename='app.log',level=logging.INFO)

# Funcao para incluir o checksum no pacote

def incluirChecksum(entrada):
    soma = 0
    for elemento in entrada:
        soma += ord(elemento)
    soma = soma % 256
    return(entrada + "{0:02X}".format(soma) + "\x03")

# Thread Principal

def scanThread():

    # Global Variables

    global SERIAL_PORT
    global dataGamma
    global dataNeutron
    global dataTotal
    global dataN
    global dataG

    # Inicialização da interface serial

    serial_interface = serial.Serial(port = "{}".format(SERIAL_PORT),
                                     baudrate = 19200,
                                     bytesize = serial.SEVENBITS,
                                     parity = serial.PARITY_EVEN,
                                     stopbits = serial.STOPBITS_TWO,
                                     timeout = 0.5
                                    )

    # 01 Gamma ----------- 02 Neutron

    while (True):

        # Delay de 500ms para cara envio de pacote

        #time.sleep(0.500)

        # Envia o pacote para a leitura Gamma
        try:

            pct1 = incluirChecksum("\x07" + "01RM1")

        #print(pct1)

            serial_interface.write(pct1)

        # Lê os oito caracteres enviados Gamma

            dataGamma = serial_interface.read(50)

        # Envia o pacote para a leitura Neutron

            pct2 = incluirChecksum("\x07" + "01RM2")

        #print(pct2)

            serial_interface.write(pct2)

        # Lê os oito caracteres enviados Neutron

            dataNeutron = serial_interface.read(50)

        # Calcula o valor da taxa de dose instantânea (em uSv/h)
        # descobrir como chegam os dados e trata-los
        # condicional caso a mensagem recebida for vazia por problema na sonda o algoritmo nao faz nada

            if dataGamma != "" and dataNeutron != "":
                dataG = float(dataGamma.split(" ")[1])
                dataN = float(dataNeutron.split(" ")[1])

            #print("Radiação Gamma:     " + "{}".format(dataG) + " uSv/h")
            #print("Radiação Neutron:   " + "{}".format(dataN) + " uSv/h")

        # Imprime na tela o resultado

            dataTotal = dataG + dataN

        except Exception as e:
            print(e)
            logging.error("Error occurred" + str(e))
            pass


# aux a thread principal

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

