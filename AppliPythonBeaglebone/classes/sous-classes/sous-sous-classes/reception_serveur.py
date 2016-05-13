#/usr/bin/env python
# -*-coding:Utf-8 -*
import socket
import threading
import Queue
from time import sleep
class Reception_Serveur(threading.Thread):
	"""
	Classe englobant le socket serveur permettant la transmission d'infos du smartphone au robot
		Contient:
			Socket serveur réceptionnant les informations du smartphone
			
		Prend en entrée:
			serveru : L'élément parent Serveur, contenant à la fois l'émission et la réception
			queue_output : Une queue d'items output, les informations que le serveur transmet au controleur : les commandes demandées par smartphone
			stopevent : Une variable provoquant l'arrêt du thread, passée depuis le thread parent, qui permet l'arrêt en cascade
	"""
	def __init__(self,serveur, queue_output, stopevent):
		#Initialisation du thread lui-même		
		threading.Thread.__init__(self)
		#Les informations recues par le socket seront empilées ici
		self.output = queue_output
		self.serveur = serveur
		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = stopevent
		
		### Socket serveur
		self.socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#On définit le socket comme étant réutilisable, afin de permettre de multiples connexions
		self.socket_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#Adresse : localhost, port utilisé : 12800
		self.socket_serveur.bind(('', 12800))
		#On permet de multiples connexions au serveur
		self.socket_serveur.listen(9999)


	def run(self):
		sleep(1)
		#Compteur permettant de voir si un socket ne répond pas
		compteur_attente = 0
		#Pour le moment, on n'a pas recu de connexions, on attend
		attente = True
		#Tant que le controleur ne demande pas au thread de s'arreter
		try:
			while not self.stoprequest.isSet():
				#Si on nous demande d'attendre, on scrute le socket pour accepter une connexion
				if(attente):
					#On attend une connexion et on l'accepte
					self.connexion_avec_client, self.infos_connexion = self.socket_serveur.accept()
					#On transmet les informations au serveur
					self.serveur.infos_connexion = self.infos_connexion
					#On attend plus
					attente = False
				try:
					#On attend les informations du smartphone
					#On déclare un timeout de 50 ms afin que la réception lève une exception timeout si aucune donnée n'est transmise durant ces 50 ms
					#Au bout de 1000 exceptions (5 secondes), on estime que l'on a perdu la connexion et on ferme le socket
					self.socket_serveur.settimeout(0.05)
					chaine = ""
					continuer = True
					enregistrer = False
					#On attend du JSON très simple sous la forme {"mode":"0","vitesseD":"127",....}
					#on scrute donc caractère par caractère pour enregistrer la chaine
					while continuer:
						msg = self.connexion_avec_client.recv(1)
						if(msg == "{"):
							enregistrer = True
						elif(msg == "}"):
							continuer = False
						if(enregistrer):
							chaine += msg
					#print(chaine)
					#On enlève le timeout du socket, afin de ne pas fermer un socket fonctionnant à l'évidence
					self.socket_serveur.settimeout(None)
					#Si 5 secondes sans informations se sont écoulées
					#Ou si le smartphone a envoyé un JSON déclenchant la déconnexion
					#On ferme le socket et on retourne dans l'état d'attente
					if((compteur_attente > 1000) | (chaine =='{"connexion":"false"}')):
						self.socket_serveur.shutdown(socket.SHUT_WR)
						attente = True
						compteur_attente = 0
						#On remet les informations de connexion du serveur à zéro, afin d'arreter l'émission
						self.serveur.infos_connexion = (('',''))
					#Si la chaine contient un message significatif, on le transmet
					elif(chaine != ""):
						self.output.appendleft((chaine))
				except socket.timeout:
					compteur_attente += 1
					continue
				except socket.error as msg:
					#Si une erreur se déclenche, on ferme le socket par prévention
					self.socket_serveur.shutdown(socket.SHUT_WR)
					print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB Socket fermé")
					attente = True
					#On remet les informations de connexion du serveur à zéro, afin d'arreter l'émission
					self.serveur.infos_connexion = (('',''))
					continue
		finally:
			self.socket_serveur.close()

	def stop(self):
		self.stoprequest.set()