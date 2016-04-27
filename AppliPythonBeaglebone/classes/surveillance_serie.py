import threading
import logging
from datetime import datetime

class Surveillance_serie(threading.Thread):
	def __init__(self,controleur,filename="surveillance_serie.log"):
        self.pere   =controleur
		self.serie=Serie(ident)
		self.stoprequest = threading.Event()
		logging.basicConfig(filename=filename,level=logging.DEBUG)
		

	def kill(self):
		del self.serveur
		self.serie=Serie()
		self.pere.mise_a_jour_serie(self.serie)

	def run(self):
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
					logging.critical("Le thread Serie ne répondait plus, il a été tué et réinstancié")
				else:
					statut_serie = "vivant"
				maintenant = datetime.now()
				logging.debug("Le "+maintenant.day+"/"+maintenant.month+"/"+maintenant.year" à "+maintenant.hour+":"+maintenant.minute+":"+maintenant.second+", le thread serie est "+statut_serie+" et les messages suivants sont en attente de traitement : Emission série:"+message_input+"///// Réception série:"+message_output)
			except Queue.Empty:
				continue