# coding: utf8
import threading
from collections import deque
import numpy as np
import sys
import time

import cv2
import string

class Video(threading.Thread):
	def __init__(self,stopevent):
		threading.Thread.__init__(self)
		#self.serveur = controleur.surveillance_serveur.serveur 
		self.stoprequest = stopevent
		self.video = cv2.VideoCapture(0)
		#self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
		#self.out = cv2.VideoWriter('output.avi',self.fourcc, 20.0, (640,480), True)


	def __del__(self):
		self.video.release()

	def run(self):
		print("Initialisation effectuée, on rentre dans la boucle")
		self.buffer = {}
		self.increment = 0
		#self.out.write(125 * np.ones((640,480,3), np.uint8))
		try:
			#while not self.stoprequest.isSet():
			while self.increment < 10:
				print("on tente de récupérer l'image")
				success, image = self.video.read()
				if not success:
					continue
				time.sleep(0.05)
				print("on a récupéré l'image, on l'écrit")
				#image = cv2.flip(image,0)
				#self.out.write(image)
				#ret, self.buffer = cv2.imencode('.jpg', image)
				#print(ret)
				cv2.imwrite('test'+str(self.increment)+'.jpg',image)
				#self.serveur.input.appendleft(jpeg.tobytes()) 
				self.increment += 1
				print(self.increment)
				cv2.waitKey(40)
		finally:
			self.video.release()

	def stop(self):
		self.stoprequest.set()

e = threading.Event()
v = Video(e)
v.start()