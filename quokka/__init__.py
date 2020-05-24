from flask import Flask
from flask_cors import CORS

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
from quokka.controller import get_device_info

import_inventory(filename="inventory.json", filetype="json")

# Pre-populate the DB with device facts
inventory = get_devices()
for device in inventory:
    result, facts = get_device_info(device_name=device["name"], requested_info="facts")
    if result == "success":
        set_facts(device, facts)

