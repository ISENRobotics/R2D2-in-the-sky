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
		self.serie.input.appendleft((0,128,128,2))
		try:
			while not self.stoprequest.isSet():
				try:
					infos = self.serveur.output.pop()
					#Traitement des infos
					#print("Dans la classe Algorithmique : "+str(infos))
					self.verif_trame_recu(infos)
					
				except IndexError:
					try:
						#Si on n'a pas recu d'informations dans le temps imparti, on regarde si un message à envoyer est arrivé
						infos = self.serie.output.pop()
						#print("Dans la classe Algorithmique : "+str(infos))
						#Traitement des infos
						self.serveur.input.appendleft(infos)
					except IndexError:
						continue
		finally:
			self.serveur.stop()
			self.serie.stop()

	def verif_trame_recu(self,trame):
		#variable décidant quel moteur est à gauche et quel moteur est à droite
		sens_des_moteurs_moteur_1_a_gauche_moteur_2_a_droite = False
		#variable inversant les vitesses moteurs recues (full forward devient full reverse)
		#sert à rétablir le sens du robot (moteurs montées dans le mauvais sens)
		inversion_vitesse_moteur = True
		try:
			msg_recu_json = json.loads(trame)
			result_mode = 0
			result_droite = 0
			result_gauche = 0
			if('temps' in msg_recu_json):
				temps = int(round(time.time() * 1000))
				if(temps - int(msg_recu_json['temps']) < 2000):
					if('mode' in msg_recu_json):
						result_mode = self.verif_commande_SETMODE(int(msg_recu_json['mode']))
						if(result_mode):
							self.MODE = int(msg_recu_json['mode']);
							if(self.MODE == 8):
								#Mode arrêt
								self.serie.input.appendleft((0,128,128,2))
							elif (self.MODE == 2):
								#mode portrait
								default = 0
								if(('vitesse' in msg_recu_json) & ('angle' in msg_recu_json)):
									vitesse = int(msg_recu_json['vitesse'])
									turn = float(msg_recu_json['angle'])
								elif('vitesse' in msg_recu_json):
									vitesse = int(msg_recu_json['vitesse'])
									turn = float(default)
								elif('angle' in msg_recu_json):
									vitesse = default
									turn = float(msg_recu_json['angle'])
								else:
									self.serveur.input.appendleft("La vitesse et l'angle n'ont pas été recues, les instructions n'ont pas été exécutées")
								#if(vitesse != default):
								#	vitesse += 128
								result_vitesse = self.verif_commande_SETSPEED(vitesse)
								turn = self.conversion_TURN_MODE_2(turn)
								if(result_vitesse):
									self.serie.input.appendleft((3,vitesse,int(turn),2))
							else:
								#Mode paysage
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
								if(inversion_vitesse_moteur):
									vitesse_gauche *= -1
									vitesse_droite *= -1
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
										self.serie.input.appendleft((self.MODE,vitesse_gauche,vitesse_droite,2))
									else:
										self.serie.input.appendleft((self.MODE,vitesse_droite,vitesse_gauche,2))
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

	def conversion_TURN_MODE_2(self,turn_value):
		if(turn_value <=90.0):
			return int((127-(turn_value/90.0)*127.0)/2.0)
		elif((turn_value>90.0) & (turn_value<=180.0)):
			return int((((turn_value/90.0)-1)*(-127))/2.0)
		elif((turn_value>180.0) & (turn_value<=270.0)):
			return int((127.0 - ((turn_value/90.0)-2)*127.0)/2.0)
		else:
			return int((((turn_value/90.0)-3)*(-127))/2.0)

	def stop(self):
		self.stoprequest.set()