#!/usr/bin/python
# -*- coding: utf-8 -*-

from epics import camonitor
from Queue import Queue
from pcaspy import Driver, SimpleServer
import sys
import threading

class IntegralDriver(Driver):

    # Add elements do queue
    def __init__(self, PV_input, PV_output):

        Driver.__init__(self)

        self.PV_input = PV_input
        self.PV_output = PV_output

        # created variables
        self.dataBuffer = []

        # start queue
        self.queue = Queue()

        # start others threads
        self.process_thread = threading.Thread(target=self.processThread)
        self.process_thread.setDaemon(True)
        self.process_thread.start()

        # monitor of PV element
        camonitor(self.PV_input, callback=self.enqueueData)

    # Queue Thread
    def enqueueData(self, **kwargs):
        self.queue.put({"value": kwargs["value"], "timestamp": kwargs["timestamp"]})

    # Process Thread
    def processThread(self):

        # Integral Function
        def integral_ele(dataPast, data):
            deltaTime = (data["timestamp"] - dataPast["timestamp"]) / 3600.0
            return ((data["value"] + dataPast["value"]) * deltaTime * 0.5)

        # Queue processing
        while (True):

            dataQueue = self.queue.get(block=True)

            # Feed Buffers
            if (self.dataBuffer == []):
                self.dataBuffer.append(dataQueue)
                continue
            else:
                if (dataQueue["timestamp"] <= self.dataBuffer[-1]["timestamp"]):
                    continue
                else:
                    self.dataBuffer.append(dataQueue)

            # Integral Calculation
            integral = self.getParam(self.PV_output)
            integral += integral_ele(self.dataBuffer[-2], self.dataBuffer[-1])
            while (self.dataBuffer[-1]["timestamp"] - self.dataBuffer[1]["timestamp"] > 14400.0):
                integral -= integral_ele(self.dataBuffer[0], self.dataBuffer[1])
                self.dataBuffer = self.dataBuffer[1:]

            # Att integral value to PV out
            self.setParam(self.PV_output, integral)
            self.updatePVs()


# Main Thread

if (__name__ == "__main__"):

    # PVs I/O
    PV_input = sys.argv[1]
    PV_output = sys.argv[2]

    # PV config
    PVs = {PV_output: {"type": "float",
                       "prec": 3,
                       "unit": "uSv",
                       "low": -0.1,
                       "high": 1.5,
                       "lolo": -0.1,
                       "hihi": 2}}

    # Start Threads prl and CA
    CA_server = SimpleServer()
    CA_server.createPV("", PVs)
    driver = IntegralDriver(PV_input, PV_output)

    # Main loop
    while (True):
        CA_server.process(0.1)
