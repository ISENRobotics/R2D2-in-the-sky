# coding: utf8
import threading
import logging
from datetime import datetime
from time import sleep
import Queue
from collections import deque

import sys
sys.path.insert(0, '/root/R2D2/classes/sous-classes')

import serie


class Surveillance_serie(threading.Thread):
	def __init__(self,controleur,filename="surveillance_serie.log"):
		threading.Thread.__init__(self)
		self.pere   =controleur
		self.queue_input_reception = deque()
		self.queue_output_emission = deque()
		self.serie=serie.Serie(self.queue_input_reception,self.queue_output_emission)
		self.stoprequest = threading.Event()
		logger1 = logging.getLogger('R2D2.surveillance_serie')
		formatter = logging.Formatter('%(asctime)s : %(message)s')
		fileHandler = logging.FileHandler(filename, mode='w')
		fileHandler.setFormatter(formatter)
		streamHandler = logging.StreamHandler()
		streamHandler.setFormatter(formatter)

		logger1.setLevel(logging.DEBUG)
		logger1.addHandler(fileHandler)
		logger1.addHandler(streamHandler)
		logger1.debug("Démarrage du thread de Surveillance_serie")
		self.serie.start()

	def kill(self):
		del self.serie
		self.serie=Serie()
		self.pere.mise_a_jour_serie(self.serie)

	def run(self):
		logger1.debug("Surveillance_serie running")
		sleep(0.01)
		logger1.debug("Serie initialized, commencing surveillance")
		#Messages servant à logger l'activité de la liaison série
		message_input = ""
		message_output = ""
		while not self.stoprequest.isSet():
			try:
				#Routine de logging d'activité de la liaison série
				if(message_input != self.serie.input[0]):
					message_input = self.serie.input[0]
				if(message_output != self.serie.output[0]):
					message_output = self.serie.output[0]
				serie_vivante = self.serie.is_alive()
				if(not serie_vivante):
					statut_serie = "mort"
					kill()
					logger1.critical("Le thread Serie ne répondait plus, il a été tué et réinstancié")
				else:
					statut_serie = "vivant"
				maintenant = datetime.now()
				logger1.debug("Le "+maintenant.day+"/"+maintenant.month+"/"+maintenant.year+" à "+maintenant.hour+":"+maintenant.minute+":"+maintenant.second+", le thread serie est "+statut_serie+" et les messages suivants sont en attente de traitement : Emission série:"+str(message_input)+"///// Réception série:"+str(message_output))
			except IndexError:
				continue

	def stop(self):
		self.stoprequest.set()