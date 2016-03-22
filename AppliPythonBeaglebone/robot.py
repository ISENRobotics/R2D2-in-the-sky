#/usr/bin/env python
# -*-coding:Utf-8 -*
import Adafruit_BBIO.UART as UART
import serial
import socket
import curses

import os
import sys

###   Préparation du programme

class Robot(object):
	"""
	Classe regroupant l'application générale du robot
		Contient:
			Une connexion série UART
			L'algorythmique de surveillance et la transmission des commandes aux moteurs
	"""
	def __init__(self):
		### Liaison série
		#On choisir la liaison série 4
		UART.setup("UART4")

		#Ouverture de la liaison série
		self.ser = serial.Serial(port = "/dev/ttyO4", baudrate=9600)
		self.ser.close()

	#Fonction chargée d'effectuer l'envoi sur la liaison série des commandes moteurs
	def ordre_moteurs(self,commande):
		self.ser.open()
		if self.ser.isOpen():
			self.ser.write(b+commande)
			#Si la commande est de connaitre la vitesse des moteurs 1 ou 2, on retourne cette valeur
			if (commande == '0x21' || commande == '0x22'):
					return self.ser.read()
		self.ser.close()
	
	def get_serial(self):
		return self.ser.name


