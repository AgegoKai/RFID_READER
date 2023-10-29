# RFID Access Control System

An access control system based on an RFID card reader with Raspberry Pi Pico. It allows scanning RFID cards, reading their unique identifiers (UID), and logging this information in a database along with the date and time of the read.

## Required Components

- Raspberry Pi Pico
- MFRC522 RFID Reader
- Micro USB Cable
- RFID Card
- LED (optional)
- Resistor (optional, for the LED)
- Computer with access to a serial port (COM)
- MySQL Workbench (for database configuration)

## Hardware Setup

1. **Connecting the RFID Reader to Raspberry Pi Pico:**
   - VCC to 3v3V (OUT)
   - GND to GND
   - RST to GP22
   - MISO to GP2
   - MOSI to GP3
   - SCK to GP4
   - NSS to GP5
   - IRQ not used

2. **Connecting the LED:**
   - LED anode to GP17 on Raspberry Pi Pico
   - LED cathode to GND through a resistor (e.g., 220Ω)

## Software Configuration

### Raspberry Pi Pico

1. Ensure you have the Micropython environment installed on your Raspberry Pi Pico.
2. Copy the code for handling the RFID reader and save it as `main.py` on Raspberry Pi Pico.

### MySQL Database

1. Launch MySQL Workbench.
2. Create a new database.
3. Create a table to store card read data. Execute the following SQL script:

   ```sql
   CREATE TABLE AccessLogs (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       surname VARCHAR(255) NOT NULL,
       access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   
### Computer

1. Install required Python libraries including `pyserial` and `mysql-connector-python`.
2. Copy the code to read data from the serial port and save it to the database.
3. In the `pc_side.py` file, update the following lines with your database user and password:
   ```python
   db_user = 'your_user'
   db_password = 'your_password'

## Usage

1. Run the Raspberry Pi Pico with the connected RFID reader.
2. Run the Python script on the computer to read data from the serial port.
3. Hold the RFID card to the reader.
4. Check if the LED lights up momentarily, indicating a card read.
5. Check if the read data (name, surname, date, time) has been saved in the database.

## Troubleshooting

In case of any issues, make sure that:
- All connections are correct.
- Raspberry Pi Pico is properly programmed.
- The script on the computer is correctly configured and has access to the serial port and the database.
- The COM port in the computer script (`pc_side.py`) is correctly set to match the port to which Raspberry Pi Pico is connected. Change the COM port in the script if necessary.
