import mysql.connector
from mysql.connector import Error
import datetime

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "alarm_system"
        )
        if conn.is_connected():
            print(f"Verbindung zur Datenbank erfolgreich")
            return conn, True
    except:
        print(f"Fehler beim Verbinden: {e}")
        return None, False
    

def is_authorized(conn, testID):
    try:
        cursor = conn.cursor()

        query = "SELECT name FROM user WHERE rfid = %s"
        cursor.execute(query, (testID,))

        result = cursor.fetchone()
        cursor.close

        if result:
            return True, result[0]
        else:
            return False, None 

    except:
        print(f"Fehler beim Abrufen der Daten: {err}")
        return False, None
    

def is_admin(conn, testID):
    try:
        cursor = conn.cursor()

        query = "SELECT name FROM user WHERE rfid = %s AND rolle = 'admin'"
        cursor.execute(query, (testID,))

        result = cursor.fetchone()
        cursor.close

        if result:
            return True, result[0]
        else:
            return False, None 

    except:
        print(f"Fehler beim Abrufen der Daten: {err}")
        return False, None

def dbLog(conn, Date, Event, User):
    try:
        print(Date, Event, User)
        cursor = conn.cursor()
        # query = (
        #     "INSERT INTO 'incidents' ('date', 'event', 'user') " 
        #     "VALUES (%s, %s, %s)"
        # )
        query = "INSERT INTO incidents (date, event, user) VALUES (%s, %s, %s)"
        print(query)
        data =  (Date, Event, User)
        data = (data[0].replace(microsecond=0), data[1], data[2])
        print(data)
        print("hallo")
        cursor.execute(query, data)
        conn.commit()
        print("Erfolgreich hochgeladen")

    except:
        print(f"Fehler beim Schreiben der Daten auf die Datenbank 'Incidents': {e}")

