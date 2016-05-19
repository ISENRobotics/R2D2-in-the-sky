# coding: utf8
import threading
from collections import deque

class Template_surveillance(threading.Thread):
	def __init__(self,controleur,filename="surveillance_template_partage.log"):
		threading.Thread.__init__(self)
		self.pere   =controleur
		self.input_template_partage = deque()
		self.output_template_partage = deque()
		self.template_partage=template_partage(self.input_template_partage,self.output_template_partage)
		self.stoprequest = threading.Event()
		logger1 = logging.getLogger('template_partage.template_partage')
		formatter = logging.Formatter('%(asctime)s : %(message)s')
		fileHandler = logging.FileHandler(filename, mode='w')
		fileHandler.setFormatter(formatter)
		streamHandler = logging.StreamHandler()
		streamHandler.setFormatter(formatter)

		logger1.setLevel(logging.DEBUG)
		logger1.addHandler(fileHandler)
		logger1.addHandler(streamHandler)
		logger1.debug("Démarrage du thread de Surveillance_serie")
		self.template_partage.start()
		logger1.debug("Thread série démarré")


	def run(self):
		message_input = ""
		message_output = ""
		while not self.stoprequest.isSet():
			try:
				#Routine de logging d'activité de la liaison série
				if(message_input != self.template_partage.input[0]):
					message_input = self.template_partage.input[0]
				if(message_output != self.template_partage.output[0]):
					message_output = self.template_partage.output[0]
				template_partage_vivant = self.template_partage.is_alive()
				if(not serie_vivante):
					statut_template_partage = "mort"
					self.kill()
					logger1.critical("Le thread template_partage ne répondait plus, il a été tué et réinstancié")
				else:
					statut_template_partage = "vivant"
				maintenant = datetime.now()
				logger1.debug("Le "+maintenant.day+"/"+maintenant.month+"/"+maintenant.year+" à "+maintenant.hour+":"+maintenant.minute+":"+maintenant.second+", le thread template_partage est "+statut_template_partage+" et les messages suivants sont en attente de traitement : Emission série:"+str(message_input)+"///// Réception série:"+str(message_output))
			except IndexError:
				continue


	def kill(self):
		#on efface la classe défectueuse
		del self.template_partage
		#On en crée une nouvelle 
		self.template_partage=template_partage(self.input_template_partage,self.output_template_partage)
		#On prévient le controleur de mettre à jour la classe de traitement principal
		self.pere.mise_a_jour_template_partage(self.template_partage)

	def stop(self):
		self.stoprequest.set()