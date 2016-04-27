#/usr/bin/env python
# -*-coding:Utf-8 -*
import Adafruit_BBIO.UART as UART
import serial
import curses

import threading

import os
import sys
import Queue

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
		self.queue_input_reception = Queue.Queue()
		self.queue_output_emission = Queue.Queue()

		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = threading.Event()
		self.thread_emission_serie = Emission_serie(self.queue_output_emission)
		self.thread_reception_serie = Reception_serie(self.queue_input_reception)
		thread_emission_serie.start()
		thread_reception_serie.start()
		
	def run(self):
		#Tant que le controleur ne demande pas au thread de s'arreter
		while not self.stoprequest.isSet():
			try:
				#On regarde si on a recu des informations, si oui, on les transmet à l'algorithmique
				infos = self.input.get(True,0.005)
				self.queue_output_emission.put(infos)
			except Queue.Empty:
				try:
					#Si on n'a pas recu d'informations dans le temps imparti, on regarde si un message à envoyer est arrivé
					infos = self.queue_input_reception.get(True,0.005)
					self.output.put(infos)
				except Queue.Empty:
					continue