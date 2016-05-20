#!/bin/bash
#Activation des liaisons s▒ries
#echo BB-UART1 > /sys/devices/bone_capemgr.9/slots
echo BB-UART2 > /sys/devices/bone_capemgr.9/slots
echo BB-UART4 > /sys/devices/bone_capemgr.9/slots

#Modification du module vid▒o pour aller avec la logitech
rmmod uvcvideo
modprobe uvcvideo nodrop=1 timeout=5000 quirks=0x80
#Lancement du programme
/usr/bin/python /root/R2D2/controleur.py