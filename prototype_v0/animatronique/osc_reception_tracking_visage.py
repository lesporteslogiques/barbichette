"""
  Projet Barbichette
  Réception de messages OSC envoyés par l'ordi "perception"
  3 messages : 
  /posx : abcisse du visage détecté, normalisée entre 0 et 1, -1 si pas de visage
  /posy : ordonnée du vaisage détecté, entre 0 et 1, -1 si pas de visage
  /smile : 1 si sourire détecté, 0 sinon
  20230615, La Baleine
  python 3.7.3 @ tinycheck (RPi4 Raspbian GNU/Linux 10, buster)
  + python OSC
  
"""

# Correspondances (gauche/droite pour la tête)
# commands du côté droit inversées
# 0 : sourcil gauche 			(50, 135)
# 1 : sourcil droit 	(inv) 	(135, 50)
# 2 : machoire basse           	(?, ?)
# 3 : oeil gauche				(50, 130)
# 4 : oeil droit   				(50, 130)
# 5 : paupière gauche			()			PROBLEME
# 6 : paupière droite			()   		PROBLEME
# 7 : bouche gauche				(50, 110)   PROB : refaire mécanisme
# 8 : bouche droite		(inv)	(110, 50)   PROB : refaire mécanisme
# 9 : yeux						(50, 130)

DEBUG = False

from pythonosc import dispatcher, osc_server
import threading
import time
import random
from adafruit_servokit import ServoKit

posx_cible = 0.5
posy_cible = 0.5
sourcil_cible = 0
bouche_ouverte = 0
bouche_ouverte_pre = 0
is_speaking = False

kit = ServoKit(channels=16)   # définir le nombre de canaux de la carte PCA9685


# Équivalent à la fonction map() de Processing
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# Ajuster les positions des servos
def ajuste_regard(posx_cible, posy_cible):
    servo_ogx_cible = map_value(posx_cible, 0, 1, 50, 130)
    servo_odx_cible = map_value(posx_cible, 0, 1, 50, 130)
    servo_oy_cible = map_value(posy_cible, 0, 1, 50, 130)
    
    print("servo_ogx_cible : " + str(servo_ogx_cible))
    print("servo_odx_cible : " + str(servo_odx_cible))
    print("servo_oy_cible : " + str(servo_oy_cible))
    
    kit.servo[3].angle = servo_ogx_cible
    kit.servo[4].angle = servo_odx_cible
    kit.servo[9].angle = servo_oy_cible
  
  
# Ajuster les positions des sourcils
def ajuste_sourcil(sourcil_cible):
    servo_sg_cible = map_value(sourcil_cible, 0, 1, 50.0, 135.0)
    servo_sd_cible = map_value(sourcil_cible, 0, 1, 135.0, 50.0)
    
    print("servo_sg_cible : " + str(servo_sg_cible))
    print("servo_sd_cible : " + str(servo_sd_cible))
    
    kit.servo[0].angle = servo_sg_cible
    kit.servo[1].angle = servo_sd_cible

# Ajuster la position de la bouche
def ajuste_bouche(val):
    if val == 1:
        kit.servo[7].angle = 110.0
        kit.servo[8].angle = 50.0
    else:
        kit.servo[7].angle = 91.0
        kit.servo[8].angle = 91.0

# Gérer les messages OSC reçus
def handle_osc_message(address, *args):
    global posx_cible
    global posy_cible
    global sourcil_cible
    global is_speaking
  
    if address == "/posx":
        posx = args[0]
        if DEBUG:
            print("Position X:", posx)
        # lissage exponentiel de la position en x cible
        if (posx != -1):
            posx_cible = (0.85 * posx_cible) + (0.15 * posx) 

    elif address == "/posy":
        posy = args[0]
        if DEBUG:
            print("Position Y:", posy)
        # lissage exponentiel de la position en y cible
        if (posy != -1):
            posy_cible = (0.85 * posy_cible) + (0.15 * posy) 
        
    elif address == "/smile":
        smile = args[0]
        if DEBUG:
            print("Smile:", smile)
        # actions à réaliser en fonction de smile...
        sourcil_cible = (0.85 * sourcil_cible) + (0.15 * smile) 
  
    elif address == "/speak":
        speak = args[0]
        if DEBUG:
            print("Speak:", speak)
        if speak == 1.0:
            is_speaking = True
        else:
            is_speaking = False  
    


# Créer un dispatcher pour associer des fonctions aux adresses OSC
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/posx", handle_osc_message)
dispatcher.map("/posy", handle_osc_message)
dispatcher.map("/smile", handle_osc_message)
dispatcher.map("/speak", handle_osc_message)

# Créer un serveur OSC qui écoute sur le port spécifié
ip = "0.0.0.0"   # Adresse IP sur laquelle écouter les messages OSC
port = 12345     # Port sur lequel écouter les messages OSC
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Serveur OSC en attente sur {}:{}".format(ip, port))

# Démarrer le serveur OSC dans un thread séparé
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

while True:
    ajuste_regard(posx_cible, posy_cible)
    ajuste_sourcil(sourcil_cible)
    if is_speaking:
        bouche_ouverte = random.choice([0, 0, 0, 0, 1])
        ajuste_bouche(bouche_ouverte)
    # else:
        # ~ if random.randint(0, 500) > 490:
            # ~ if bouche_ouverte != bouche_ouverte_pre:
                # ~ ajuste_bouche(bouche_ouverte)
                # ~ bouche_ouverte_pre = bouche_ouverte
    time.sleep(1)
