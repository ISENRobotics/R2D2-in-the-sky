# coding: utf8
import threading
import logging
from datetime import datetime
from time import sleep
import Queue
from collections import deque

import sys
sys.path.insert(0, '/root/R2D2/classes/sous-classes')

import serveur

class Surveillance_serveur(threading.Thread):
	def __init__(self,controleur,filename="surveillance_serveur.log"):
		threading.Thread.__init__(self)
		self.pere   =controleur
		self.queue_input_reception = deque()
		self.queue_output_emission = deque()
		self.serveur=serveur.Serveur(self.queue_input_reception,self.queue_output_emission)
		self.stoprequest = threading.Event()
		self.logger2 = logging.getLogger('R2D2.surveillance_serveur')
		self.formatter = logging.Formatter('%(asctime)s : %(message)s')
		self.fileHandler = logging.FileHandler(filename, mode='w')
		self.fileHandler.setFormatter(self.formatter)
		self.streamHandler = logging.StreamHandler()
		self.streamHandler.setFormatter(self.formatter)

		self.logger2.setLevel(logging.DEBUG)
		self.logger2.addHandler(self.fileHandler)
		self.logger2.addHandler(self.streamHandler)
		self.logger2.debug("Démarrage du thread de Surveillance_serveur")

		self.serveur.daemon=True
		self.serveur.start()
		self.logger2.debug("Thread serveur démarré")

	def run(self):
		self.logger2.debug("Surveillance_serveur running")
		sleep(0.01)
		self.logger2.debug("Serveur initialized, commencing surveillance")
		#Messages servant à logger l'activité du serveur
		self.message_input = ""
		self.message_output = ""
		self.statut_serveur = "vivant"
		while not self.stoprequest.isSet():
			try:
				#Routine de logging d'activité du serveur
				if(self.message_input != self.serveur.input[0]):
					self.message_input = self.serveur.input[0]
			except IndexError:
				self.message_input = "pas d'input"
			try:
				if(self.message_output != self.serveur.output[0]):
					self.message_output = self.serveur.output[0]
			except IndexError:
				self.message_output = "pas d'output"
			self.serveur_vivant = self.serveur.is_alive()
			if(not self.serveur_vivant):
				self.statut_serveur = "mort"
				self.kill()
				self.logger2.critical("Le thread Serveur ne répondait plus, il a été tué et réinstancié")
			else:
				self.statut_serveur = "vivant"
			self.logger2.debug("Le thread serveur est "+self.statut_serveur+" et les messages suivants sont en attente de traitement : Emission serveur:"+str(self.message_input)+"///// Réception serveur:"+str(self.message_output))
			sleep(0.1)

	def stop(self):
		self.stoprequest.set()


	def kill(self):
		del self.serveur
		self.serveur=Serveur()
		self.serveur.daemon = True
		self.serveur.start()
		self.pere.mise_a_jour_serveur(self.serveur)