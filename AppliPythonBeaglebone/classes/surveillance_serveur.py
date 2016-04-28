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
		logger2 = logging.getLogger('R2D2.surveillance_serveur')
		formatter = logging.Formatter('%(asctime)s : %(message)s')
		fileHandler = logging.FileHandler(filename, mode='w')
		fileHandler.setFormatter(formatter)
		streamHandler = logging.StreamHandler()
		streamHandler.setFormatter(formatter)

		logger2.setLevel(logging.DEBUG)
		logger2.addHandler(fileHandler)
		logger2.addHandler(streamHandler)
		logger2.debug("Démarrage du thread de Surveillance_serveur")

		self.serveur.start()
		logger2.debug("Thread serveur démarré")

	def run(self):
		logger2.debug("Surveillance_serveur running")
		sleep(0.01)
		logger2.debug("Serveur initialized, commencing surveillance")
		#Messages servant à logger l'activité du serveur
		message_input = ""
		message_output = ""
		while not self.stoprequest.isSet():
			try:
				#Routine de logging d'activité du serveur
				if(message_input != self.serveur.input[0]):
					message_input = self.serveur.input[0]
				if(message_output != self.serveur.output[0]):
					message_output = self.serveur.output[0]
				serveur_vivant = self.serveur.is_alive()
				if(not serveur_vivant):
					statut_serveur = "mort"
					self.kill()
					logger2.critical("Le thread Serie ne répondait plus, il a été tué et réinstancié")
				else:
					statut_serveur = "vivant"
				maintenant = datetime.now()
				logger2.debug("Le "+maintenant.day+"/"+maintenant.month+"/"+maintenant.year+" à "+maintenant.hour+":"+maintenant.minute+":"+maintenant.second+", le thread serie est "+statut_serveur+" et les messages suivants sont en attente de traitement : Emission série:"+message_input+"///// Réception série:"+message_output)
			except IndexError:
				continue

	def stop(self):
		self.stoprequest.set()


	def kill(self):
		del self.serveur
		self.serveur=Serveur()
		self.pere.mise_a_jour_serveur(self.serveur)