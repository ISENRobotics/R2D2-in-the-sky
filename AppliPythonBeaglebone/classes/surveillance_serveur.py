# coding: utf8
import threading
import logging
from datetime import datetime
from time import sleep
import Queue

import serveur

class Surveillance_serveur(threading.Thread):
	def __init__(self,controleur,filename="surveillance_serveur.log"):
		self.pere   =controleur
		self.queue_input_reception = Queue.Queue()
		self.queue_output_emission = Queue.Queue()
		self.serveur=serveur.Serveur(self.queue_input_reception,self.queue_output_emission)
		self.stoprequest = threading.Event()
		logging.basicConfig(filename=filename,level=logging.DEBUG)
		logging.debug("Démarrage du thread de Surveillance_serveur")
		self.serveur.start()

	def kill(self):
		del self.serveur
		self.serveur=Serveur()
		self.pere.mise_a_jour_serveur(self.serveur)

	def run(self):
		sleep(0.01)
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
					kill()
					logging.critical("Le thread Serie ne répondait plus, il a été tué et réinstancié")
				else:
					statut_serveur = "vivant"
				maintenant = datetime.now()
				logging.debug("Le "+maintenant.day+"/"+maintenant.month+"/"+maintenant.year+" à "+maintenant.hour+":"+maintenant.minute+":"+maintenant.second+", le thread serie est "+statut_serveur+" et les messages suivants sont en attente de traitement : Emission série:"+message_input+"///// Réception série:"+message_output)
			except Queue.Empty:
				continue