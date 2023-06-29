#!/usr/bin/env python3

# source : https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/
# arduino relié à /dev/ttyUSB0 (pour trouver le port : ls /dev/tty*)
# baud rate à 19200, correspond à celui défini dans arduino
# timeout : durée allouée à la lecture série
# readline() : lit jusqu'au caractère de fin de ligne
# decode('utf- 8') : transforme les bytes réçues dans le type souhaité
# rstrip() : retire les caractères de fin de ligne
import serial
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)
    # vider le buffer série en début de communication
    ser.reset_input_buffer()
    while True:
		# y a t'il des données en attente ?
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
