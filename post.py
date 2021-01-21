import json
import requests
import board
import adafruit_dht
import pytz
from datetime import datetime
import configparser

dhtDevice = adafruit_dht.DHT22(board.D4)

def post(url, data):
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }

    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.text)

if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read('/home/pi/temp/config.ini')
    
    while True:
        try:
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            
        except RuntimeError as error:
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

        if (temperature_c is None) or (humidity is None):
            continue
        
        temperature_f = temperature_c*(9/5)+32
        
        localtime = datetime.now(pytz.timezone(cfg['device']['tz']))
        localtime_str = localtime.strftime("%m/%d/%Y %H:%M:%S")
            
        data = {
            'location': cfg['device']['location'],
            'timestamp': localtime_str,
            'sensors': [
                {
                    'sensorType': 'DHT22',
                    'temperature': round(temperature_f,2),
                    'humidity': round(humidity,2)
                }
            ]
        }

        try:
            post(cfg['server']['url'], data)
        except Exception as error:
            raise error

        break
        
