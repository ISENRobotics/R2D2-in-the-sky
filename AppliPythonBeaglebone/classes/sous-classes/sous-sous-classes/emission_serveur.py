#/usr/bin/env python
# -*-coding:Utf-8 -*
import socket, errno
import threading

from time import sleep

class Emission_Serveur(threading.Thread):
	"""
	Classe englobant le socket serveur permettant la transmission d'infos du robot au smartphone
		Contient:
			Socket client transmettant les informations vers le smartphone, partagé avec la classe Réception_serveur via leur élément parent Serveur

		Prend en entrée:
			serveur : L'élément parent qui contient à la fois l'émission et la réception, utilisé afin de partager le même socket
			queue_input : Une queue d'items input, les informations que le controleur envoie à la classe Serveur : le retour des commandes de la liaison série ou les problèmes rencontrés
			stopevent :  Une variable provoquant l'arrêt du thread, passée depuis le thread parent, qui permet l'arrêt en cascade
	"""
	def __init__(self, serveur,queue_input,stopevent):
		threading.Thread.__init__(self)
		self.input = queue_input
		self.serveur = serveur
		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = stopevent
		
		
	def run(self):
		#On sleep afin d'assurer une plus grande rapidité d'initialisation aux autres classes
		sleep(1)
		#On n'est pas encore connecté
		self.connecte = False
		try:
			while not self.stoprequest.isSet():
				#Tant que le serveur ne dispose pas d'informations de connexion, cela veut dire que l'application
				#smartphone ne s'est pas encore connecté au programme
				#On boucle en attendant
				while (self.serveur.infos_connexion[0] == '') & (self.serveur.infos_connexion[1] == ''):
					continue
				### Socket client
				#On crée le socket de connexion
				#On fait partager le socket de la classe Réception_serveur à la classe Émission_serveur, afin d'assurer l'envoi vers la bonne personne
				self.socket_client = self.serveur.thread_reception_serveur.connexion_avec_client
				try:
					#On récupére les infos à envoyer s'il y en a
					infos = self.input.pop()
					self.socket_client.send(infos)
					continue
				except socket.error as serr:
					if serr.errno != errno.ECONNREFUSED:
						# Not the error we are looking for, re-raise
						raise serr
					print(str(serr))
					#Si la connection a été refusée, on dort 1 seconde et on recommence
					sleep(1)
					continue
				except IndexError:
					continue
		finally:
			self.socket_client.close()

	def stop(self):
		self.stoprequest.set()
