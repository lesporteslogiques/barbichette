#!/usr/bin/python3

# Animation par interface graphique de la tête animatronique
# les commandes sont envioyées directement aux servo sans passer par OSC
# python 3.5.3
#   + pyyaml 3.12 ( pip3 show pyyaml )
#   	* https://pyyaml.org/wiki/PyYAMLDocumentation
#   + argparse 1.4.0
#   	* https://docs.python.org/3/library/argparse.html
#       * https://docs.python.org/fr/3/howto/argparse.html
#   + guizero 1.4.0
#		* 


# fonctionnement général
import os
import sys
import argparse    # traitement des arguments de la ligne de commande
import yaml        # format utilisé pour le fichier de configuration

# imports pour contrôle de la tête animatronique
import time
from adafruit_servokit import ServoKit

# imports GUI
from guizero import App, Text, Slider, Box, PushButton

# Traitement des arguments en ligne de commande ***********************

parser = argparse.ArgumentParser(description="Test arguments et fichiers de configuration",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-v", "--verbose", type=int, choices=[0, 1, 2], default=0, help="informations de debug")
parser.add_argument("-config", default="0", help="Fichier de configuration (yaml)")
args = parser.parse_args()

# Traitement du fichier de configuration si nécessaire ****************

if args.config != "0":
    if os.path.exists(args.config):
        with open(args.config, "r") as fp:
            args_yaml = yaml.safe_load(fp)
    else:
        print("le fichier " + args.config + " n'existe pas!");
        print("fin du script");
        exit()

# Traitement des valeurs récupérées dans l'étape de config


# Définir le nombre de canaux de la carte PCA9685 (1 canal = 1 servo)
kit = ServoKit(channels=16)

# *********************************************************************
# Fonctions d'animations
# *********************************************************************
# Correspondances (gauche/droite pour la tête)
# commands du côté droit inversées
# 0 : sourcil gauche 			(50, 135)
# 1 : sourcil droit 	(inv) 	(135, 50)
# 2 : machoire basse           	(?, ?)
# 3 : oeil gauche				(50, 130)
# 4 : oeil droit   				(50, 130)
# 5 : paupière gauche			(180, 60) (clos, écarquillé) /!\ pas linéaire			
# 6 : paupière droite			(60, 150) (clos, écarquillé) /!\ pas linéaire	  		
# 7 : bouche gauche				(50, 110)   PROB : refaire mécanisme
# 8 : bouche droite		(inv)	(110, 50)   PROB : refaire mécanisme
# 9 : yeux						(50, 130)

def moue():
	kit.servo[0].angle = 50
	kit.servo[1].angle = 135
	kit.servo[2].angle = 120
	kit.servo[3].angle = 70
	kit.servo[4].angle = 110
	# ~ kit.servo[5].angle = 100
	# ~ kit.servo[6].angle = 100
	kit.servo[7].angle = 110
	kit.servo[8].angle = 50
	kit.servo[9].angle = 130
	time.sleep(2)
	
def sleep():
	kit.servo[0].angle = 90
	kit.servo[1].angle = 90
	kit.servo[2].angle = 90
	kit.servo[3].angle = 90
	kit.servo[4].angle = 90
	# ~ kit.servo[5].angle = 90
	# ~ kit.servo[6].angle = 90
	kit.servo[7].angle = 90
	kit.servo[8].angle = 90
	kit.servo[9].angle = 90
	time.sleep(2)
	
def louche():
	kit.servo[0].angle = 135
	kit.servo[1].angle = 50
	kit.servo[2].angle = 120
	kit.servo[3].angle = 130
	kit.servo[4].angle = 50
	# ~ kit.servo[5].angle = 100
	# ~ kit.servo[6].angle = 100
	kit.servo[7].angle = 110
	kit.servo[8].angle = 50
	kit.servo[9].angle = 130
	time.sleep(2)

def reset():
	
	# sourcil gauche
	kit.servo[0].angle = 90
	slider7_va.value = 90
	slider7.value = 90
	
	# sourcil droit
	kit.servo[1].angle = 90
	slider8_va.value = 90
	slider8.value = 90
	
	# sourcils
	slider9_va.value = 90
	slider9.value = 90	
	
	# machoire basse
	kit.servo[2].angle = 120
	
	# oeil gauche
	kit.servo[3].angle = 90
	slider4_va.value = 90
	slider4.value = 90
	
	#oeil droit
	kit.servo[4].angle = 90
	slider5_va.value = 90
	slider5.value = 90
	
	# regard
	slider6_va.value = 90
	slider6.value = 90
	
	# paupière gauche
	kit.servo[5].angle = 120
	slider1_va.value = 120
	slider1.value = 120
	
	# paupière droite
	kit.servo[6].angle = 105
	slider2_va.value = 105
	slider2.value = 105
	
	# bouche gauche
	kit.servo[7].angle = 110
	
	# bouche droite
	kit.servo[8].angle = 50
	
	# hauteur des yeux
	kit.servo[9].angle = 90
	slider3_va.value = 90
	slider3.value = 90

	

# *********************************************************************
# GUI
# *********************************************************************



def paupiere_gauche(sv):
    #client.send_message("/rec/data", [float(slider1_value), 1, 2., "hello"])  # Send message with float, int, float and string
    print("paupiere gauche : " + sv)
    kit.servo[5].angle = int(sv)
    slider1_va.value = sv

def paupiere_droit(sv):
    #client.send_message("/rec/truc", float(slider2_value))
    print("paupiere droite : " + sv)
    kit.servo[6].angle = int(sv)
    slider2_va.value = sv

def paupieres(sv):
	print("actionner les 2 paupières : " + sv)
	paupiere_gauche(sv)
	paupiere_droit(sv)
	slider1.value = sv
	slider2.value = sv
	slider10_va.value = sv

def yeux_hauteur(sv):
    #client.send_message("/rec/truc", float(slider2_value))
    print(sv)
    kit.servo[9].angle = int(sv)
    slider3_va.value = sv
      
def oeil_gauche(sv):
    #client.send_message("/rec/truc", float(slider2_value))
    print(sv)
    kit.servo[3].angle = int(sv)
    slider4_va.value = sv
    
def oeil_droit(sv):
    #client.send_message("/rec/truc", float(slider2_value))
    print(sv)
    kit.servo[4].angle = int(sv)
    slider5_va.value = sv
    
def regard(sv):
    #client.send_message("/rec/truc", float(slider2_value))
    print(sv)
    oeil_gauche(sv)
    oeil_droit(sv)
    slider6_va.value = sv
    slider4.value = sv
    slider5.value = sv
    
def sourcil_gauche(sv):
	print("sourcil gauche : " + sv)
	kit.servo[0].angle = int(sv)
	slider7_va.value = sv
	
def sourcil_droit(sv):
	print("sourcil droit : " + sv)
	kit.servo[1].angle = int(sv)
	slider8_va.value = sv
	
def sourcils(sv):
	print("sourcils : " + sv)
	sourcil_gauche(sv)
	sourcil_droit(sv)
	slider9_va.value = sv
	slider7.value = sv
	slider8.value = sv
	
def fermer_yeux():
	kit.servo[5].angle = 180
	kit.servo[6].angle = 60
	
def ouvrir_yeux():
	kit.servo[5].angle = 80
	kit.servo[6].angle = 120

# client = SimpleUDPClient(ip, port)  # Create client
app = App(title="animation de la tête animatronique")
# message = Text(app, text="test pour envoyer des commandes OSC")

slider1_box = Box(app, width="fill", align="top")
slider1 = Slider(slider1_box, width="300", command=paupiere_gauche, align="left", start=60, end=180)
slider1_ad = Text(slider1_box, text="paupière gauche", align="left")
slider1_va = Text(slider1_box, text=slider1.value, align="left")

slider2_box = Box(app, width="fill", align="top")
slider2 = Slider(slider2_box, width="300", command=paupiere_droit, align="left", start=60, end=150)
slider2_ad = Text(slider2_box, text="paupière droite", align="left")
slider2_va = Text(slider2_box, text=slider2.value, align="left")

slider10_box = Box(app, width="fill", align="top")
slider10 = Slider(slider10_box, width="300", command=paupieres, align="left", start=60, end=150)
slider10_ad = Text(slider10_box, text="paupières", align="left")
slider10_va = Text(slider10_box, text=slider10.value, align="left")

slider3_box = Box(app, width="fill", align="top")
slider3 = Slider(slider3_box, width="300", command=yeux_hauteur, align="left", start=50, end=130)
slider3_ad = Text(slider3_box, text="yeux hauteur", align="left")
slider3_va = Text(slider3_box, text=slider3.value, align="left")

slider4_box = Box(app, width="fill", align="top")
slider4 = Slider(slider4_box, width="300", command=oeil_gauche, align="left", start=50, end=130)
slider4_ad = Text(slider4_box, text="oeil gauche", align="left")
slider4_va = Text(slider4_box, text=slider4.value, align="left")

slider5_box = Box(app, width="fill", align="top")
slider5 = Slider(slider5_box, width="300", command=oeil_droit, align="left", start=50, end=130)
slider5_ad = Text(slider5_box, text="oeil droit", align="left")
slider5_va = Text(slider5_box, text=slider5.value, align="left")

slider6_box = Box(app, width="fill", align="top")
slider6 = Slider(slider6_box, width="300", command=regard, align="left", start=50, end=130)
slider6_ad = Text(slider6_box, text="regard", align="left")
slider6_va = Text(slider6_box, text=slider6.value, align="left")

slider7_box = Box(app, width="fill", align="top")
slider7 = Slider(slider7_box, width="300", command=sourcil_gauche, align="left", start=50, end=130)
slider7_ad = Text(slider7_box, text="sourcil gauche", align="left")
slider7_va = Text(slider7_box, text=slider7.value, align="left")

slider8_box = Box(app, width="fill", align="top")
slider8 = Slider(slider8_box, width="300", command=sourcil_droit, align="left", start=50, end=130)
slider8_ad = Text(slider8_box, text="sourcil droit", align="left")
slider8_va = Text(slider8_box, text=slider8.value, align="left")

slider9_box = Box(app, width="fill", align="top")
slider9 = Slider(slider9_box, width="300", command=sourcils, align="left", start=50, end=130)
slider9_ad = Text(slider9_box, text="sourcils", align="left")
slider9_va = Text(slider9_box, text=slider9.value, align="left")

bouton_1 = PushButton(app, text="fermer yeux", command=fermer_yeux)
bouton_2 = PushButton(app, text="ouvrir yeux", command=ouvrir_yeux)

reset()   # Mettre tout en position neutre

app.display()




 
