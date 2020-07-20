import yaml
import requests
import random
import time

filename = "devices.yaml"
with open("../../quokka/data/" + filename, "r") as import_file:
    devices = yaml.load(import_file.read())

while True:

    for device in devices:

        if device["transport"] != "HTTP-REST":
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

        rsp = requests.post("http://192.168.254.114:5000/device/heartbeat", json=heartbeat_info)

    time.sleep(60)
