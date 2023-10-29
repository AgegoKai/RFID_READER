from mfrc522 import MFRC522
import utime
from machine import Pin

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring

# Konfiguracja dla Raspberry Pi Pico
reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)
led = Pin(17, Pin.OUT)  # Ustaw pin GP17 jako wyjściowy dla diody LED

print("")
print("Please place card on reader")
print("")

PreviousCard = [0]

try:
    while True:
        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if uid == PreviousCard:
                continue
            if stat == reader.OK:
                uid_str = uidToString(uid)
                print("Card detected {}".format(uid_str))
                
                # Zapal diodę LED
                led.value(1)
                utime.sleep_ms(500)  # Dioda będzie świecić przez 0,5 sekundy
                led.value(0)  # Wyłącz diodę LED
                
                PreviousCard = uid
            else:
                pass
        else:
            PreviousCard = [0]
        utime.sleep_ms(50)
except KeyboardInterrupt:
    pass
