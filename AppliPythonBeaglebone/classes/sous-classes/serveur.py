# coding: utf8
import socket
import threading
from collections import deque

from time import sleep

import sys
sys.path.insert(0, '/root/R2D2/classes/sous-classes/sous-sous-classes')

from emission_serveur import Emission_Serveur
from reception_serveur import Reception_Serveur

class Serveur(threading.Thread):
	"""
	Classe englobant le socket serveur
		Contient:
			Socket serveur réceptionnant les informations du smartphone
			Socket client transmettant les informations vers le smartphone

		Prend en entrée:
			queue_input : Une queue d'items input, les informations que le controleur envoie à la classe Serveur : le retour des commandes de la liaison série
			queue_output : Une queue d'items output, les informations que le serveur transmet au controleur : les commandes demandées par smartphone
			stopevent : Une variable provoquant l'arrêt du thread, passée depuis le thread parent, qui permet l'arrêt en cascade
	"""
	def __init__(self, controleur, queue_input, queue_output,stopevent):
		#Initialisation du thread lui-même		
		threading.Thread.__init__(self)
		self.pere = controleur
		self.input = queue_input
		self.output = queue_output
		self.infos_connexion = (('',''))

		self.queue_input_reception = deque()
		self.queue_output_emission = deque()

		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = threading.Event()
		self.thread_reception_serveur = Reception_Serveur(self,self.queue_input_reception,stopevent)
		self.thread_reception_serveur.daemon = True
		self.thread_emission_serveur = Emission_Serveur(self,self.queue_output_emission,stopevent)
		self.thread_emission_serveur.daemon = True
		self.thread_emission_serveur.start()
		self.thread_reception_serveur.start()
		

	def run(self):
		sleep(1)
		#Tant que le controleur ne demande pas au thread de s'arreter
		try:
			while not self.stoprequest.isSet():
				try:
					#On regarde si on a recu des informations, si oui, on les transmet à l'traitement
					infos = self.queue_input_reception.pop()
					self.output.appendleft(infos)
				except IndexError:
					try:
						#Si on n'a pas recu d'informations dans le temps imparti, on regarde si un message à envoyer est arrivé
						infos = self.input.pop()
						self.queue_output_emission.appendleft(infos)
					except IndexError:
						continue
		finally:
			self.thread_reception_serveur.stop()
			self.thread_emission_serveur.stop()

	def stop(self):
		self.stoprequest.set()