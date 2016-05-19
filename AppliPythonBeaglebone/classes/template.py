# coding: utf8
import threading

class Template(threading.Thread):
	def __init__(self,controleur,stopevent):
		threading.Thread.__init__(self)
		#En cas de mise en place d'une surveillance d'une classe, un template de surveillance_partage est disponible
		#contenant la classe à partager entre cette classe et la classe de surveillance
		#self.template_partage=controleur.surveillance.template_partage 
		self.stoprequest = stopevent

	def run(self):
		while not self.stoprequest.isSet():
			try:
				#do something here
				
			except IndexError:
				continue

	def stop(self):
		self.stoprequest.set()