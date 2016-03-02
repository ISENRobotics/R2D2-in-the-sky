#/usr/bin/env python
import Adafruit_BBIO.UART as UART
import serial
import socket
import curses

import os
import sys

###   Préparation du programme

class Robot(object):
	"""
	Classe regroupant l'application générale du robot
		Contient:
			Une connexion série UART
			L'algorythmique de surveillance et la transmission des commandes aux moteurs
	"""
	def __init__(self):
		### Liaison série
		#On choisir la liaison série 4
		UART.setup("UART4")

		#Ouverture de la liaison série
		self.ser = serial.Serial(port = "/dev/ttyO4", baudrate=9600)
		self.ser.close()

	#Fonction chargée d'effectuer l'envoi sur la liaison série des commandes moteurs
	def ordre_moteurs(self,commande):
		self.ser.open()
		if self.ser.isOpen():
			self.ser.write(commande)
			#Si la commande est de connaitre la vitesse des moteurs 1 ou 2, on retourne cette valeur
			if (commande == '0x21' || commande == '0x22'):
					return self.ser.read()
		self.ser.close()

class Socket(object):
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
		#connexion_avec_client, infos_connexion = socket_serveur.accept()

		### Socket client
		#On crée le socket de connexion
		self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#On connecte le socket sur l'adresse et le port désiré
		#Idée : attribuer une IP fixe grâce au routeur au téléphone Android, voir réseau en 255.255.255.252
		self.socket_client.connect(('192.168.1.3', 12800))

	#TODO
	def transmission(self,destination,infos):
		#Soit on envoie au robot, soit on envoie au smartphone
		if destination == "robot":
			return self.socket_serveur.recv(1024)
		else:
			self.socket_client.send(infos)

### Programme principal
if __name__ == '__main__':
	#On prépare un fichier temporaire tant que le script est lancé
	pid = str(os.getpid())
	pidfile = "/tmp/mydaemon.pid"

	if os.path.isfile(pidfile):
    	print "%s already exists, exiting" % pidfile
	    sys.exit()
	file(pidfile, 'w').write(pid)
	#On effectue le vrai travail ici
	try:
	    robot = Robot()
		socket = Socket()
		#on initialise la fenetre graphique mode terminal
		stdscr = curses.initscr()
		#On n'affiche pas les entrées saisies à l'écran
		curses.noecho()
		curses.cbreak()
		#On active le mode keypad, permettant la transcription automatique des touches spéciales telles que les flèches en "propriétés curses"
		stdscr.keypad(1)
		#On fait en sorte que getch() ne soit pas bloquant
		stdscr.nodelay(True)
		continue = True
		while continue:
			#On récupère l'entrée utilisateur
			c = stdscr.getch()
			if c == curses.KEY_LEFT:
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
			elif c == curses.KEY_RIGHT:
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
			elif c == curses.KEY_UP:
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
			elif c == curses.KEY_DOWN:
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
			elif c == curses.KEY_ESC
				continue = False
			pass
	#Quand on a fini toute l'application (si celle-ci a une fin), on efface le fichier disant que l'application est lancée (et on restaure le terminal initial)
	finally:
		curses.nocbreak()
		stdscr.keypad(0)
		curses.echo()
		curses.endwin()
	    os.unlink(pidfile)
