"""
  Projet Barbichette
  Envoi de messages OSC, pour simuler un 2 ordi
  3 messages : 
  /posx : abcisse du visage détecté, normalisée entre 0 et 1, -1 si pas de visage
  /posy : ordonnée du vaisage détecté, entre 0 et 1, -1 si pas de visage
  /smile : 1 si sourire détecté, 0 sinon
  20230615, La Baleine
  python 3.7.3 @ tinycheck (RPi4 Raspbian GNU/Linux 10, buster)
    + python OSC 1.8.1
  
"""

import time
import random
from pythonosc import udp_client

random.seed(1)

# Adresse IP et port du destinataire OSC
ip = "127.0.0.1"    # Adresse IP du destinataire OSC
port = 12345        # Port du destinataire OSC

# Créer un client OSC
client = udp_client.SimpleUDPClient(ip, port)

# Envoyer des valeurs à intervalle régulier
while True:
    posx = random.random()
    posy = random.random()
    smile = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])

    # Envoyer les valeurs en OSC
    client.send_message("/posx", posx)
    client.send_message("/posy", posy)
    client.send_message("/smile", int(smile))  # Les valeurs booléennes sont converties en entiers (0 ou 1) pour OSC

    time.sleep(2) # Attendre x seconde(s)

# Fermer le client OSC
client.close()

