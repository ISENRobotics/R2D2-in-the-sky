#/usr/bin/env python
# -*-coding:Utf-8 -*
import Adafruit_BBIO.UART as UART
import serial
import curses

import threading

import os
import sys
import Queue
from collections import deque

from time import sleep

import sys
sys.path.insert(0, '/root/R2D2/classes/sous-classes/sous-sous-classes')

from emission_serie import Emission_Serie
from reception_serie import Reception_Serie

###   Préparation du programme

class Serie(threading.Thread):
	"""
	Classe regroupant la communication par liaison série avec les moteurs
		Prend en entrée:
			queue_input : Une queue d'items input, les informations que le controleur envoie à la classe Série : les paramètres des commandes
			queue_output : Une queue d'items output, les informations que la liaison série envoie au controleur : les retours des commandes effectuées
			sel_uart : variable sélectionnant la liaison série à ouvrir, valant 1 par défaut (UART1)
	"""

	def __init__(self, queue_input, queue_output, stopevent, sel_uart =1):
		if(sel_uart not in [1,2,4,5]):
				return "Erreur : la liaison série spécifiée n'est pas valide"
		threading.Thread.__init__(self)
		self.input = queue_input
		self.output = queue_output
		self.queue_input_reception = deque()
		self.queue_output_emission = deque()

		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = stopevent
		self.thread_emission_serie = Emission_Serie(self.queue_output_emission,stopevent)
		self.thread_emission_serie.daemon = True
		self.thread_reception_serie = Reception_Serie(self.queue_input_reception,stopevent)
		self.thread_reception_serie.daemon = True
		self.thread_emission_serie.start()
		self.thread_reception_serie.start()
		
	def run(self):
		sleep(1)
		#Tant que le controleur ne demande pas au thread de s'arreter
		try:
			while not self.stoprequest.isSet():
				try:
					#On regarde si on a recu des informations, si oui, on les transmet à l'algorithmique
					infos = self.input.pop()
					print("Dans la classe Série: "+str(infos))
					self.queue_output_emission.appendleft(infos)
				except IndexError:
					try:
						#Si on n'a pas recu d'informations dans le temps imparti, on regarde si un message à envoyer est arrivé
						infos = self.queue_input_reception.pop()
						print("Dans la classe Série: "+str(infos))
						self.output.appendleft(infos)
					except IndexError:
						continue
					except KeyboardInterrupt as key:
						self.stoprequest.set()
				except KeyboardInterrupt as key:
					self.stoprequest.set()
		except KeyboardInterrupt as key:
			self.stoprequest.set()
		finally:
			self.thread_emission_serie.stop()
			self.thread_reception_serie.stop()

	def stop(self):
		self.stoprequest.set()