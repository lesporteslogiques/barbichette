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

from pythonosc import dispatcher, osc_server
import threading

# Gérer les messages OSC reçus
def handle_osc_message(address, *args):
  if address == "/posx":
    posx = args[0]
    print("Position X:", posx)
    # actions à réaliser en fonction de posx...

  elif address == "/posy":
    posy = args[0]
    print("Position Y:", posy)
    # actions à réaliser en fonction de posy...
        
  elif address == "/smile":
    smile = args[0]
    print("Smile:", smile)
    # actions à réaliser en fonction de smile...

# Créer un dispatcher pour associer des fonctions aux adresses OSC
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/posx", handle_osc_message)
dispatcher.map("/posy", handle_osc_message)
dispatcher.map("/smile", handle_osc_message)

# Créer un serveur OSC qui écoute sur le port spécifié
ip = "0.0.0.0"   # Adresse IP sur laquelle écouter les messages OSC
port = 12345     # Port sur lequel écouter les messages OSC
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Serveur OSC en attente sur {}:{}".format(ip, port))

# Démarrer le serveur OSC dans un thread séparé
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

