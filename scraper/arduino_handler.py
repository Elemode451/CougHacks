import serial
import requests
import json

ser = serial.Serial('/dev/ttyACM0', 9600) 

while True:
    line = ser.readline().decode().strip()
    try:
        data = json.loads(line)
        print("Received from Arduino:", data)

        res = requests.post("http://localhost/register", json=data)
        print("Backend response:", res.json())
    except json.JSONDecodeError:
        print("bad data:", line)
