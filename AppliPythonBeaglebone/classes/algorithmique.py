# coding: utf8
import threading
import logging
import json
from datetime import datetime
from time import sleep

import serveur
import serie

class Algorithmique(threading.Thread):
	def __init__(self,controleur):
		self.serveur = controleur.surveillance_serveur.serveur 
		self.serie   = controleur.surveillance_serie.serie;
		self.stoprequest = threading.Event()

	def run(self):
		while not self.stoprequest.isSet():
			try:
				infos = self.serveur.output.get(True,0.005)
				#Traitement des infos

				self.serie.output.put(infos)
			except Queue.Empty:
				try:
					#Si on n'a pas recu d'informations dans le temps imparti, on regarde si un message à envoyer est arrivé
					infos = self.serie.output.get(True,0.005)
					#Traitement des infos

					self.serveur.intput.put(infos)
				except Queue.Empty:
					continue


	def get_serial(self):
		return self.ser.name

	def verif_trame_recu(self,trame):
		try:
			msg_recu_json = json.loads(trame)
			result_mode = 0
			result_droite = 0
			result_gauche = 0
			if('mode' in msg_recu_json):
				result_mode = verif_commande_SETMODE(int(msg_recu_json['mode']))
				if(result_mode):
					self.MODE = int(msg_recu_json['mode']);
					#on commence par assigner des vitesses telles que les moteurs ne bougent pas
					if(self.MODE %2 == 0):
						default = 128
					else:
						default = 0
					if('vitesseD' in msg_recu_json & 'vitesseG' in msg_recu_json):
						vitesse_gauche = int(msg_recu_json['vitesseG'])
						vitesse_droite = int(msg_recu_json['vitesseD'])
					elif('vitesseG' in msg_recu_json):
						vitesse_gauche = int(msg_recu_json['vitesseG'])
						vitesse_droite = default
					elif('vitesseD' in msg_recu_json):
						vitesse_gauche = default
						vitesse_droite = int(msg_recu_json['vitesseD'])
					#Si on est en mode 0 ou 2, on ramène les vitesses entre 0 et 255
					else:
						self.serveur.input.put("Aucune vitesse n'a été recue, les instructions n'ont pas été exécutées")
					if(self.MODE%2 == 0):
						if(vitesseG != default):
							vitesseG += 128
						if(vitesseD != default):
							vitesseD += 128
					result_droite = verif_commande_SETSPEED(vitesseD)
					result_gauche = verif_commande_SETSPEED(vitesseG)
					#Si tout est bon, on envoie à la liaison série
					if(result_mode & result_droite & result_gauche):
						self.serie.input.put((msg_recu_json['mode'],msg_recu_json['vitesseG'],msg_recu_json['vitesseD']))
					#sinon, on informe le serveur
					else:
						self.serveur.input.put("Un des paramètres recu n'est pas bon, les instructions n'ont pas été exécutées")
				else:
					self.serveur.input.put("Le mode recu n'est pas bon, aucune instruction n'a été exécuté")
			else:
				self.serveur.input.put("Le mode n'a pas été recu, aucune instruction n'a été exécuté")
		except ValueError:
			self.serveur.input.put("Decoding JSON has failed")


	def verif_commande_SETSPEED(self,parameter):
		if((self.MODE % 2) == 0):
			return (parameter >= 0) & (parameter <= 255)
		else :
			return (parameter >= -128) & (parameter <= 127)

	def verif_commande_SETACCELERATION(self,parameter):
		return (parameter >= 1) & (parameter <= 10)

	def verif_commande_SETMODE(self,parameter):
		return (parameter >= 0) & (parameter <= 3)