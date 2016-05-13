#/usr/bin/env python
# -*-coding:Utf-8 -*
import socket, errno
import threading

from time import sleep

class Emission_Serveur(threading.Thread):
	"""
	Classe englobant le socket serveur permettant la transmission d'infos du robot au smartphone, et inversement
		Contient:
			Socket serveur réceptionnant les informations du smartphone
			Socket client transmettant les informations vers le smartphone

		Prend en entrée:
			queue_input : Une queue d'items input, les informations que le controleur envoie à la classe Serveur : le retour des commandes de la liaison série
			queue_output : Une queue d'items output, les informations que le serveur transmet au controleur : les commandes demandées par smartphone
			
	"""
	def __init__(self, serveur,queue_input,stopevent):
		threading.Thread.__init__(self)
		self.input = queue_input
		self.serveur = serveur
		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = stopevent
		
		
	def run(self):
		sleep(1)
		self.connecte = False
		while (self.serveur.infos_connexion[0] == '') & (self.serveur.infos_connexion[1] == ''):
			continue
		self.socket_client = self.serveur.thread_reception_serveur.connexion_avec_client
		print(self.socket_client)
		try:
			self.i = 0
			while not self.stoprequest.isSet():
				### Socket client
				#On crée le socket de connexion
				self.socket_client = self.serveur.thread_reception_serveur.connexion_avec_client
				try:
					infos = self.input.pop()
					self.socket_client.send(infos)
					continue
				except socket.error as serr:
					if serr.errno != errno.ECONNREFUSED:
						# Not the error we are looking for, re-raise
						raise serr
					print(str(serr))
					sleep(1)
					continue
				except IndexError:
					continue
		finally:
			self.socket_client.close()

	def stop(self):
		self.stoprequest.set()
