import yaml
import requests
import random
import time
from datetime import datetime

NUM_CONSECUTIVE_FAILURES_REQUIRED = 3
INTERVAL_TIME = 60

filename = "devices.yaml"
with open("quokka/data/" + filename, "r") as import_file:
    devices = yaml.safe_load(import_file.read())

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

        response_time = random.randint(2000, 7500)
        cpu = random.randint(20, 50)
        memory = random.randint(30, 50)

        heartbeat_info = {
            "name": device["name"],
            "serial": device["serial"],
            "response_time": response_time,
            "cpu": cpu,
            "memory": memory,
        }

        print(
            f"{str(datetime.now())[:-3]}: sdwan sim for {device['name']}, heartbeat_info: {heartbeat_info}"
        )

        try:
            rsp = requests.post(
                "http://192.168.254.114:5000/device/heartbeat", json=heartbeat_info
            )
            if rsp.status_code != 200:
                print(
                    f"{str(datetime.now())[:-3]}: --- response: {rsp.status_code}, {rsp.json()}"
                )
        except BaseException as e:
            print(f"Error in connecting to quokka server: {repr(e)}")

    print()
    time.sleep(INTERVAL_TIME)
