# coding: utf8
import threading
import time
import os

class Video(threading.Thread):
	"""
	Classe englobant le streaming vidéo
		Un essai d'intégration d'OpenCV a été effectué, mais n'a pas été concluant, tant en termes de complexité qu'en termes de performances
		La version actuelle se base donc sur une intégration système en dur du logiciel avconv sur Linux, afin d'effectuer le streaming vers l'IP fixe du smartphone
		Prend en entrée:
			stopevent : Une variable provoquant l'arrêt du thread, passée depuis le thread parent, qui permet l'arrêt en cascade
	"""
	def __init__(self,stopevent):
		threading.Thread.__init__(self)
		self.stoprequest = stopevent

	def run(self):
		print("Initialisation effectuée, on rentre dans la boucle")
		self.error = 1
		try:
			while(self.error != 0):
				os.system('avconv -f video4linux2 -s 640x360 -r 10 -b 350k -i /dev/video0 -f mp4 tcp://172.17.0.2:12801')
				time.sleep(1)
		finally:
			print('stop')

	def stop(self):
		self.stoprequest.set()
