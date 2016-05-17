# coding: utf8
import threading

class Template(threading.Thread):
	def __init__(self,controleur):
		threading.Thread.__init__(self)
		self.template_partage=controleur.surveillance.template_partage 
		self.stoprequest = threading.Event()

    def run(self):
    	while not self.stoprequest.isSet():
			try:
				#do something here
				
			except IndexError:
				continue