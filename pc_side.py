import serial
import datetime
import mysql.connector
import time

# Słownik przypisujący UID karty do imienia i nazwiska
card_uid_to_name = {
    "Card detected 017E018B": "Ania",
    "Card detected 017BDE8B": "Jryna",
    "Card detected 017E01BB": "Ola",
    # Dodaj więcej kart w formacie "UID": "Imię i nazwisko"
}

# Ustawienia portu szeregowego
port = "COM4"
baudrate = 9600

# Ustawienia połączenia z MySQL
db_config = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
}

def save_to_database(name, reading_time):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = f"INSERT INTO work_times (employee) VALUES ('{name}')"
        print(query)
        cursor.execute(query)
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
                uid = str(ser.readline().decode('utf-8').strip())
                name = card_uid_to_name.get(uid, "Nieznana karta")
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{name} - Czas: {current_time}")
                print(uid)
                save_to_database(name, current_time)
        except serial.SerialException:
            print("Utracono połączenie z urządzeniem. Ponawiam próbę...")
            ser.close()
            return

if __name__ == "__main__":
    while True:
        ser = connect_to_serial()
        read_from_serial(ser)
