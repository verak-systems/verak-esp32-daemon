import sqlite3
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import logging
from dotenv import load_dotenv
import os

load_dotenv()

LOG_FILE = "/var/log/verak/daemon.log"
con = sqlite3.connect("database/sensor_data.db3")
cur = con.cursor()

# Need to create the table if it doesn't exist


def on_connect(client, userdata, flag, reason_code, props):
    print(f"Connected with {reason_code}")
    client.subscribe("verak/sensors/esp32/digitalTemp")

def on_message(client, userdata, msg):
    print(f"{msg.payload.decode()} from {msg.topic}")
    #cur.execute("insert into data values('')")

def main():
    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="esp32-sub")

    client.on_connect = on_connect
    client.on_message = on_message
    print(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"), os.getenv("PORT"), os.getenv("HOST"))
    client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))
    

    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))

    if isinstance(host, str) and isinstance(port, int): 
        client.connect(host, port, 60)
    
    else:
        raise ValueError("Host or port invalid")

    client.loop_forever()


#with daemon.DaemonContext():
    #main()

if __name__ == "__main__":
    main()
