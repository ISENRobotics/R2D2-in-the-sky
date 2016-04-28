#/usr/bin/env python
# -*-coding:Utf-8 -*
import socket
import json
import threading
import Queue
from collections import deque

from time import sleep

import sys
sys.path.insert(0, '/root/R2D2/classes/sous-classes/sous-sous-classes')

from emission_serveur import Emission_Serveur
from reception_serveur import Reception_Serveur

class Serveur(threading.Thread):
	"""
	Classe englobant le socket serveur permettant la transmission d'infos du robot au smartphone, et inversement
		Contient:
			Socket serveur réceptionnant les informations du smartphone
			Socket client transmettant les informations vers le smartphone

		Prend en entrée:
			queue_input : Une queue d'items input, les informations que le controleur envoie à la classe Serveur : le retour des commandes de la liaison série
			queue_output : Une queue d'items output, les informations que le serveur transmet au controleur : les commandes demandées par smartphone
			
	"""
	def __init__(self, queue_input, queue_output):
		threading.Thread.__init__(self)
		self.input = queue_input
		self.output = queue_output

		self.queue_input_reception = deque()
		self.queue_output_emission = deque()

		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = threading.Event()
		self.thread_emission_serveur = Emission_Serveur(self.queue_output_emission)
		self.thread_reception_serveur = Reception_Serveur(self.queue_input_reception)
		self.thread_emission_serveur.start()
		self.thread_reception_serveur.start()
		

	def run(self):
		sleep(1)
		#Tant que le controleur ne demande pas au thread de s'arreter
		while not self.stoprequest.isSet():
			try:
				#On regarde si on a recu des informations, si oui, on les transmet à l'algorithmique
				infos = self.queue_input_reception.pop()
				print("Dans la classe Serveur, coté réception : "+str(infos))
				self.output.appendleft(infos)
				print("On met dans la pile "+str(infos))
			except IndexError:
				try:
					#Si on n'a pas recu d'informations dans le temps imparti, on regarde si un message à envoyer est arrivé
					infos = self.input.pop()
					print("Dans la classe Serveur, coté émission : "+str(infos))
					self.queue_output_emission.appendleft(infos)
					print("On met dans la pile "+str(infos))
				except IndexError:
					continue

	def stop(self):
		self.stoprequest.set()