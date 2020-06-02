from flask import Flask
from flask_cors import CORS
import threading


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)

import quokka.views
import quokka.models

db.create_all()

from quokka.models.apis import import_devices, get_devices, set_facts
from quokka.controller.device_info import get_device_info

import_devices(filename="devices.yaml", filetype="yaml")

# Pre-populate the DB with device facts
devices = get_devices()
for device in devices:
    result, facts = get_device_info(device_name=device["name"], requested_info="facts")
    if result == "success":
        set_facts(device, facts)

from quokka.controller.DiscoverTask import DiscoverTask
discover_task = DiscoverTask()
discover_thread = threading.Thread(target=discover_task.discover, args=(3600,))
discover_thread.start()

from quokka.controller.MonitorTask import MonitorTask
monitor_task = MonitorTask()
monitor_thread = threading.Thread(target=monitor_task.monitor, args=(60,))
monitor_thread.start()


def shutdown():
    print("---> Entering shutdown sequence")
    discover_task.set_terminate()
    monitor_task.set_terminate()

    print("--- ---> Shutting down threads")
    discover_thread.join()
    monitor_thread.join()

    print("--- ---> all threads shut down, terminating.")


import atexit
atexit.register(shutdown)

