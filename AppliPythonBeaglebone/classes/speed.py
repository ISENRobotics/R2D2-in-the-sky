# coding: utf8
import threading
import logging
import time
import json

class Speed(threading.Thread):
	def __init__(self,controleur,stopevent):
		threading.Thread.__init__(self)
		#En cas de mise en place d'une surveillance d'une classe, un template de surveillance_partage est disponible
		#contenant la classe à partager entre cette classe et la classe de surveillance
		#self.template_partage=controleur.surveillance.template_partage 
		self.pere = controleur
		self.stoprequest = stopevent
		self.serie = controleur.surveillance_serie.serie
		self.serveur = controleur.surveillance_serveur.serveur
		self.logger = logging.getLogger("R2D2_Test")
		self.logger.setLevel(logging.INFO)
		self.formatter= logging.Formatter('%(asctime)s : %(message)s')
		self.fileHandler = logging.FileHandler("/var/log/R2D2_testspeed", mode='w')
		self.fileHandler.setFormatter(self.formatter)
		self.logger.addHandler(self.fileHandler)


	def run(self):
		self.serie.input.appendleft((0,128,128,2))
		while not self.stoprequest.isSet():
			try:
				info = self.serveur.output.pop()
				self.logger.info("Message received : " +str(info))
				
				self.getData(info)
				#do something here
				
			except IndexError:
				try:
					
					self.i = 10
				except IndexError:
					continue
			finally:
				self.serveur.stop()
				self.serie.stop()

	def getData(self, start):
		inversion = False
		try:
			self.logger.info("Message : " + start)
			self.commande = json.loads(start)
			self.logger.info("Json : "+ str(self.commande))
			self.logger.info("Commande1 : " + self.commande['commande'])
			self.logger.info("Vitesse : " +self.commande['speed'])
			vitesse = int(self.commande['speed'])
			if(self.commande['commande'] == "start"):	
				self.logger.info("Into while")
				self.serie.informations(constants.GET_ENCODER_1)
				self.serie.input.appendleft((0,vitesse,vitesse,2))

				encod = self.serveur.output.pop()
				#encod = "YOUOU"
				self.logger.info("Message received : " +str(len(encod)))

				if encod != '':
					self.logger.info("Message received : " +str(encod))
					encod = json.loads(encod)
					if int(encod['Encoder_Number']) == 1:
						self.serie.informations(constants.GET_ENCODER_1)
						while encod == '':
							encod1 = self.serie.ouput.pop()
						self.pere.traitement.input.appendleft(encod1)
					elif str(encod['Encoder_Number']) == 2:
						self.serie.informations(constants.GET_ENCODER_2)
						while encode == '':
							encod2 = self.serie.output.pop()
						self.pere.traitement.input.append(encod2)
					elif str(encod['commande']) != 'start':
						self.serie.input.appendleft((0,int(encod['speed']),int(encod['speed']),2))
						self.commande = encod
				time.sleep(0.1)
				#data = json.dumps({'Encoder1' : str(encod1), 'Encoder 2' : str(encod2)), 'Time' : str(time.time())})
				#self.pere.traitement.input.appendleft(data)
		except Exception,e:
			self.logger.debug("ERROR : " + str(e)+ ' ')
		finally:
			self.serie.input.appendleft((0,128,128,2))

	def stop(self):
		self.stoprequest.set()
