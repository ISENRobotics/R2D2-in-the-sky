#/usr/bin/env python
# -*-coding:Utf-8 -*
import Adafruit_BBIO.UART as UART
import serial
import socket
import curses

import os
import sys

import constants

###   Préparation du programme

class Robot(object):
	"""
	Classe regroupant l'application générale du robot
		Contient:
			Une connexion série UART
			L'algorythmique de surveillance et la transmission des commandes aux moteurs
	"""
	MODE = 0

	def __init__(self, sel_uart =1):
		### Liaison série
		#On choisir la liaison série 1
		UART.setup("UART"+sel_uart)

		#Ouverture de la liaison série
		self.ser = serial.Serial(port = "/dev/ttyO"+sel_uart, baudrate=38400,bytesize=8, stopbits=1,timeout=None)
		self.ser.close()

	#Fonction chargée d'effectuer l'envoi sur la liaison série des commandes moteurs
	def ordre_moteurs(self,commande,parameter):
		#On vérifie que la commande et son paramètre correspondent à des valeurs autorisées
		AUTORISATION = True
		if(commande == constants.SET_SPEED_1 || commande == constants.SET_SPEED_2):
			if(MODE == 0 || MODE == 1):
				AUTORISATION = verif_commande_SETSPEED_01(parameter)
			else
				if(commande == constants.SET_SPEED):
					AUTORISATION = verif_commande_SETSPEED_23(parameter)
				else
					AUTORISATION = verif_commande_TURN(parameter)
		else if(commande == constants.SET_ACCELERATION):
			AUTORISATION = verif_commande_SETACCELERATION(parameter)
		else if(commande == constants.SET_MODE):
			AUTORISATION = verif_commande_SETMODE(parameter)

		if(AUTORISATION):
			self.ser.open()
			if self.ser.isOpen():
				self.ser.write(constants.CMD+commande+parameter)
				#Si la commande est une commande GET, on lit la réponse et on la retourne
				if (commande in constants.LIST_GET):
						return self.ser.read()
			self.ser.close()
	
	def get_serial(self):
		return self.ser.name


	def verif_commande_SETSPEED_01(self,parameter):
		if(MODE == 0):
			return (parameter >= 0) & (parameter <= 255)
		else if (MODE == 1):
			return (parameter >= -128) & (parameter <= 127)
		else :
			return False;


	def verif_commande_SETSPEED_23(self,parameter):
		if(MODE == 2):
			return (parameter >= 0) & (parameter <= 255)
		else if (MODE == 3):
			return (parameter >= -128) & (parameter <= 127)
		else :
			return False;

	def verif_commande_TURN(self,parameter):
		if(MODE == 2):
			return (parameter >= 0) & (parameter <= 255)
		else if (MODE == 3):
			return (parameter >= -128) & (parameter <= 127)
		else :
			return False;

	def verif_commande_SETACCELERATION(self,parameter):
		return (parameter >= 1) & (parameter <= 10)

	def verif_commande_SETMODE(self,parameter):
		return (parameter >= 0) & (parameter <= 3)