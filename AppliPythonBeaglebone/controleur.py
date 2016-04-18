#/usr/bin/env python
# -*-coding:Utf-8 -*
import Adafruit_BBIO.UART as UART
import serial
import socket
import curses

import os
import sys

import thread

"""
	On importe les classes personnalisées python
"""
import Serveur
import Robot

### Programme principal
if __name__ == '__main__':
	#On prépare un fichier temporaire tant que le script est lancé
	pid = str(os.getpid())
	pidfile = "/tmp/controleur.pid"

	try:
		#On teste si le fichier existe déja
		if os.path.isfile(pidfile):
			os.link(pidfile,"daemon_python")
		else
			file(pidfile, 'w').write(pid)
			os.link(pidfile,"daemon_python")
	except IOError as e:
    	print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
	    print "Unexpected error:", sys.exc_info()[0]
	    raise
	    sys.exit()
	#On effectue le vrai travail ici
	try:
	    robot = Robot()
		serveur = Serveur()
		#on initialise la fenetre graphique mode terminal
		stdscr = curses.initscr()
		#On n'affiche pas les entrées saisies à l'écran
		curses.noecho()
		curses.cbreak()
		#On active le mode keypad, permettant la transcription automatique des touches spéciales telles que les flèches en "propriétés curses"
		stdscr.keypad(1)
		#On fait en sorte que getch() ne soit pas bloquant
		stdscr.nodelay(True)
		continue = True
		while continue:
			#On récupère l'entrée utilisateur
			c = stdscr.getch()
			if c == curses.KEY_LEFT:
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
			elif c == curses.KEY_RIGHT:
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
			elif c == curses.KEY_UP:
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
			elif c == curses.KEY_DOWN:
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
				robot.ordre_moteurs(robot,"x21")
			elif c == curses.KEY_ESC
				continue = False
			pass
	#Quand on a fini toute l'application (si celle-ci a une fin), on efface le fichier disant que l'application est lancée (et on restaure le terminal initial)
	finally:
		curses.nocbreak()
		stdscr.keypad(0)
		curses.echo()
		curses.endwin()
		try:
        	os.remove("daemon_python")
        	#os.unlink("daemon_python") est équivalent selon la documentation python, version liens Unix
		except OSError, e:  ## si l'opération échoue, on affiche l'erreur rencontrée (voir au niveau des permissions)
		    print ("Error: %s - %s." % (e.filename,e.strerror))
	    
