import serial
import datetime
import mysql.connector
import time

# Słownik przypisujący UID karty do imienia i nazwiska
card_uid_to_name = {
    "0X17DF5CB": "Jakub Gąsiorski",
    # Dodaj więcej kart w formacie "UID": "Imię i nazwisko"
}

# Ustawienia portu szeregowego
port = "COM11"
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
        if conn.is_connected():
            cursor.close()
            conn.close()

def connect_to_serial():
    while True:
        try:
            ser = serial.Serial(port, baudrate, timeout=1)
            print(f"Połączono z portem: {port}")
            return ser
        except serial.SerialException:
            print(f"Nie można połączyć z portem: {port}. Ponawiam próbę...")
            time.sleep(5)  # Zamiast utime.sleep

def read_from_serial(ser):
    while True:
        try:
            if ser.in_waiting > 0:
                uid = ser.readline().decode('utf-8').strip()
                name = card_uid_to_name.get(uid, "Nieznana karta")
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{name} - Czas: {current_time}")
                #save_to_database(name, current_time)
        except serial.SerialException:
            print("Utracono połączenie z urządzeniem. Ponawiam próbę...")
            ser.close()
            return

if __name__ == "__main__":
    while True:
        ser = connect_to_serial()
        read_from_serial(ser)
