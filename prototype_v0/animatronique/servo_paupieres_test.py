import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

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

# ~ louche()
# ~ moue()
# ~ sleep()
# ~ louche()
# ~ sleep()

#moue()

# droite
# ~ kit.servo[6].angle = 150 # écarquillé
# ~ time.sleep(2)
# ~ kit.servo[6].angle = 130 # très grand ouvert
# ~ time.sleep(2)
# ~ kit.servo[6].angle = 90  # mi-clos
# ~ time.sleep(2)
# ~ kit.servo[6].angle = 60  # clos
# ~ time.sleep(2)

# gauche
# ~ kit.servo[5].angle = 180 # clos
# ~ time.sleep(2)
# ~ kit.servo[5].angle = 150 # mi-clos
# ~ time.sleep(2)
# ~ kit.servo[5].angle = 90  # grand ouvert
# ~ time.sleep(2)
# ~ kit.servo[5].angle = 60  # écarquillé
# ~ time.sleep(2)
for angle in range(180, 50, -10):
	kit.servo[5].angle = angle # clos
	time.sleep(0.5)
