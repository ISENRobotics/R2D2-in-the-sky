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

	def __init__(self):
		### Liaison série
		#On choisir la liaison série 1
		UART.setup("UART1")

		#Ouverture de la liaison série
		self.ser = serial.Serial(port = "/dev/ttyO1", baudrate=38400,bytesize=8, stopbits=1,timeout=None)
		self.ser.close()

	#Fonction chargée d'effectuer l'envoi sur la liaison série des commandes moteurs
	def ordre_moteurs(self,commande):
		#On vérifie que la commande et son paramètre correspondent à des valeurs autorisées
		AUTORISATION = True
		if(commande == constants.SET_SPEED_1 || commande == constants.SET_SPEED_2):
			if(MODE == 0 || MODE == 1):
				AUTORISATION = verif_commande_SETSPEED_01()
			else
				if(commande == constants.SET_SPEED):
					AUTORISATION = verif_commande_SETSPEED_23()
				else
					AUTORISATION = verif_commande_TURN()
		else if(commande == constants.SET_ACCELERATION):
			AUTORISATION = verif_commande_SETACCELERATION
		else if(commande == constants.SET_MODE):
			AUTORISATION = verif_commande_SETMODE

		if(AUTORISATION):
			self.ser.open()
			if self.ser.isOpen():
				self.ser.write(commande)
				#Si la commande est de connaitre la vitesse des moteurs 1 ou 2, on retourne cette valeur
				if (commande == '0x21' || commande == '0x22'):
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