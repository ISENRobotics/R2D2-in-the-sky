import Adafruit_BBIO.UART as UART
import serial
import socket

#################################################################################
#################################################################################
#################     Liaison série avec les moteurs     ########################
#################################################################################
#################################################################################


#On choisir la liaison série 4
UART.setup("UART4")

#Ouverture de la liaison série
ser = serial.Serial(port = "/dev/ttyO4", baudrate=9600)
ser.close()
ser.open()
if ser.isOpen():
	print "Serial is open!"
    ser.write("Hello World!")
ser.close()

###################################################################################
###################################################################################
###############     Socket de connexion avec l'application Android      ###########
###################################################################################
###################################################################################


################################
####Partie Serveur-réception####
################################

#On crée le socket de connexion
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Port à définir suivant les possibilités de l'application Android, ici port 12800
connexion_principale.bind(('', 12800))

#Une connexion maximale possible au socket, histoire d'éviter le chevauchement des ordres si deux applications tentent de controler le robot
connexion_principale.listen(1)

#On accepte la connexion
#Attention, la méthode accept bloque le programme tant qu'aucun client ne s'est présenté
connexion_avec_client, infos_connexion = connexion_principale.accept()


################################
####Partie Client-envoi####
################################

#On crée le socket de connexion
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#On connecte le socket sur l'adresse et le port désiré
connexion_avec_serveur.connect(('localhost', 12800))
