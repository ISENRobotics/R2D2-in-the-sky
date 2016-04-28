#/usr/bin/env python
# -*-coding:Utf-8 -*
import Adafruit_BBIO.UART as UART
import serial
import socket
import curses

import os
import sys
sys.path.append("classes/")
import Queue

import thread

"""
	On importe les classes personnalisées python
"""
import surveillance_serveur
import surveillance_serie
import algorithmique
#import template
#import template_surveillance


class Controleur(object):
### Programme principal

	def __init__(self):
		#On prépare un fichier temporaire tant que le script est lancé
		pid = str(os.getpid())
		pidfile = "/tmp/controleur.pid"

		try:
			#On teste si le fichier existe déja
			if os.path.isfile(pidfile):
				os.link(pidfile,"daemon_python")
			else:
				file(pidfile, 'w').write(pid)
				os.link(pidfile,"daemon_python")
		except IOError as e:
			message = "I/O error("+str(e.errno)+"): "+str(e.strerror)
			print(message)
	   #On effectue le vrai travail ici
		self.surveillance_serveur = surveillance_serveur.Surveillance_serveur(self)
		self.surveillance_serie   = surveillance_serie.Surveillance_serie(self)
		self.algorithmique        = algorithmique.Algorithmique(self)
		####################################
		#	Partie Template
		####################################
		#self.template			  = template.Template(self)
		#self.template_surveillance	= template_surveillance.Template_surveillance(self)
		self.continuer = True


	def fonctionnement(self):
		try:
			self.surveillance_serveur.start()
			self.surveillance_serie.start()
			self.algorithmique.start()
			
			####################################
			#	Partie Template
			####################################
			#La partie surveillance doit être lancée avant la partie traitement
			#self.template_surveillance.start()
			#self.template.start()	

				


			self.surveillance_serveur.join()
			self.surveillance_serie.join()
			self.algorithmique.join()

			#self.template_surveillance.join()
			#self.template.join()	

				
		#On récupère toutes exceptions génantes (Ctrl-C de l'utilisateur, arrêt brutal du système)
		except KeyboardInterrupt as key:
			print("User-generated interrupt, exiting....")
			#curses.nocbreak()
			#stdscr.keypad(0)
			#curses.echo()
			#curses.endwin()
			try:
				os.remove("daemon_python")
				self.surveillance_serveur.stop()
				self.surveillance_serveur.join()
				self.surveillance_serie.stop()
				self.surveillance_serie.join()
				self.algorithmique.stop()
				self.algorithmique.join()


				####################################
				#	Partie Template
				####################################
				#self.template_surveillance.stop()
				#self.template_surveillance.join()
				#self.template.stop()	
				#self.template.join()	

				
				#os.unlink("daemon_python") est équivalent selon la documentation python, version liens Unix
			except OSError as e:  ## si l'opération échoue, on affiche l'erreur rencontrée (voir au niveau des permissions)
				print ("Error: %s - %s." % (e.filename,e.strerror))

		except SystemExit as exit_sys:
			print("An exception forcing the interpreter to stop has been detected, shutting down....")
			#curses.nocbreak()
			#stdscr.keypad(0)
			#curses.echo()
			#curses.endwin()
			try:
				os.remove("daemon_python")
				self.surveillance_serveur.stop()
				self.surveillance_serveur.join()
				self.surveillance_serie.stop()
				self.surveillance_serie.join()
				self.algorithmique.stop()
				self.algorithmique.join()

				####################################
				#	Partie Template
				####################################
				#self.template_surveillance.stop()
				#self.template_surveillance.join()
				#self.template.stop()	
				#self.template.join()	


				#os.unlink("daemon_python") est équivalent selon la documentation python, version liens Unix
			except OSError as e:  ## si l'opération échoue, on affiche l'erreur rencontrée (voir au niveau des permissions)
				print ("Error: %s - %s." % (e.filename,e.strerror))
		#Quand on a fini toute l'application (si celle-ci a une fin), on efface le fichier disant que l'application est lancée (et on restaure le terminal initial)
		finally:
			#curses.nocbreak()
			#stdscr.keypad(0)
			#curses.echo()
			#curses.endwin()
			while self.continuer:
				continue
			try:
				os.remove("daemon_python")
				self.surveillance_serveur.stop()
				self.surveillance_serveur.join()
				self.surveillance_serie.stop()
				self.surveillance_serie.join()
				self.algorithmique.stop()
				self.algorithmique.join()
				####################################
				#	Partie Template
				####################################
				#self.template_surveillance.stop()
				#self.template_surveillance.join()
				#self.template.stop()	
				#self.template.join()	

				#os.unlink("daemon_python") est équivalent selon la documentation python, version liens Unix
			except OSError as e:  ## si l'opération échoue, on affiche l'erreur rencontrée (voir au niveau des permissions)
				print ("Error: %s - %s." % (e.filename,e.strerror))


	
	def mise_a_jour_serveur(self,serveur):
		self.algorithmique.serveur=serveur
	def mise_a_jour_serie(self,serie):
		self.algorithmique.serie=serie

	#def mise_a_jour(self,template_partage):
	#	self.template.template_partage=template_partage


c=Controleur()
c.fonctionnement()