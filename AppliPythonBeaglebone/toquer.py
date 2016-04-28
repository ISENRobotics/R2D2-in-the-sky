# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:11:53 2016

@author: Kany
"""


class Serveur(object):
    def __init__(self,ident):
        self.ident=ident

class Surveillance_serveur(object):
    def __init__(self,controleur,ident):
        self.pere   =controleur
        self.serveur=Serveur(ident)
    def kill(self):
        del self.serveur
        self.serveur=Serveur(2)
        self.pere.mise_a_jour(self.serveur)

        
class Algorithmique(object):
    def __init__(self,controleur):
        self.serveur=controleur.surveillance.serveur 
        
class Controleur(object):
    def __init__(self,ident):
        self.surveillance=Surveillance(self,ident)
        self.algorithmique=Algorithmique(self)
    def mise_a_jour(self,serveur):
        self.algorithmique.serveur=serveur
        

c=Controleur(1)
print(c.algorithmique.serveur.ident)
print(c.surveillance.serveur)
print(c.algorithmique.serveur)

c.surveillance.kill()
print(c.surveillance.serveur.ident)
print(c.surveillance.serveur)
print(c.algorithmique.serveur.ident)
print(c.algorithmique.serveur)        
