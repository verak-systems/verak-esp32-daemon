from enum import CONFORM
import daemon
import sqlite3
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import logging

LOG_FILE = "/var/log/verak/daemon.log"
con = sqlite3.connect("database/sensor_data.db3")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS ")

def on_connect(client, userdata, flag, reason_code, props):
   client.subscribe("verak/sensors/esp32/digitalTemp")

def on_message(client, userdata, msg):
    cur.execute("insert into data values('')")

def main():
    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="esp32-sub")
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("esp")-

