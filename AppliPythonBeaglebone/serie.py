#/usr/bin/env python
# -*-coding:Utf-8 -*
import Adafruit_BBIO.UART as UART
import serial
import curses

import threading

import os
import sys
import Queue
import constants

###   Préparation du programme

class Serie(threading.Thread):
	"""
	Classe regroupant la communication par liaison série avec les moteurs
		Prend en entrée:
			queue_input : Une queue d'items input, les informations que le controleur envoie à la classe Série : les paramètres des commandes
			queue_output : Une queue d'items output, les informations que la liaison série envoie au controleur : les retours des commandes effectuées
			sel_uart : variable sélectionnant la liaison série à ouvrir, valant 1 par défaut (UART1)
	"""

	def __init__(self, queue_input, queue_output, sel_uart =1):
		if(sel_uart not in [1,2,4,5]):
				return "Erreur : la liaison série spécifiée n'est pas valide"
		threading.Thread.__init__(self)
		self.input = queue_input
		self.output = queue_output
		self.MODE = 0
		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = threading.Event()
		### Liaison série
		#On choisit la liaison série 1 par défaut, la liaison série spécifiée sinon
		UART.setup("UART"+str(sel_uart))

		#Ouverture de la liaison série
		self.ser = serial.Serial(port = "/dev/ttyO"+str(sel_uart), baudrate=38400,bytesize=8, stopbits=1,timeout=None)
		self.test = self.ordre_moteurs("31","ff")
		self.test2 = self.ordre_moteurs("32","ff")
		self.ser.close()

	def run(self):
		#Tant que le controleur ne demande pas au thread de s'arreter
		while not self.stoprequest.isSet():
			try:
				#On regarde si un nouveau jeu d'instructions a été mis en queue
				#Les jeux d'instructions se décomposent de la manière suivante : 
				#	infos[0] : valeur du mode de fonctionnement demandé
				#	infos[1] : valeur de la vitesse 1 demandée
				#	infos[2] : valeur de la vitesse 2 demandée
				#	infos[3] : valeur de l'acceleration demandée
				infos = self.input.get(True)
				self.resultM = 0
				if(self.MODE != infos[0]):
					self.resultM = self.ordre_moteurs(constants.SET_MODE,infos[0])

				self.MODE = int(infos[0])
				self.resultG = self.ordre_moteurs(constants.SET_SPEED_1,int(infos[1]))
				self.resultD = self.ordre_moteurs(constants.SET_SPEED_2,int(infos[2]))
				#self.resultA = self.ordre_moteurs(constants.SET_ACCELERATION,int(infos[3]))
				#On renvoie au controleur les résultats des ordres
				print(self.resultG)
				print(self.resultD)
				self.output.put((self.resultM, self.resultG, self.resultD))
			except Queue.Empty:
				continue

	#Fonction chargée d'effectuer l'envoi sur la liaison série des commandes moteurs
	def ordre_moteurs(self,commande,parameter):
		#On vérifie que la commande et son paramètre correspondent à des valeurs autorisées
		self.AUTORISATION = True
		if(commande in constants.LIST_SET):
			self.AUTORISATION = self.verif_commande_SETSPEED(parameter)
		elif(commande == constants.SET_ACCELERATION):
			self.AUTORISATION = self.verif_commande_SETACCELERATION(parameter)
		elif(commande == constants.SET_MODE):
			self.AUTORISATION = self.verif_commande_SETMODE(parameter)

		if(self.AUTORISATION):
			self.ser.open()
			if self.ser.isOpen():
				self.ser.write(bytearray.fromhex(constants.CMD+commande+str(parameter)))
				#Si la commande est une commande GET, on lit la réponse et on la retourne
				if (commande in constants.LIST_GET):
						return self.ser.read()
			else:
				#Si la liaison série n'est pas ouverte, on renvoie l'erreur 1000
				return 1000
			self.ser.close()
		return 0
	
	def get_serial(self):
		return self.ser.name


	def verif_commande_SETSPEED(self,parameter):
		if(self.MODE % 2):
			return (parameter >= 0) & (parameter <= 255)
		else :
			return (parameter >= -128) & (parameter <= 127)

	def verif_commande_SETACCELERATION(self,parameter):
		return (parameter >= 1) & (parameter <= 10)

	def verif_commande_SETMODE(self,parameter):
		return (parameter >= 0) & (parameter <= 3)
