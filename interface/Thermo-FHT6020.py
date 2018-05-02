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

sample = 14400
dataBuffer = [0.0]*sample
timeBuffer = [0]*sample
deltatimeBuffer = [0]*sample
gammaBuffer = [0.0]*sample
neutronBuffer = [0.0]*sample
integralgamma = 0.0
integralneutron = 0.0
integral = 0.0
dataGamma = 0.0
dataNeutron = 0.0
dataTotal = 0.0
dataG = 0.0
dataN = 0.0
deltatime = 0
j=0
flag = 0

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

# Funcao para calcular o delta time para integral

def time_sec(timeBuffer):
    deltatime = (timeBuffer[-1] - timeBuffer[-2]).total_seconds()
    return deltatime

# Thread Principal

def scanThread():

    # Global Variables

    global integral
    global dataBuffer
    global SERIAL_PORT
    global dataGamma
    global dataNeutron
    global dataTotal
    global dataN
    global dataG
    global timeBuffer
    global deltatimeBuffer
    global integralgamma
    global integralneutron
    global gammaBuffer
    global neutronBuffer
    global sample
    global deltatime
    global j
    global flag

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


        #print("Radiação Total:     " + "{}".format(dataTotal) + " uSv/h")
        #print("\n")

        # Calcula o valor em Sv/h e ja que terei que multiplicar por segundo preciso de converter
        # De uSv/h para Sv/s e multiplicar por delta T para obter a área

            gammaBuffer.append(dataG)
            neutronBuffer.append(dataN)
            dataBuffer.append(dataTotal)

        # Tendo em vista que a integral começa zerada a soma de todos os vetores é igual a zero logo não
        # preciso somar todos os vetores.

            timeBuffer.append(datetime.datetime.utcnow())

            if timeBuffer[-1] != 0 and timeBuffer[-2] != 0:

                deltatime = time_sec(timeBuffer)
                deltatimeBuffer.append(deltatime)
		
                integralgamma += ((gammaBuffer[-1] + gammaBuffer[-2]) * deltatimeBuffer[-1])  / (2 * 3600)
                integralneutron += ((neutronBuffer[-1] + neutronBuffer[-2]) * deltatimeBuffer[-1])  / (2 * 3600)
                integral += ((dataBuffer[-1] + dataBuffer[-2]) * deltatimeBuffer[-1])  / (2 * 3600)

		if deltatimeBuffer[0] != 0:
                    while j <= sample:
		    	
		        flag = 1
                	
                        if (timeBuffer[-1] - timeBuffer[j]).total_seconds() > sample and deltatimeBuffer[0] != 0:
        	        
                            integralgamma -= ((gammaBuffer[j] + gammaBuffer[j + 1]) * deltatimeBuffer[j]) / (2 * 3600)
                            integralneutron -= ((neutronBuffer[j] + neutronBuffer[j + 1]) * deltatimeBuffer[j]) / (2 * 3600)
                            integral -= ((dataBuffer[j] + dataBuffer[j + 1]) * deltatimeBuffer[j]) / (2 * 3600)
                        j += 1

                j = 0
                flag = 0

                    

        # Apaga o primeiro elemento do vetor ao adicionar um novo caso passe do tamanho sample

            if len(dataBuffer) > sample:
                dataBuffer = dataBuffer[1:]

            if len(timeBuffer) > sample:
                timeBuffer = timeBuffer[1:]

            if len(deltatimeBuffer) > sample:
                deltatimeBuffer = deltatimeBuffer[1:]

            if len(gammaBuffer) > sample:
                gammaBuffer = gammaBuffer[1:]

            if len(neutronBuffer) > sample:
                neutronBuffer = neutronBuffer[1:]


        # print("O valor da integral em 4h é:  " + "{}".format(integral) + " uSv")
        # print("\n")

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

        if (data == "RAD_G?\n") and flag != 1:
            answer = "{:.10f}".format(gammaBuffer[-1])

        elif (data == "RAD_N?\n") and flag != 1:
            answer = "{:.10f}".format(neutronBuffer[-1])

        elif (data == "RAD_T?\n" and flag != 1):
            answer = "{:.10f}".format(dataBuffer[-1])

        elif (data == "RAD_I?\n") and flag != 1:
            answer = "{:.10f}".format(integral)

        elif (data == "RAD_I_G?\n") and flag != 1:
            answer = "{:.10f}".format(integralgamma)

        elif (data == "RAD_I_N?\n") and flag != 1:
            answer = "{:.10f}".format(integralneutron)

        else:
            continue

        answer += "\n"
        udp_server_socket.sendto(answer, address)

        # The end
