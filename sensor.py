# Sensor.py
from DBconnector import dbLog
import datetime

import RPi.GPIO as GPIO
import time

# Definierte GPIO-Pins
PIR_GPIO = 21  # Bewegungsmelder-Eingang
PIR_GPIO2 = 19  # LED-Ausgang oder anderes Ausgangsgerät

# GPIO-Setup und Initialisierung
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIR_GPIO2, GPIO.OUT)
GPIO.setwarnings(False)

# Callback-Funktion für Bewegungserkennung
def motion_detected_callback(channel):
    global con
    print("Motion detected at " + str(time.ctime()))
    GPIO.output(PIR_GPIO2, GPIO.HIGH)
    # Hier kannst du die Datenbankprotokollierung hinzufügen oder andere Aktionen ausführen
    Date = datetime.datetime.now()
    Event = "Bewegung festgestellt"
    User = None 
    dbLog(con, Date, Event, User)
    time.sleep(2)
    GPIO.output(PIR_GPIO2, GPIO.LOW)

# Event-Handler-Funktion zum Starten des Bewegungssensors
def setup_motion_sensor(conn):
    con = conn
    GPIO.add_event_detect(PIR_GPIO, GPIO.RISING, callback=motion_detected_callback)
    print("Bewegungssensor aktiv.")

# Clean-up Funktion
def cleanup():
    GPIO.cleanup()
