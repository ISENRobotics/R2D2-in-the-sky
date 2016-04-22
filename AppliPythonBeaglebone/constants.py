#constants.py

#Mot de commande, a envoyer avant chaque commande
CMD = "00"

#Mot permettant de récupérer la vitesse du moteur 1, effectuer une lecture série après son envoi
GET_SPEED_1 = "21"

#Mot permettant de récupérer la vitesse du moteur 2, effectuer une lecture série après son envoi
GET_SPEED_2 = "22"

#Mot permettant de récupérer la valeur de l'encodeur 1 
#nécessite une variable 32 BITS OBLIGATOIREMENT
GET_ENCODER_1 = "23"

#Mot permettant de récupérer la valeur de l'encodeur 2
#nécessite une variable 32 BITS OBLIGATOIREMENT
GET_ENCODER_2 = "24"

#Mot permettant de récupérer la valeur de l'encodeur 1 et 2 à la suite
#nécessite deux variables 32 BITS OBLIGATOIREMENT
GET_ENCODERS = "25"

#Mot permettant de récupérer la valeur de voltage de la batterie connectée.
#La valeur de retour vaut 10 fois la valeur réelle (121 pour 12.1V)
GET_VOLTS = "26"

#Mot permettant de récupérer l'ampérage du moteur 1
#Même principe que pour GET_VOLTS, 10 fois la valeur réelle (25 pour 2.5A)
GET_CURRENT_1 = "27"

#Mot permettant de récupérer l'ampérage du moteur 2
#Même principe que pour GET_VOLTS, 10 fois la valeur réelle (25 pour 2.5A)
GET_CURRENT_2 = "28"

#Mot permettant de récupérer la version du software du contrôleur
GET_VERSION = "29"

#Mot permettant de récupérer l'accélération de l'ensemble
GET_ACCELERATION = "2A"

#Mot permettant de récupérer le mode de fonctionnement du controleur
#Mode 0 : moteurs acceptant des valeurs de 0 (départ à fond en arrière) à 255 (départ à fond en avant)
#Mode 1 : moteurs acceptant des valeurs de -128 (départ à fond en arrière) à 127 (départ à fond en avant)
#Mode 2 : La variable SPEED_1 controle la vitesse des deux moteurs, SPEED_2 controle la rotation, valeurs acceptées de 0 à 255
#Mode 3 : Similaire à Mode 2, mais avec des valeurs allant de -128 à 127
GET_MODE = "2B"

#Mot renvoyant la concaténation de GET_VOLTS et GET_CURRENTS
GET_VOLTS_AND_CURRENTS = "2C"

#Liste python regroupant tous les GET, ne sert que dans l'algorithmique
LIST_GET = [GET_SPEED_1,GET_SPEED_2,GET_ENCODER_1,GET_ENCODER_2,GET_ENCODERS,GET_VOLTS,GET_CURRENT_1,GET_CURRENT_2,GET_VERSION,GET_ACCELERATION,GET_MODE,GET_VOLTS_AND_CURRENTS]

#Mot permettant d'assigner une valeur pour la vitesse du moteur 1
#Valeurs acceptées : cf GET_MODE
#MODES ACCEPTES : 0 et 1
SET_SPEED_1 = "31"

#Mot permettant d'assigner une valeur pour la vitesse du moteur 2
#Valeurs acceptées : cf GET_MODE
#MODES ACCEPTES : 0 et 1
SET_SPEED_2 = "32"

#Mot permettant d'assigner une valeur pour la rotation
#Valeurs acceptées : cf GET_MODE
#MODES ACCEPTES : 2 et 3
SET_SPEED = "31"

#Mot permettant d'assigner une valeur pour la rotation
#Valeurs acceptées : cf GET_MODE
#MODES ACCEPTES : 2 et 3
TURN = "32"

LIST_SET = [SET_SPEED_1,SET_SPEED_2]

#Mot permettant d'assigner une valeur pour l'accélération des moteurs
#Valeurs acceptées : 1 à 10
SET_ACCELERATION = "33"

#Mot permettant d'assigner une valeur pour le mode de fonctionnement
#Mode 0 : moteurs acceptant des valeurs de 0 (départ à fond en arrière) à 255 (départ à fond en avant)
#Mode 1 : moteurs acceptant des valeurs de -128 (départ à fond en arrière) à 127 (départ à fond en avant)
#Mode 2 : La variable SPEED_1 controle la vitesse des deux moteurs, SPEED_2 controle la rotation, valeurs acceptées de 0 à 255
#Mode 3 : Similaire à Mode 2, mais avec des valeurs allant de -128 à 127
SET_MODE = "34"

#Mot de commande remettant à 0 les deux encodeurs des moteurs
RESET_ENCODERS = "35"

#Mot de commande désactivant la régulation de la puissance par les encodeurs 
#ATTENTION, A UTILISER AVEC PRECAUTION
DISABLE_REGULATOR = "36"

#Mot de commande activant la régulation de la puissance par les encodeurs 
#ACTIVE PAR DEFAUT
ENABLE_REGULATOR = "37"

#Mot de commande désactivant la cessassion de communication quand la liaison n'a pas communiqué depuis un certain temps
DISABLE_TIMEOUT = "38"

#Mot de commande activant la cessassion de communication après 2 secondes sans communication sur la liaison
ENABLE_TIMEOUT = "39"