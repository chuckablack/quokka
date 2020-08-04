import yaml
import requests
import random
import time
import psutil
from datetime import datetime
import argparse

NUM_CONSECUTIVE_FAILURES_REQUIRED = 3
INTERVAL_TIME = 60

filename = "devices.yaml"
with open("quokka/data/" + filename, "r") as import_file:
    devices = yaml.safe_load(import_file.read())

parser = argparse.ArgumentParser(description="Simulate SDWAN devices")
parser.add_argument('-quokka',  default='localhost', help='IP address of quokka server')
args = parser.parse_args()
quokka_ip = args.quokka
print(f"Quokka IP: {quokka_ip}")

# This dict keeps track of devices' failures - we must fail a couple times in a row in order
# for the monitoring software to be aware that the device is unavailable
consecutive_failures = dict()
for device in devices:
    consecutive_failures[device["id"]] = 0

while True:

    for device in devices:

        if device["transport"] != "HTTP-REST":
            continue

        if consecutive_failures[device["id"]] > 0:
            print(
                f"{str(datetime.now())[:-3]}: SKIPPING HEARTBEAT (again) for {device['name']}, countdown={consecutive_failures[device['id']]}"
            )
            consecutive_failures[device["id"]] -= 1
            continue

        # Fail to send heartbeat 1/20th of the time
        if random.randint(1, NUM_CONSECUTIVE_FAILURES_REQUIRED*10/NUM_CONSECUTIVE_FAILURES_REQUIRED) == 1:
            print(
                f"{str(datetime.now())[:-3]}: SKIPPING HEARTBEAT for {device['name']}"
            )
            consecutive_failures[device["id"]] = NUM_CONSECUTIVE_FAILURES_REQUIRED
            continue

        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()[2]

        heartbeat_info = {
            "name": device["name"],
            "serial": device["serial"],
            "response_time": device["response_time"] if "response_time" in device else 0,
            "cpu": cpu,
            "memory": memory,
        }

        print(
            f"{str(datetime.now())[:-3]}: sdwan sim for {device['name']}, heartbeat_info: {heartbeat_info}"
        )

        try:
            start = time.time()
            rsp = requests.post(
                "http://" + quokka_ip + ":5000/device/heartbeat", json=heartbeat_info
            )
            device["response_time"] = (time.time() - start) * 1000
            if rsp.status_code != 200:
                print(
                    f"{str(datetime.now())[:-3]}: --- response: {rsp.status_code}, {rsp.json()}"
                )
        except BaseException as e:
            print(f"Error in connecting to quokka server: {repr(e)}")

        time.sleep(1)  # space out the heartbeats a little bit

    print()
    time.sleep(INTERVAL_TIME)
