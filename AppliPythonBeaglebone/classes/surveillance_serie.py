# coding: utf8
import threading
import logging
from time import sleep
from collections import deque

import sys
sys.path.insert(0, '/root/R2D2/classes/sous-classes')
sys.path.insert(0, '/root/R2D2/classes/sous-classes/sous-sous-classes')

import serie
import constants


class Surveillance_serie(threading.Thread):
	"""
	Classe englobant la surveillance du Thread global de la liaison série
		Contient:
			Une classe Série, partagée avec la classe traitement

		Prend en entrée:
			controleur : le controleur général du programme, contenant toutes les classes principales
			stopevent : Une variable provoquant l'arrêt du thread, passée depuis le thread parent, qui permet l'arrêt en cascade
			filename : le nom du fichier de logs créé, valeur par défaut : surveillance_serie.log
	"""
	def __init__(self,controleur,stopevent,filename="/var/log/R2D2_surveillance_serie.log"):
		#Initialisation du thread lui-même
		threading.Thread.__init__(self)
		#On définit l'élément parent controleur
		self.pere   =controleur
		self.queue_input_reception = deque()
		self.queue_output_emission = deque()
		self.serie=serie.Serie(self.queue_input_reception,self.queue_output_emission,stopevent)
		self.stoprequest = stopevent
		#Définition du logger de la classe
		#Affiche les messages d'erreurs et critiques sur la console
		#Enregistre tous les messages (de DEBUG à CRITICAL) dans le fichier de logs
		self.logger1 = logging.getLogger('R2D2.surveillance_serie')
		self.logger1.setLevel(logging.DEBUG)
		self.formatter = logging.Formatter('%(asctime)s : %(message)s')
		self.fileHandler = logging.FileHandler(filename, mode='w')
		self.fileHandler.setFormatter(self.formatter)
		self.streamHandler = logging.StreamHandler()
		self.streamHandler.setFormatter(self.formatter)
		self.streamHandler.setLevel(logging.ERROR)

		self.logger1.addHandler(self.fileHandler)
		self.logger1.addHandler(self.streamHandler)
		self.logger1.debug("Démarrage du thread de Surveillance_serie")
		self.serie.daemon = True
		#On lance le thread de la liaison série que l'on surveille
		self.serie.start()
		self.logger1.debug("Thread série démarré")

	def run(self):
		try:
			self.logger1.debug("Surveillance_serie running")
			sleep(0.01)
			self.logger1.debug("Serie initialized, commencing surveillance")
			#Messages servant à logger l'activité de la liaison série
			self.message_input = ""
			self.message_output = ""
			self.statut_serveur = "vivant"
			#Tant que le controleur n'ordonne pas l'arrêt
			while not self.stoprequest.isSet():
				try:
					self.log1 = False
					self.log2 = False
					#Si le message de la pile d'émission de la liaison série a changé par rapport à celui que l'on a retenu, on le change
					#et on enclenche la variable permettant le log
					if(self.message_input != self.serie.input[0]):
						self.message_input = self.serie.input[0]
						self.log1 = True
				except IndexError:
					#variable "dummy", juste parce qu'il faut faire quelque chose dans cet except
					self.i = 1
				try:
					#Si le message de la pile de réception de la liaison série a changé par rapport à celui que l'on a retenu, on le change
					#et on enclenche la variable permettant le log
					if(self.message_output != self.serie.output[0]):
						self.message_output = self.serie.output[0]
						self.log2 = True
				except IndexError:
					#variable "dummy", juste parce qu'il faut faire quelque chose dans cet except
					self.i = 1
				#On regarde si le thread Série est vivant
				self.serie_vivante = self.serie.is_alive()
				if(not self.serie_vivante):
					#Si le thread est mort, on enclenche les opérations de maintenance et on log l'incident
					self.statut_serie = "mort"
					self.kill()
					self.logger1.critical("Le thread Serie ne répondait plus, il a été tué et réinstancié")
				else:
					self.statut_serie = "vivant"
				#Si on a quelque chose à logger
				if(self.log1 | self.log2):
					self.logger1.info("Le thread serie est "+self.statut_serie+" et les messages suivants sont en attente de traitement : Emission série:"+str(self.message_input)+"///// Réception série:"+str(self.message_output))
				
				#Valeurs particulières inatteignables
				self.infos_volts = 9999
				self.infos_current1 = 9999
				self.infos_current2 = 9999
				self.infos_version = 9999

				while(self.infos_volts == 9999):
					self.infos_volts = self.informations(constants.GET_VOLTS)
					if(self.infos_volts == 9999):
						sleep(0.05)
				while(self.infos_current1 == 9999):
					self.infos_current1 = self.informations(constants.GET_CURRENT_1)
					if(self.infos_current1 == 9999):
						sleep(0.05)
				while(self.infos_current2 == 9999):
					self.infos_current2 = self.informations(constants.GET_CURRENT_2)
					if(self.infos_current2 == 9999):
						sleep(0.05)
				while(self.infos_version == 9999):
					self.infos_version = self.informations(constants.GET_VERSION)
					if(self.infos_version == 9999):
						sleep(0.05)
				self.logger1.info("Informations à propos des moteurs : Voltage recu : "+str((float)(ord(self.infos_volts))/10.0)+" V //Intensité du courant du moteur 1 : "+str((float)(ord(self.infos_current1))/10.0)+" A //Intensité du courant du moteur 2 : "+str((float)(ord(self.infos_current2))/10.0)+" A ///Version du software logiciel : "+str((float)(ord(self.infos_version))))
				self.pere.traitement.serveur.input.appendleft('Voltage : '+str((float)(ord(self.infos_volts))/10.0)+' V //Courant 1 : '+str((float)(ord(self.infos_current1))/10.0)+' A //Courant 2 : '+str((float)(ord(self.infos_current2))/10.0)+' A /// Version soft: '+str((float)(ord(self.infos_version)))+'\n')

				#On dort 20 ms
				sleep(0.5)
		finally:
			self.serie.stop()

	def stop(self):
		self.stoprequest.set()


	#Fonction de maintenance du thread Série, déclenchée en cas d'incident
	#On efface l'ancienne instance de Série, on en instancie une nouvelle et on la démarre
	#Enfin, on notifie le controleur que la liaison série a changée
	def kill(self):
		del self.serie
		self.serie=Serie(self.queue_input_reception,self.queue_output_emission,self.stoprequest)
		self.serie.daemon = True
		self.serie.start()
		self.pere.mise_a_jour_serie(self.serie)

	def informations(self,commande):
		#print("On envoie à la liaison Série depuis la surveillance série : "+str(commande))
		self.serie.input.appendleft((commande,5000))
		while(True):
			try :
				infos = self.serie.output.pop()
				if(infos != ''):
					break
			except IndexError:
				continue
		return infos