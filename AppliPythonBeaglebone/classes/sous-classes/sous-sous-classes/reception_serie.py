# coding: utf8
import Adafruit_BBIO.UART as UART
import serial
from time import sleep

import threading

import constants

###   Préparation du programme

class Reception_Serie(threading.Thread):
	"""
	Classe regroupant la communication par liaison série avec les moteurs
		Prend en entrée:
			queue_output : Une queue d'items output, les informations que la liaison Série va faire remonter au controleur : les retours des commandes s'il y en a 
			stopevent : Une variable provoquant l'arrêt du thread, passée depuis le thread parent, qui permet l'arrêt en cascade
			sel_uart : variable sélectionnant la liaison série à ouvrir, valant 1 par défaut (UART1)
	"""

	def __init__(self, queue_output, stopevent,sel_uart, occupe):
		#Les liaisons valides sont les liaisons 1,2,4
		if(sel_uart not in [1,2,4]):
				return "Erreur : la liaison série spécifiée n'est pas valide"
		#Initialisation du thread lui-même		
		threading.Thread.__init__(self)
		#Les informations recues sur la liaison série seront empilées ici
		self.output = queue_output
		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = stopevent
		#Variable empechant l'empiêtement des classes Série (pas de lecture quand envoi, et pas d'envoi quand lecture)
		self.occupe = occupe
		### Liaison série
		#On choisit la liaison série spécifiée, sinon la liaison série 1 par défaut
		UART.setup("UART"+str(sel_uart))

		#Ouverture de la liaison série
		#le parametre stopbits DOIT etre égal à 1, le mettre à deux entraine une incompréhension par le controleur des moteurs des ordres à envoyer
		self.ser = serial.Serial(port = "/dev/ttyO"+str(sel_uart), baudrate=38400,bytesize=8, stopbits=1,timeout=0.5)
		#On ferme la liaison série instanciée, afin de ne pas occuper constamment le canal
		self.ser.close()

	def run(self):
		#Tant que le controleur ne demande pas au thread de s'arreter
		sleep(1)
		try:
			while not self.stoprequest.isSet():
				try:
					self.infos_recues = False
					while(not self.infos_recues):
						if(not self.occupe):
							self.occupe = True
							self.ser.open()
							infos = self.ser.read()
							#On regarde si des informations nous parviennent de la liaison série
							#S'il y a quelque chose, on le transmet au controleur
							if(infos != ''):
								self.output.appendleft(infos)
							self.ser.close()
							self.occupe = False
							self.infos_recues = True
						else:
							continue
				except IndexError:
					self.occupe = False
					continue
				except serial.SerialException:
					continue
		finally:
			self.ser.close()
	
	def stop(self):
		self.stoprequest.set()