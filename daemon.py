import sqlite3
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import logging
from dotenv import load_dotenv
import os
import json

load_dotenv()

LOG_FILE = "/var/log/verak/daemon.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
con = sqlite3.connect("database/sensor_data.db3")
cur = con.cursor()

# TODO:
# Need to create the table if it doesn't exist
# Change all print statments to logging statements


def on_connect(client, userdata, flag, reason_code, props):
    logging.info(f"Connected with {reason_code}")
    client.subscribe("verak/sensors/esp32/#")

def on_message(client, userdata, msg):
    # payload = json.loads(msg.payload.decode())
    print(f"{msg.payload.decode()} from {msg.topic}")
   
    try:   
        identifier = msg.topic.split("/")[-1]

        if identifier == "analogTemp":
            cur.execute("select id from unit where value = 'C'")
            test = cur.fetchall()
            print(test)

        elif identifier == "digitalTemp":
            pass
        #sql = f"insert into data values(?, ?, ?, ?, ?, ?)"
        #cur.execute(sql, (
            #payload['device'],
           # payload['digitalTemp'],
          #payload['unit'],
         #   payload['timestamp'],
        #))

       # con.commit()
    except Exception as ex:
        print(f"{ex}")
        

def main():
    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="esp32-sub")

    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))
    

    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))

    if isinstance(host, str) and isinstance(port, int): 
        client.connect(host, port, 60)
    
    else:
        raise ValueError("Host or port invalid")

    client.loop_forever()

if __name__ == "__main__":
    main()
