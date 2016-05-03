# coding: utf8
import threading
import logging
import json
from datetime import datetime
import time

import sys
sys.path.insert(0, '/root/R2D2/classes/sous-classes')

import serveur
import serie

class Algorithmique(threading.Thread):
	def __init__(self,controleur,stopevent):
		threading.Thread.__init__(self)
		self.serveur = controleur.surveillance_serveur.serveur 
		self.serie   = controleur.surveillance_serie.serie;
		self.stoprequest = stopevent
		
	def run(self):
		try:
			while not self.stoprequest.isSet():
				print("ON RENTRE DANS LA CLASSE ALGO BITCH !")
				try:
					infos = self.serveur.output.pop()
					#Traitement des infos
					print("Dans la classe Algorithmique : "+str(infos))
					self.verif_trame_recu(infos)
					
				except IndexError:
					try:
						#Si on n'a pas recu d'informations dans le temps imparti, on regarde si un message à envoyer est arrivé
						infos = self.serie.output.pop()
						print("Dans la classe Algorithmique : "+str(infos))
						#Traitement des infos
						self.serveur.input.appendleft(infos)
					except IndexError:
						continue
		except KeyboardInterrupt as key:
			self.stoprequest.set()

	def verif_trame_recu(self,trame):
		sens_des_moteurs_moteur_1_a_gauche_moteur_2_a_droite = True
		try:
			msg_recu_json = json.loads(trame)
			result_mode = 0
			result_droite = 0
			result_gauche = 0
			if('temps' in msg_recu_json):
				temps = int(round(time.time() * 1000))
				print("ALGORITHMIQUE : VOILA CE QUE VAUT LA SOUSTRACTION DU TEMPS ACTUEL AU TEMPS ENVOYEEEEEEEEEEEEEEEEEEEEEEEE : "+str(temps - int(msg_recu_json['temps'])))
				if(temps - int(msg_recu_json['temps']) < 2000):
					if('mode' in msg_recu_json):
						result_mode = self.verif_commande_SETMODE(int(msg_recu_json['mode']))
						if(result_mode):
							self.MODE = int(msg_recu_json['mode']);
							if(self.MODE == 8):
								self.serie.input.appendleft((0,128,128))
							else:
								#on commence par assigner des vitesses telles que les moteurs ne bougent pas
								if(self.MODE %2 == 0):
									default = 128
								else:
									default = 0
								if(('vitesseD' in msg_recu_json) & ('vitesseG' in msg_recu_json)):
									vitesse_gauche = int(msg_recu_json['vitesseG'])
									vitesse_droite = int(msg_recu_json['vitesseD'])
								elif('vitesseG' in msg_recu_json):
									vitesse_gauche = int(msg_recu_json['vitesseG'])
									vitesse_droite = default
								elif('vitesseD' in msg_recu_json):
									vitesse_gauche = default
									vitesse_droite = int(msg_recu_json['vitesseD'])
								else:
									self.serveur.input.appendleft("Aucune vitesse n'a été recue, les instructions n'ont pas été exécutées")
								#Si on est en mode 0 ou 2, on ramène les vitesses entre 0 et 255
								if(self.MODE%2 == 0):
									if(vitesse_gauche != default):
										vitesse_gauche += 128
									if(vitesse_droite != default):
										vitesse_droite += 128
								result_droite = self.verif_commande_SETSPEED(vitesse_droite)
								result_gauche = self.verif_commande_SETSPEED(vitesse_gauche)
								#Si tout est bon, on envoie à la liaison série
								if(result_mode & result_droite & result_gauche):
									if(sens_des_moteurs_moteur_1_a_gauche_moteur_2_a_droite):
										self.serie.input.appendleft((self.MODE,vitesse_gauche,vitesse_droite))
									else:
										self.serie.input.appendleft((self.MODE,vitesse_droite,vitesse_gauche))
								#sinon, on informe le serveur
						else:
							self.serveur.input.appendleft("{'probleme':'Le mode recu n'est pas bon, aucune instruction n'a été exécuté'}")
					else:
						self.serveur.input.appendleft("{'probleme':'Le mode n'a pas été recu, aucune instruction n'a été exécuté'}")
				else:
					self.serveur.input.appendleft("{'probleme':'Les informations ont pris trop de temps à arriver, elles n'ont pas été exécutées'}")
			else:
				self.serveur.input.appendleft("{'probleme':'temps non reçu, impossible de vérifier les informations'}")
		except ValueError:
			self.serveur.input.appendleft("{'probleme':'Decoding JSON has failed'}")


	def verif_commande_SETSPEED(self,parameter):
		if((self.MODE % 2) == 0):
			return (parameter >= 0) & (parameter <= 255)
		else :
			return (parameter >= -128) & (parameter <= 127)

	def verif_commande_SETACCELERATION(self,parameter):
		return (parameter >= 1) & (parameter <= 10)

	def verif_commande_SETMODE(self,parameter):
		return ((parameter >= 0) & (parameter <= 3)) | (parameter == 8)

	def stop(self):
		self.stoprequest.set()