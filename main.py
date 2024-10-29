#Benötigte Bibliotheken
import RPi.GPIO as GPIO
import mfrc522
import time
import datetime
import sensor
from mfrc522 import SimpleMFRC522
from mfrc522 import MFRC522
from DBconnector import get_db_connection
from DBconnector import is_authorized
from DBconnector import is_admin
from DBconnector import dbLog
reader = SimpleMFRC522()
reader2 = MFRC522()

#Datenbankenverbindung herstellen

conn, connected = get_db_connection()


#==========FUNKTIONEN==========

def writeTag(reader): #Funktion zum Überschreiben den "Texts" auf dem Tag
    text = input('Enter tag data:')
    print("Hold tag to module")
    reader.write(text)
    print("Done...")
            
def readTag(reader): #Funktion zum lesen der "ID" und des "TEXTS" auf dem Tag
    id, text = reader.read()
    print(id)
    print(text)
def readAdmin(reader): #Funktion zum erkennen des Admin Status. 
    id, text = reader.read()
    isAdmin, name = is_admin(conn, id) #Gibt TRUE und den Namen zurück wenn die gegebene ID in der Datenbank mit dem Zusatz "Admin" hinterlegt ist
    if isAdmin:
        return True, name
    else: 
        return False, name
def checkTag(reader): #Checkt ob der Benutzer zugriff zum Raum hat
    print("Bitte halte deine Karte bereit")
    id, text = reader.read()
    accepted, name = is_authorized(conn, id) #Gibt TRUE und den Namen zurück, wenn die ID in der Users Datenbank vorhanden ist.
    global status
    if accepted:
        print(f"Ja cool komm rein, {name}") 
        
        Date = datetime.datetime.now()
        Event = "Zuganggewaehrt"
        User = id
        
        if conn.is_connected():  # Bei MySQL, für andere Datenbanken siehe jeweilige Dokumentation
            dbLog(conn, Date, Event, User)
        else:
            print("Datenbankverbindung nicht aktiv.") #Speichert das Event in der Incidents Datenbank
    else:
        print("du kommst hier nich rein!")
        
        Date = datetime.datetime.now()
        Event = "Zugang nicht gewaehrt"
        User = id

        print(Date, Event, User)
        
        if conn.is_connected():  # Bei MySQL, für andere Datenbanken siehe jeweilige Dokumentation
            dbLog(conn, Date, Event, User)
        else:
            print("Datenbankverbindung nicht aktiv.") #Speichert das Event in der Incidents Datenbank
    
#==========MAIN LOOP==========
sensor.setup_motion_sensor(conn)
while True:
    status = None
    while status != reader2.MI_OK:
        (status,TagType) = reader2.MFRC522_Request(reader2.PICC_REQIDL)
        if status == reader2.MI_OK:
            try:
                idTest, name = readAdmin(reader) #Bekommt TRUE (Bei Admin) oder FALSE wieder
                if idTest: #Wenn kein Admin wird nur die checkTag Funktion getriggert
                    isAdmin = True #Wenn Admin wird eine oberfläche zur Auswahl getriggert
                    while isAdmin:
                        input1 = None
                        print("====================")
                        print(f"Hallo {name}")
                        print("Willkommen in der Admin übersicht.")
                        input1 = input("Willst du tun? Tag Lesen (l) / Tag beschreiben (s) / Eingang checken (c) / abmelden (a) ")
                        time.sleep(1)
                        #print("Dein Input ist:")
                        print(input1)
                        if input1 == "l":
                            print("Lesemodul aktiv")
                            print("halte das Tag an das Lesegerät")
                            time.sleep(0.1)
                            readTag(reader)
                            print("====================")
                        elif input1 == "s":
                            writeTag(reader)
                            print("====================")
                        elif input1 == "c":
                            checkTag(reader)
                            print("====================")
                        elif input1 == "a":
                            print(f"Auf Widersehen {name}")
                            print("====================")
                            isAdmin = False
                            status = None
                        else:
                            print("ich konnte deinen Input nicht zuordnen. Bitte versuche es erneut")
                else:
                    checkTag(reader)
                    
            except KeyboardInterrupt:
                print("Programm manuell angehalten")
                GPIO.cleanup()
            
            except:
                print("FEHLER!!!")
                GPIO.cleanup()
                
            finally:
                GPIO.cleanup()
        


            
                
            
   
    
    
