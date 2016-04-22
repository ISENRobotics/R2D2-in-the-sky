#/usr/bin/env python
# -*-coding:Utf-8 -*
import socket
import json
import threading

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

		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = threading.Event()
		### Socket serveur
		self.socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#Adresse et Port à définir suivant les possibilités de l'application Android, ici port 12800
		self.socket_serveur.bind(('', 12800))

		#Une connexion maximale possible au socket, comme ca pas de problème avec plusieurs applications, un seul téléphone peut communiquer avec l'appli
		self.socket_serveur.listen(1)

		#On accepte la connexion
		#Attention, la méthode accept bloque le programme tant qu'aucun client ne s'est présenté
		connexion_avec_client, infos_connexion = self.socket_serveur.accept()
		print(infos_connexion)
		### Socket client
		#On crée le socket de connexion
		#self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#On connecte le socket sur l'adresse et le port désiré
		#Idée : attribuer une IP fixe grâce au routeur au téléphone Android, voir réseau en 255.255.255.252
		#self.socket_client.connect(('192.168.0.3', 12800))

	def run(self):
		#Tant que le controleur ne demande pas au thread de s'arreter
		while not self.stoprequest.isSet():
			try:
				#On attend les informations du smartphone
				msg_recu = connexion_avec_client.recv(49)
				msg_recu_json = json.loads(msg_recu)
				if('mode' in msg_recu_json & 'vitesseG' in msg_recu_json & 'vitesseD' in msg_recu_json & 'accel' in msg_recu_json ):
					#On envoie au controleur les informations parsées
					self.output.put((msg_recu_json['mode'],msg_recu_json['vitesseG'],msg_recu_json['vitesseD'],msg_recu_json['accel']))
					#On attend le retour des ordres que la liaison série envoie au controleur après éxécution des ordres
					infos = self.input.get(True, 0.05)
					self.socket_client.send(infos)
				else:
					self.socket_client.send("Les commandes demandées ont été anormalement changées, elles n'ont pas été exécutées...")
			except Queue.Empty:
				continue