#/usr/bin/env python
# -*-coding:Utf-8 -*
import socket
import threading
import Queue
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
	def __init__(self, serveur,queue_input):
		threading.Thread.__init__(self)
		self.input = queue_input

		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = threading.Event()
		
		### Socket client
		#On crée le socket de connexion
		self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#On connecte le socket sur l'adresse et le port désiré
		#Idée : attribuer une IP fixe grâce au routeur au téléphone Android, voir réseau en 255.255.255.252
		self.socket_client.connect((serveur.infos_connexion[0], serveur.infos_connexion[1]))

	def run(self):
		sleep(1)
		while not self.stoprequest.isSet():
			try:
				infos = self.input.pop()
				print("Dans la classe Emission serveur : "+str(infos))
				#self.socket_client.send(infos)
				continue
			except IndexError:
				continue

	def stop(self):
		self.stoprequest.set()
