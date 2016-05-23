# coding: utf8
import threading
import logging
from time import sleep
from collections import deque

import sys
sys.path.insert(0, '/root/R2D2/classes/sous-classes')

import serveur

class Surveillance_serveur(threading.Thread):
	"""
	Classe englobant la surveillance du Thread global du serveur de communications
		Contient:
			Une classe Serveur, partagée avec la classe traitement

		Prend en entrée:
			controleur : le controleur général du programme, contenant toutes les classes principales
			stopevent : Une variable provoquant l'arrêt du thread, passée depuis le thread parent, qui permet l'arrêt en cascade
			filename : le nom du fichier de logs créé, valeur par défaut : surveillance_serveur.log
	"""
	def __init__(self,controleur,stopevent,filename="/var/log/R2D2_surveillance_serveur.log"):
		#Initialisation du thread lui-même
		threading.Thread.__init__(self)
		#On définit l'élément parent controleur
		self.pere   =controleur
		self.queue_input_reception = deque()
		self.queue_output_emission = deque()
		self.serveur=serveur.Serveur(self.pere,self.queue_input_reception,self.queue_output_emission,stopevent)
		self.stoprequest = stopevent
		#Définition du logger de la classe
		#Affiche les messages d'erreurs et critiques sur la console
		#Enregistre tous les messages (de DEBUG à CRITICAL) dans le fichier de logs
		self.logger2 = logging.getLogger('R2D2.surveillance_serveur')
		self.logger2.setLevel(logging.DEBUG)
		self.formatter = logging.Formatter('%(asctime)s : %(message)s')
		self.fileHandler = logging.FileHandler(filename, mode='w')
		self.fileHandler.setFormatter(self.formatter)
		self.streamHandler = logging.StreamHandler()
		self.streamHandler.setFormatter(self.formatter)
		self.streamHandler.setLevel(logging.ERROR)

		self.logger2.addHandler(self.fileHandler)
		self.logger2.addHandler(self.streamHandler)
		self.logger2.debug("Démarrage du thread de Surveillance_serveur")

		self.serveur.daemon=True
		#On lance le thread du serveur que l'on surveille
		self.serveur.start()
		self.logger2.debug("Thread serveur démarré")

	def run(self):
		try:
			self.logger2.debug("Surveillance_serveur running")
			sleep(0.01)
			self.logger2.debug("Serveur initialized, commencing surveillance")
			#Messages servant à logger l'activité du serveur
			self.message_input = ""
			self.message_output = ""
			self.statut_serveur = "vivant"
			#Tant que le controleur n'ordonne pas l'arrêt
			while not self.stoprequest.isSet():
				try:
					self.log1 = False
					self.log2 = False
					#Si le message de la pile d'émission du serveur a changé par rapport à celui que l'on a retenu, on le change
					#et on enclenche la variable permettant le log
					if(self.message_input != self.serveur.input[0]):
						self.message_input = self.serveur.input[0]
						self.log1 = True
				except IndexError:
					#variable "dummy", juste parce qu'il faut faire quelque chose dans cet except
					self.i = 1
				try:
					#Si le message de la pile de réception du serveur a changé par rapport à celui que l'on a retenu, on le change
					#et on enclenche la variable permettant le log
					if(self.message_output != self.serveur.output[0]):
						self.message_output = self.serveur.output[0]
						self.log2 = True
				except IndexError:
					#variable "dummy", juste parce qu'il faut faire quelque chose dans cet except
					self.i = 1
				#On regarde si le thread Serveur est vivant
				self.serveur_vivant = self.serveur.is_alive()
				if(not self.serveur_vivant):
					#Si le thread est mort, on enclenche les opérations de maintenance et on log l'incident
					self.statut_serveur = "mort"
					self.kill()
					self.logger2.critical("Le thread Serveur ne répondait plus, il a été tué et réinstancié")
				else:
					self.statut_serveur = "vivant"
				#Si on a quelque chose à logger
				if(self.log1 | self.log2):
					self.logger2.info("Le thread serveur est "+self.statut_serveur+" et les messages suivants sont en attente de traitement : Emission serveur:"+str(self.message_input)+"///// Réception serveur:"+str(self.message_output))
				#On dort 20 ms
				sleep(0.00002)
		finally:
			self.serveur.stop()

	def stop(self):
		self.stoprequest.set()

	#Fonction de maintenance du thread Serveur, déclenchée en cas d'incident
	#On efface l'ancienne instance de Serveur, on en instancie une nouvelle et on la démarre
	#Enfin, on notifie le controleur que la liaison série a changée
	def kill(self):
		del self.serveur
		self.serveur=Serveur(self.queue_input_reception,self.queue_output_emission,self.stoprequest)
		self.serveur.daemon = True
		self.serveur.start()
		self.pere.mise_a_jour_serveur(self.serveur)