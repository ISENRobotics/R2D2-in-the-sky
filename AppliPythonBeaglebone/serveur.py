#/usr/bin/env python
# -*-coding:Utf-8 -*
import socket

class Serveur(object):
	"""
	Classe englobant le socket serveur permettant la transmission d'infos du robot au smartphone, et inversement
		Contient:
			Socket serveur réceptionnant les informations du smartphone
			Socket client transmettant les informations vers le smartphone
	"""
	def __init__(self):
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
		msg_recu = connexion_avec_client.recv(1024);
		print(msg_recu)
		connexion_avec_client.close();

	def connection(self):
		### Socket client
		#On crée le socket de connexion
		self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#On connecte le socket sur l'adresse et le port désiré
		#Idée : attribuer une IP fixe grâce au routeur au téléphone Android, voir réseau en 255.255.255.252
		self.socket_client.connect(('192.168.0.3', 12800))

	#TODO
	def transmission(self,destination,infos):
		#Soit on envoie au robot, soit on envoie au smartphone
		if destination == "robot":
			return self.socket_serveur.recv(1024)
		else:
			self.socket_client.send(infos)
