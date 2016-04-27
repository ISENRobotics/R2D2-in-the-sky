#/usr/bin/env python
# -*-coding:Utf-8 -*
import socket
import json
import threading
import Queue

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

		queue_input_reception = Queue.Queue()
		queue_output_emission = Queue.Queue()

		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = threading.Event()
		self.thread_emission_serveur = Emission_serveur(queue_output_emission)
		self.thread_reception_serveur = Reception_serveur(queue_input_reception)
		thread_emission_serveur.start()
		thread_reception_serveur.start()
		

	def run(self):
		#Tant que le controleur ne demande pas au thread de s'arreter
		while not self.stoprequest.isSet():
			try:
				#On regarde si on a recu des informations, si oui, on les transmet à l'algorithmique
				infos = self.queue_input_reception.get(True,0.005)
				self.output.put(infos)
			except Queue.Empty:
				try:
					#Si on n'a pas recu d'informations dans le temps imparti, on regarde si un message à envoyer est arrivé
					infos = self.input.get(True,0.005)
					self.queue_output_emission.put(infos)
				except Queue.Empty:
					continue