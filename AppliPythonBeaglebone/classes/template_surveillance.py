# coding: utf8
import threading
from collections import deque

#On ajoute le dossier ou l'on a déclaré notre nouvelle classe au Python path
import sys
sys.path.insert(0, '/root/R2D2/classes/sous-classes')

import classe

class Template_surveillance(threading.Thread):
	def __init__(self,controleur,filename="/var/log/surveillance_template_partage.log"):
		#Initialisation du thread lui-même
		threading.Thread.__init__(self)
		#On définit l'élément parent controleur
		self.pere   =controleur
		self.queue_input_reception = deque()
		self.queue_output_emission = deque()
		self.classe=classe.classe(self.queue_input_reception,self.queue_output_emission,stopevent)
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
		self.logger2.debug("Démarrage du thread de Surveillance_classe")

		self.classe.daemon=True
		#On lance le thread du serveur que l'on surveille
		self.classe.start()
		self.logger2.debug("Thread classe démarré")


	def run(self):
		try:
			self.logger2.debug("Surveillance_serveur running")
			sleep(0.01)
			self.logger2.debug("Serveur initialized, commencing surveillance")
			#Messages servant à logger l'activité du classe
			self.message_input = ""
			self.message_output = ""
			self.statut_classe = "vivant"
			#Tant que le controleur n'ordonne pas l'arrêt
			while not self.stoprequest.isSet():
				try:
					self.log1 = False
					self.log2 = False
					#Si le message de la pile d'émission de la classe a changé par rapport à celui que l'on a retenu, on le change
					#et on enclenche la variable permettant le log
					if(self.message_input != self.classe.input[0]):
						self.message_input = self.classe.input[0]
						self.log1 = True
				except IndexError:
					#variable "dummy", juste parce qu'il faut faire quelque chose dans cet except
					self.i = 1
				try:
					#Si le message de la pile de réception de la classe a changé par rapport à celui que l'on a retenu, on le change
					#et on enclenche la variable permettant le log
					if(self.message_output != self.classe.output[0]):
						self.message_output = self.classe.output[0]
						self.log2 = True
				except IndexError:
					#variable "dummy", juste parce qu'il faut faire quelque chose dans cet except
					self.i = 1
				#On regarde si le thread classe est vivant
				self.classe_vivant = self.classe.is_alive()
				if(not self.classe_vivant):
					#Si le thread est mort, on enclenche les opérations de maintenance et on log l'incident
					self.statut_classe = "mort"
					self.kill()
					self.logger2.critical("Le thread classe ne répondait plus, il a été tué et réinstancié")
				else:
					self.statut_classe = "vivant"
				#Si on a quelque chose à logger
				if(self.log1 | self.log2):
					self.logger2.info("Le thread classe est "+self.statut_classe+" et les messages suivants sont en attente de traitement : Emission serveur:"+str(self.message_input)+"///// Réception serveur:"+str(self.message_output))
				#On dort 20 ms
				sleep(0.00002)
		finally:
			self.classe.stop()


	def kill(self):
		#on efface la classe défectueuse
		del self.classe
		#On en crée une nouvelle 
		self.classe=classe(self.input_template_partage,self.output_template_partage)
		#On met le Thread en mode "daemon", c'est à dire qu'il passe à l'arrière plan
		#et s'arretera si son thread parent s'arrête => permet l'arrêt en cascade du programme
		self.classe.daemon = True
		#On démarre notre classe
		self.classe.start()
		#On prévient le controleur de mettre à jour la classe de traitement principal
		self.pere.mise_a_jour_classe(self.classe)

	def stop(self):
		self.stoprequest.set()