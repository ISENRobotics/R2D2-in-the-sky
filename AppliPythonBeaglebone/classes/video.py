# coding: utf8
import threading
from collections import deque

import sys

import cv2
import string

class Video(threading.Thread):
	def __init__(self,stopevent,filename="surveillance_serie.log"):
		threading.Thread.__init__(self)
		#self.serveur = controleur.surveillance_serveur.serveur 
		self.stoprequest = stopevent
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def run(self):
		self.buffer = {}
		try:
			while not self.stoprequest.isSet():
				success, image = self.video.read()
				if not success:
					continue
				print(success)
				print(image)
				ret, jpeg = cv2.imencode('.jpg', image,self.buffer)
				print(ret)
				print(jpeg)
				#self.serveur.input.appendleft(jpeg.tobytes()) 

		except KeyboardInterrupt as key:
			self.stoprequest.set()

	def stop(self):
		self.stoprequest.set()

e = threading.Event()
v =Video(e)
v.start()