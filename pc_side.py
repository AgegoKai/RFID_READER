import serial
import datetime
import mysql.connector

# Słownik przypisujący UID karty do imienia i nazwiska
card_uid_to_name = {
    "0X17DF5CB": "Jakub Gąsiorski",
    # Dodaj więcej kart w formacie "UID": "Imię i nazwisko"
}

# Ustawienia portu szeregowego
port = "COM5"
baudrate = 9600

# Ustawienia połączenia z MySQL
db_config = {
    'host': 'localhost',
    'user': 'twoj_uzytkownik',
    'password': 'twoje_haslo',
    'database': 'CardReadings'
}

def save_to_database(name, reading_time):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO readings (name, reading_time) VALUES (%s, %s)"
        cursor.execute(query, (name, reading_time))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Błąd bazy danych: {e}")
    finally:
        cursor.close()
        conn.close()

def read_from_serial():
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Połączono z portem: {port}")
        while True:
            if ser.in_waiting > 0:
                uid = ser.readline().decode('utf-8').strip()
                name = card_uid_to_name.get(uid, "Nieznana karta")
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{name} - Czas: {current_time}")
                save_to_database(name, current_time)
    except serial.SerialException as e:
        print(f"Błąd połączenia: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    read_from_serial()
