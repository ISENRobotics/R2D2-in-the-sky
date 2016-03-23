#/usr/bin/env python
import Adafruit_BBIO.UART as UART
import serial
import socket
import curses

import os
import sys

if __name__ == '__main__':

    ### Liaison série
    #On choisir la liaison série 4
    UART.setup("UART4")

    #Ouverture de la liaison série
    ser = serial.Serial(port = "/dev/ttyO4", baudrate=9600)
    ser.close()
    ser.open()
    if ser.isOpen():
        ser.write('x34')
        ser.write('x00')
        ser.write('x31')
        ser.write('xff')
        ser.write('x32')
        ser.write('xff')
    ser.close()
