import daemon

import logging
import paho.mqtt.client as mqtt
from paho.mqtt.enums import *

LOG_FILE = "/var/log/verak-daemon.log"


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("verak/sensors/esp32/digitalTemp")


def on_message(client, userdata, msg):
    print(f"Received {msg.payload.decode()} from {msg.topic}")


class Daemon(DaemonRunner):
    def __init__(self) -> None:
        self.stdin_path = '/dev/null'
        self.stdout_path = LOG_FILE
        self.stderr_path = LOG_FILE
        self.pidfile_path = "/var/run/verak-daemon.pid"
        self.pidfile_timeout = 5
        super().__init__(self)

    def run(self):
        with daemon.DaemonContext(
            stdin=open(self.stdin_path, 'r'),
            stdout=open(self.stdout_path, 'a+'),
            stderr=open(self.stderr_path, 'a+'),
            pidfile=self.pidfile_path
            ):
            self.main_loop()

    def main_loop(self):
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
        logging.info("Daemon Started")
        client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="esp32-Sub")
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set("esp", "Hunter123.")

        client.connect("10.0.0.186", 1883, 60)

        while True:
            client.loop_forever()
