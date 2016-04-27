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

class Reception_Serie(threading.Thread):
	"""
	Classe regroupant la communication par liaison série avec les moteurs
		Prend en entrée:
			queue_input : Une queue d'items input, les informations que le controleur envoie à la classe Série : les paramètres des commandes
			queue_output : Une queue d'items output, les informations que la liaison série envoie au controleur : les retours des commandes effectuées
			sel_uart : variable sélectionnant la liaison série à ouvrir, valant 1 par défaut (UART1)
	"""

	def __init__(self, queue_input, sel_uart =1):
		if(sel_uart not in [1,2,4,5]):
				return "Erreur : la liaison série spécifiée n'est pas valide"
		threading.Thread.__init__(self)
		self.input = queue_input
		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = threading.Event()
		### Liaison série
		#On choisit la liaison série 1 par défaut, la liaison série spécifiée sinon
		UART.setup("UART"+str(sel_uart))

		#Ouverture de la liaison série
		self.ser = serial.Serial(port = "/dev/ttyO"+str(sel_uart), baudrate=38400,bytesize=8, stopbits=1,timeout=0.005)
		self.ser.close()

	def run(self):
		#Tant que le controleur ne demande pas au thread de s'arreter
		while not self.stoprequest.isSet():
			try:
				$infos = self.ser.read()
				#On regarde si un nouveau jeu d'instructions a été mis en queue
				#Les jeux d'instructions se décomposent de la manière suivante : 
				#	infos[0] : valeur du mode de fonctionnement demandé
				#	infos[1] : valeur de la vitesse 1 demandée
				#	infos[2] : valeur de la vitesse 2 demandée
				#	infos[3] : valeur de l'acceleration demandée
				self.input.put(infos)
			except Queue.Empty:
				continue

	
