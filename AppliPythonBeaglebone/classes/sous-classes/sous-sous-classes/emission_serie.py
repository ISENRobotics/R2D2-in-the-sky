# coding: utf8
import Adafruit_BBIO.UART as UART
import serial

import threading

import constants

from time import sleep
###   Préparation du programme

class Emission_Serie(threading.Thread):
	"""
	Classe regroupant l'émission par liaison série avec les moteurs
		Prend en entrée:
			queue_input : Une queue d'items input, les informations que le controleur envoie à la classe Série : les paramètres des commandes
			stopevent : Une variable provoquant l'arrêt du thread, passée depuis le thread parent, qui permet l'arrêt en cascade
			sel_uart : variable sélectionnant la liaison série à ouvrir, valant 1 par défaut (UART1)
	"""

	def __init__(self, queue_input, stopevent, sel_uart, occupe):
		#Les liaisons valides sont les liaisons 1,2,4
		if(sel_uart not in [1,2,4]):
				return "Erreur : la liaison série spécifiée n'est pas valide"
		#Initialisation du thread lui-même
		threading.Thread.__init__(self)
		#Les informations à émettre sur la liaison série
		self.input = queue_input
		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = stopevent

		#Variable empechant l'empiêtement des classes Série (pas de lecture quand envoi, et pas d'envoi quand lecture)
		self.occupe = occupe
		### Liaison série
		#On choisit la liaison série spécifiée, sinon la liaison série 1 par défaut
		UART.setup("UART"+str(sel_uart))

		#Ouverture de la liaison série
		#le parametre stopbits DOIT etre égal à 1, le mettre à deux entraine une incompréhension par le controleur des moteurs des ordres à envoyer
		self.ser = serial.Serial(port = "/dev/ttyO"+str(sel_uart), baudrate=38400,bytesize=8, stopbits=1,timeout=None)
		#On ferme la liaison série instanciée, afin de ne pas occuper constamment le canal
		self.ser.close()

	def run(self):
		sleep(1)
		#Tant que le controleur ne demande pas au thread de s'arreter
		try:
			while not self.stoprequest.isSet():
				try:
					self.infos_envoyees = False
					#On regarde si un nouveau jeu d'instructions a été mis en queue
					#Les jeux d'instructions se décomposent de la manière suivante : 
					#	infos[0] : valeur du mode de fonctionnement demandé
					#	infos[1] : valeur de la vitesse 1 demandée en mode paysage / valeur de la vitesse des deux moteurs en mode portrait
					#	infos[2] : valeur de la vitesse 2 demandée en mode paysage / valeur de turn en mode portrait
					#	infos[3] : valeur de l'acceleration demandée (pas encore gérée dans l'application, donc mise à deux par défaut)
					infos = ""
					#print("Longueur de la pile d'entrée : "+str(len(self.input)))
					infos = self.input.pop()
					print("Longueur de la pile d'entrée après pop : "+str(len(self.input)))
					longueur = len(infos)
					print("Informations recues dans l'émission Série : "+str(infos))
					print("Longueur de l'information série : "+str(longueur))
					while(not self.infos_envoyees):
						print("on tente l'envoi d'informations")
						if(longueur == 4):
							if(not self.occupe):
								self.occupe = True
								print("L'envoi occupe la liaison série")
								self.ordre_moteurs(constants.SET_MODE,infos[0])
								self.ordre_moteurs(constants.SET_SPEED_1,infos[1])
								self.ordre_moteurs(constants.SET_SPEED_2,infos[2])
								self.ordre_moteurs(constants.SET_ACCELERATION,infos[3])
								self.occupe = False
								self.infos_envoyees = True
							else:
								continue
						elif(longueur == 2):
							#print("on rentre ou il faut")
							#print("Une seule info détectée : "+str(infos[0])) 
							if(not self.occupe):
								self.occupe = True
								print("L'envoi occupe la liaison série")
								self.ordre_moteurs(infos[0],infos[1])
								self.occupe = False
								self.infos_envoyees = True
							else:
								continue
				except IndexError:
					#Si le pop de la queue input a provoqué un IndexError, ca veut dire que la pile est vide, on continue
					continue
		finally:
			#On ferme la liaison série quand on demande au thread de s'arrêter
			self.ser.close()

	#Fonction chargée d'effectuer l'envoi sur la liaison série des commandes moteurs
	def ordre_moteurs(self,commande,parameter):
		self.ser.open()
		if self.ser.isOpen():
			#Si le paramètre est positif, la conversion en hexadécimal ne pose pas de problèmes
			if(parameter >= 0):
				if(parameter == 5000):
					#Paramétre particulier envoyé par la surveillance série, dummy
					print("Commande envoyée dans émission (surveillance série) : "+str(constants.CMD+commande))
					self.ser.write(bytearray.fromhex(constants.CMD+commande))
				else:
					#Utilisation normale
					param = format(parameter, '#04x')[2:]
					#Un chiffre hexadécimal comprend nécessairement au minimum DEUX lettres.
					#Donc si le paramètre est compris entre 0 et 9, on lui ajoute un 0 devant.
					#9 devient 09 
					if(len(param) == 1):
						param = "0"+param
					#print("Commande envoyée dans émission (fonctionnement normal) : "+str(constants.CMD+commande+param))
					#On écrit le mot de synchronisation, puis la commande et enfin son paramètre
					self.ser.write(bytearray.fromhex(constants.CMD+commande+param))
			else:
				#Si le paramètre est négatif, il faut forcer le bit de signe à 1 pour que le controleur
				#des moteurs le prenne en compte
				parameter += 128
				param = format(parameter, '#04x')[3:]
				if(len(param) == 1):
					param = "0"+param
				self.ser.write(bytearray.fromhex(constants.CMD+commande+param))
		else:
			#Si la liaison série n'est pas ouverte, on renvoie l'erreur 1000 (n'arrive jamais normalement en conditions d'utilisations normales)
			print("Problème !")
		self.ser.close()

	#Fonction chargée de permettre l'arret du thread depuis l'extérieur de la classe
	def stop(self):
		self.stoprequest.set()