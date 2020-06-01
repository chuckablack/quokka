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

from quokka.models.apis import import_inventory, get_devices, set_facts
from quokka.controller.device_info import get_device_info

import_inventory(filename="inventory.yaml", filetype="yaml")

# Pre-populate the DB with device facts
inventory = get_devices()
for device in inventory:
    result, facts = get_device_info(device_name=device["name"], requested_info="facts")
    if result == "success":
        set_facts(device, facts)

from quokka.controller.discovery import discover
discovery_thread = threading.Thread(target=discover, args=(3600,))
discovery_thread.start()

from quokka.controller.monitor import monitor
monitor_thread = threading.Thread(target=monitor, args=(300,))
monitor_thread.start()

