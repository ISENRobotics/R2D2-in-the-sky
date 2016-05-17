# coding: utf8
import threading
from collections import deque


class Template_partage(threading.Thread):
	def __init__(self, queue_input, queue_output):
		threading.Thread.__init__(self)
		self.input = queue_input
		self.output = queue_output
		#variable écoutant l'arrêt du thread par le controleur
		self.stoprequest = threading.Event()
		

	def run(self):
		sleep(1)
		#Tant que le controleur ne demande pas au thread de s'arreter
		while not self.stoprequest.isSet():
			try:
				#do something here
			except IndexError:
				continue

	def stop(self):
		self.stoprequest.set()