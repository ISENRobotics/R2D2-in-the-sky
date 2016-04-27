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
import serveur
import serie

### Programme principal
if __name__ == '__main__':
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
	try:
		surveillance_serveur = Surveillance_serveur(self)
		surveillance_serie   = Surveillance_serie(self)
		algorithmique        = Algorithmique(self)
		#on déclare les queues nous servant à communiquer avec les threads
		queue_input_serie = Queue.Queue()
		queue_output_serie = Queue.Queue()
		queue_input_serveur = Queue.Queue()
		queue_output_serveur = Queue.Queue()
		
		thread_serie = serie.Serie(queue_input_serie,queue_output_serie)
		thread_serveur = serveur.Serveur(queue_input_serveur,queue_output_serveur)

		thread_serie.start()
		thread_serveur.start()

		continuer = True
		while continuer:
			
			infos = queue_output_serveur.get(True)
			queue_input_serie.put((infos))
			infos = queue_output_serie.get(True)
			queue_input_serveur.put((infos))
		thread_serie.join()
		thread_serveur.join()
	#On récupère toutes exceptions génantes (Ctrl-C de l'utilisateur, arrêt brutal du système)
	except KeyboardInterrupt as key:
		print("User-generated interrupt, exiting....")
		#curses.nocbreak()
		#stdscr.keypad(0)
		#curses.echo()
		#curses.endwin()
		try:
			os.remove("daemon_python")
			thread_serie.join(timeout=0)
			thread_serveur.join(timeout=0)
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
			thread_serie.join(timeout=0)
			thread_serveur.join(timeout=0)
			#os.unlink("daemon_python") est équivalent selon la documentation python, version liens Unix
		except OSError as e:  ## si l'opération échoue, on affiche l'erreur rencontrée (voir au niveau des permissions)
			print ("Error: %s - %s." % (e.filename,e.strerror))
	#Quand on a fini toute l'application (si celle-ci a une fin), on efface le fichier disant que l'application est lancée (et on restaure le terminal initial)
	finally:
		#curses.nocbreak()
		#stdscr.keypad(0)
		#curses.echo()
		#curses.endwin()
		try:
			os.remove("daemon_python")
			thread_serie.join(timeout=0)
			thread_serveur.join(timeout=0)
			#os.unlink("daemon_python") est équivalent selon la documentation python, version liens Unix
		except OSError as e:  ## si l'opération échoue, on affiche l'erreur rencontrée (voir au niveau des permissions)
			print ("Error: %s - %s." % (e.filename,e.strerror))


	
	def mise_a_jour_serveur(self,serveur):
        self.algorithmique.serveur=serveur
    def mise_a_jour_serie(self,serie):
        self.algorithmique.serie=serie