# coding: utf8
import threading
import json
import time
import datetime
import os
import sys
sys.path.insert(0, '/root/R2D2/classes/sous-classes')

import serveur
import serie

class Traitement(threading.Thread):
	"""
	Classe englobant le traitement des informations du smartphone et le dispatchage des informations aux bonnes classes
		Contient:
			Une classe Serveur, partagée avec la classe Surveillance_serveur
			Une classe Série, partagée avec la classe Surveillance_série

		Prend en entrée:
			controleur : le controleur général du programme, contenant toutes les classes principales
			stopevent : Une variable provoquant l'arrêt du thread, passée depuis le thread parent, qui permet l'arrêt en cascade
	"""
	def __init__(self,controleur,stopevent):
		#Initialisation du thread lui-même		
		threading.Thread.__init__(self)
		#On récupère les serveurs et série instanciés par les classes de surveillance
		self.serveur = controleur.surveillance_serveur.serveur 
		self.serie   = controleur.surveillance_serie.serie;
		self.stoprequest = stopevent
		self.heure_mise_a_jour = False

	def run(self):
		#On envoie un message d'arrêt aux moteurs pour être sur
		self.serie.input.appendleft((0,128,128,2))
		self.previous_angle = 0
		try:
			while not self.stoprequest.isSet():
				try:
					#Si le serveur a recu des informations du smartphone, on déclenche leurs vérifications
					infos = self.serveur.output.pop()
					self.verif_trame_recu(infos)
					
				except IndexError:
					try:
						#Si on n'a pas recu d'informations dans le temps imparti, on regarde si un message à envoyer est arrivé
						#infos = self.serie.output.pop()
						#self.serveur.input.appendleft(infos)
						#Variable dummy, servant juste à faire quelque chose durant l'exception
						self.i = 10
					except IndexError:
						continue
		finally:
			self.serveur.stop()
			self.serie.stop()

	def verif_trame_recu(self,trame):
		#variable décidant quel moteur est à gauche et quel moteur est à droite
		#Le montage actuel nous oblige à la déclarer False
		#Mettre True si une inversion des moteurs au remontage se produit
		sens_des_moteurs_moteur_1_a_gauche_moteur_2_a_droite = False
		#variable inversant les vitesses moteurs recues (full forward devient full reverse)
		#sert à rétablir le sens du robot (moteurs montées dans le mauvais sens)
		inversion_vitesse_moteur = True

		#Bridage moteur, afin de diminuer la vitesse maximale
		bridage = True
		#Par combien la vitesse sera divisée
		taux_de_bridage = 1.5
		try:
			#On essaie de décoder le JSON recu
			msg_recu_json = json.loads(trame)
			#Variables testant si l'envoi des informations à la liaison série peut se faire, mises à False par défaut
			result_mode = 0
			result_droite = 0
			result_gauche = 0
			#Si on a bien recu le timestamp de l'envoi du message
			if('temps' in msg_recu_json):
				#La beaglebone ne dispose pas de pile interne, on est donc obligé de mettre a jour l'heure système
				#en fonction de l'heure du téléphone. On récupère donc le premier timestamp et on l'utilise pour
				#actualiser l'heure système
				if(not self.heure_mise_a_jour):
					date = datetime.datetime.fromtimestamp(int(msg_recu_json['temps'])/1000).strftime('%m/%d/%Y')
					heure = datetime.datetime.fromtimestamp(int(msg_recu_json['temps'])/1000).strftime('%H:%M:%S')
					os.system("date -s "+str(date))
					os.system("date -s "+str(heure))
					self.heure_mise_a_jour = True
				#On calcule le temps actuel
				temps = int(round(time.time() * 1000))
				#Si les informations ont mises moins de 2 secondes à arriver, on continue
				if(temps - int(msg_recu_json['temps']) < 2000):
					if('mode' in msg_recu_json):
						#On vérifie si le mode recu est conforme aux valeurs autorisées
						result_mode = self.verif_commande_SETMODE(int(msg_recu_json['mode']))
						if(result_mode):
							#On met à jour le mode de fonctionnement mémorisé dans python
							#Attention, le changement de mode du CONTROLEUR des moteurs a lieu plus bas
							self.MODE = int(msg_recu_json['mode']);
							#Si on est en mode 8, le smartphone est au repos, on envoie des trames d'arrêt aux moteurs pour immobiliser le robot
							if(self.MODE == 8):
								self.serie.input.appendleft((0,128,128,2))
							elif (self.MODE == 2):
								#mode portrait, la valeur médiane des vitesses vaut 0
								default = 0
								#On assigne les informations recues aux variables vitesse et turn
								#Si des bouts de message manquent, comme la vitesse, on leur assigne la valeur médiane
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
									#Si on n'a pas recu assez d'informations, on le fait remonter au smartphone
									self.serveur.input.appendleft("La vitesse et l'angle n'ont pas été recues, les instructions n'ont pas été exécutées")
								#if(vitesse != default):
								#	vitesse += 128
								#On vérifie que la vitesse et l'angle ainsi récupérés sont conformes aux spécifications
								rotation_speed = (turn - self.previous_angle)/360 * 127
								self.previous_angle = turn
								speed_wheel1 = vitesse - rotation_speed/2
								speed_wheel2 = vitesse + rotation_speed/2
								if (speed_wheel1 > 127):
									speed_wheel2 = speed_wheel2 - (speed_wheel1 - 127)
									speed_wheel1 = 127
								elif (speed_wheel1 < -128):
									speed_wheel2 = speed_wheel2 + (speed_wheel1 + 128)
									speed_wheel1 = -128
								elif (speed_wheel2 > 127):
									speed_wheel1 = speed_wheel1 - (speed_wheel2 - 127)
									speed_wheel2 = 127
								elif (speed_wheel2 < -128):
									speed_wheel1 = speed_wheel1 + (speed_wheel2 + 128)
									speed_wheel2 = -128
	
								vitesse_gauche = self.verif_commande_SETSPEED(speed_wheel1)
								vitesse_droite = self.verif_commande_SETSPEED(speed_wheel2)
								#result_vitesse = self.verif_commande_SETSPEED(vitesse)
								#turn = self.conversion_TURN_MODE_2(turn)
								#Si tout va bien, on envoie sur la liaison série
								#if(result_vitesse):
								#	self.serie.input.appendleft((3,vitesse,int(turn),2))
								if(vitesse_gauche && vitesse_droite):
									if(sens_des_moteurs_moteur_1_a_gauche_moteur_2_a_droite):
										self.serie.input.appendleft((1,vitesse_gauche,vitesse_droite,2))
									else:
										self.serie.input.appendleft((1,vitesse_droite,vitesse_gauche,2))

							else:
								#Mode paysage
								#on commence par assigner une valeur par défaut médiane
								default = 128
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
								if(bridage):
									vitesse_gauche = (int)((float)(vitesse_gauche)/taux_de_bridage)
									vitesse_droite = (int)((float)(vitesse_droite)/taux_de_bridage)
								#Si les valeurs transmises sont inversées par rapport à la réalité, on les réajustent
								if(inversion_vitesse_moteur):
									vitesse_gauche *= -1
									vitesse_droite *= -1
								#on ramène les vitesses entre 0 et 255
								if(vitesse_gauche != default):
									vitesse_gauche += 128
								if(vitesse_droite != default):
									vitesse_droite += 128
								#On vérifie que les vitesses sont conformes
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


	#Fonction chargée de vérifier que la vitesse est comprise dans une gamme de valeurs permises selon le mode de fonctionnement actuel
	def verif_commande_SETSPEED(self,parameter):
		if((self.MODE % 2) == 0):
			return (parameter >= 0) & (parameter <= 255)
		else :
			return (parameter >= -128) & (parameter <= 127)

	#Fonction chargée de vérifier que l'accélération est bien comprise entre 1 et 10
	def verif_commande_SETACCELERATION(self,parameter):
		return (parameter >= 1) & (parameter <= 10)

	#Fonction chargée de vérifier que les modes transmis sont bien compris entre 0 et 3, ou égal à 8 si le smartphone est au repos
	def verif_commande_SETMODE(self,parameter):
		return ((parameter >= 0) & (parameter <= 3)) | (parameter == 8)

	#Fonction de conversion des angles recus du smartphone en mode portrait afin de permettre l'altération de la vitesse des moteurs
	#Ainsi, entre 0 et 90 degrés d'angles, turn doit varier de 127 à 0
	#			
	#		0->90 : 127->0 ==== y = 127-(x/90)*127
	#
	#Entre 90 et 180 degrés d'angles, turn doit varier de 0 à -127
	#			
	#		90->180 : 0->-127 ==== y = ((x/90)-1)*(-127)
	#
	#Entre 180 et 270 degrés, turn doit varier de 127 à 0
	#			
	#		180->270 : 127->0 ==== y = 127-((x/90)-2)*127
	#
	#Entre 270 et 360 degrés, turn doit varier de 0 à -127
	#			
	#		270->360 : 0->-127 ==== y = ((x/90)-3)*(-127)
	#
	#On a ici divisé par deux tous les résultats finaux afin d'obtenir un adoucissement des virages et variations
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
