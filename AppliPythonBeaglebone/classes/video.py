# coding: utf8
import threading
from collections import deque
import numpy as np
import sys
import time
import os

import cv2
import string

class Video(threading.Thread):
	def __init__(self,controleur,stopevent):
		threading.Thread.__init__(self)
		self.serveur = controleur.surveillance_serveur.serveur 
		self.stoprequest = stopevent
		#self.video = cv2.VideoCapture(0)

		#self.video = cv2.VideoCapture(0)
		#self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
		#self.out = cv2.VideoWriter('output.avi',self.fourcc, 20.0, (640,480), True)


	def __del__(self):
		self.video.release()

	def run(self):
		print("Initialisation effectuée, on rentre dans la boucle")
		#self.buffer = {}
		self.increment = 0
		#self.out.write(125 * np.ones((640,480,3), np.uint8))
		self.error = 1
		try:
			#while not self.stoprequest.isSet():
			'''while self.increment < 4:
				print("on tente de récupérer l'image")
				success, image = self.video.read()
				if not success:
					continue


				encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),75]
				result, imgencode = cv2.imencode('.jpg', image, encode_param)
				data = np.array(imgencode)
				stringData = data.tostring()
				#time.sleep(0.05)
				print("on a récupéré l'image, on l'écrit")
				#image = cv2.flip(image,0)
				#self.out.write(image)
				ret, self.buffer = cv2.imencode('.jpg', image)
				#print(ret)
				cv2.imwrite('test'+str(self.increment)+'.jpg',image)
				#img = Image.open('test.jpeg')
				#self.serveur.input.appendleft(img+'\n') 
				#self.increment += 1
				#print(self.increment)
				#cv2.waitKey(40)
			'''
			while(self.error != 0):
				os.system('avconv -f video4linux2 -s 640x360 -r 10 -b 350k -i /dev/video0 tcp://172.17.0.2:12801')
				time.sleep(1)
		finally:
			#self.video.release()
			print('stop')

	def stop(self):
		self.stoprequest.set()
