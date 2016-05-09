#/usr/bin/env python
# -*-coding:Utf-8 -*
import Adafruit_BBIO.UART as UART
import serial

import threading

import Queue
import constants

from time import sleep
###   Préparation du programme

class Emission_Serie(threading.Thread):
	"""
	Classe regroupant l'émission par liaison série avec les moteurs
		Prend en entrée:
			queue_input : Une queue d'items input, les informations que le controleur envoie à la classe Série : les paramètres des commandes
			queue_output : Une queue d'items output, les informations que la liaison série envoie au controleur : les retours des commandes effectuées
			sel_uart : variable sélectionnant la liaison série à ouvrir, valant 1 par défaut (UART1)
	"""

	def __init__(self, queue_input, stopevent, sel_uart =1):
		if(sel_uart not in [1,2,4,5]):
				return "Erreur : la liaison série spécifiée n'est pas valide"
		threading.Thread.__init__(self)
		#Les informations à émettre sur la liaison série
		self.input = queue_input
		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = stopevent
		### Liaison série
		#On choisit la liaison série 1 par défaut, la liaison série spécifiée sinon
		UART.setup("UART"+str(sel_uart))

		#Ouverture de la liaison série
		self.ser = serial.Serial(port = "/dev/ttyO"+str(sel_uart), baudrate=38400,bytesize=8, stopbits=1,timeout=None)
		self.ser.close()

	def run(self):
		sleep(1)
		#Tant que le controleur ne demande pas au thread de s'arreter
		try:
			while not self.stoprequest.isSet():
				try:
					#On regarde si un nouveau jeu d'instructions a été mis en queue
					#Les jeux d'instructions se décomposent de la manière suivante : 
					#	infos[0] : valeur du mode de fonctionnement demandé
					#	infos[1] : valeur de la vitesse 1 demandée
					#	infos[2] : valeur de la vitesse 2 demandée
					#	infos[3] : valeur de l'acceleration demandée
					infos = self.input.pop()
					print("Dans la classe Emission serie : "+str(infos))
					longueur = len(infos)
					if(longueur == 4):
						self.resultM = self.ordre_moteurs(constants.SET_MODE,infos[0])
						self.resultG = self.ordre_moteurs(constants.SET_SPEED_1,infos[1])
						self.resultD = self.ordre_moteurs(constants.SET_SPEED_2,infos[2])
						self.resultA = self.ordre_moteurs(constants.SET_ACCELERATION,infos[3])
					elif(longueur == 1):
						self.result = self.ordre_moteurs(infos[0],0)
				except IndexError:
					continue
				except KeyboardInterrupt as key:
					print("Catched a keyboard interruption in Emission_Serie, exiting")
					self.ser.close()
					self.stoprequest.set()
		except KeyboardInterrupt as key:
			self.stoprequest.set()
		finally:
			self.ser.close()

	#Fonction chargée d'effectuer l'envoi sur la liaison série des commandes moteurs
	def ordre_moteurs(self,commande,parameter):
		self.ser.open()
		if self.ser.isOpen():
			self.ser.write(bytearray.fromhex(constants.CMD+commande+format(parameter, '#04x')[2:]))
		else:
			#Si la liaison série n'est pas ouverte, on renvoie l'erreur 1000
			return 1000
		self.ser.close()

	def stop(self):
		self.stoprequest.set()