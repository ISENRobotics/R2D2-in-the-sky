# coding: utf8
import threading
import logging
from datetime import datetime
from time import sleep
import Queue
from collections import deque

import sys
sys.path.insert(0, '/root/R2D2/classes/sous-classes')

import serie


class Surveillance_serie(threading.Thread):
	def __init__(self,controleur,filename="surveillance_serie.log"):
		threading.Thread.__init__(self)
		self.pere   =controleur
		self.queue_input_reception = deque()
		self.queue_output_emission = deque()
		self.serie=serie.Serie(self.queue_input_reception,self.queue_output_emission)
		self.stoprequest = threading.Event()
		self.logger1 = logging.getLogger('R2D2.surveillance_serie')
		self.formatter = logging.Formatter('%(asctime)s : %(message)s')
		self.fileHandler = logging.FileHandler(filename, mode='w')
		self.fileHandler.setFormatter(self.formatter)
		self.streamHandler = logging.StreamHandler()
		self.streamHandler.setFormatter(self.formatter)

		self.logger1.setLevel(logging.DEBUG)
		self.logger1.addHandler(self.fileHandler)
		self.logger1.addHandler(self.streamHandler)
		self.logger1.debug("Démarrage du thread de Surveillance_serie")
		self.serie.daemon = True
		self.serie.start()
		self.logger1.debug("Thread série démarré")

	def run(self):
		self.logger1.debug("Surveillance_serie running")
		sleep(0.01)
		self.logger1.debug("Serie initialized, commencing surveillance")
		#Messages servant à logger l'activité de la liaison série
		self.message_input = ""
		self.message_output = ""
		self.statut_serveur = "vivant"
		while not self.stoprequest.isSet():
			try:
				#Routine de logging d'activité de la liaison série
				if(self.message_input != self.serie.input[0]):
					self.message_input = self.serie.input[0]
			except IndexError:
				self.message_input = "pas d'input"
			try:
				if(self.message_output != self.serie.output[0]):
					self.message_output = self.serie.output[0]
			except IndexError:
				self.message_output = "pas d'output"
			self.serie_vivante = self.serie.is_alive()
			if(not self.serie_vivante):
				self.statut_serie = "mort"
				self.kill()
				self.logger1.critical("Le thread Serie ne répondait plus, il a été tué et réinstancié")
			else:
				self.statut_serie = "vivant"
			self.logger1.debug("Le thread serie est "+self.statut_serie+" et les messages suivants sont en attente de traitement : Emission série:"+str(self.message_input)+"///// Réception série:"+str(self.message_output))

	def stop(self):
		self.stoprequest.set()


	def kill(self):
		del self.serie
		self.serie=Serie()
		self.serie.daemon = True
		self.serie.start()
		self.pere.mise_a_jour_serie(self.serie)