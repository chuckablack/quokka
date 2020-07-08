from flask import Flask
from flask_cors import CORS

from quokka.controller.utils import log_console


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask_sqlalchemy import SQLAlchemy

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres:///quokka'
db = SQLAlchemy(app)

import quokka.views
import quokka.models

db.create_all()

from quokka.models.apis import import_devices, import_compliance, import_services
from quokka.models.apis import get_all_devices, set_facts
from quokka.models.Host import Host
from quokka.controller.device.device_info import get_device_info

import_devices(filename="devices.yaml", filetype="yaml")
import_compliance(filename="compliance.yaml")
import_services(filename="services.yaml")

Host.query.delete()
db.session.commit()

# Reset time-series data
from quokka.models.DeviceStatusTS import DeviceStatusTS
from quokka.models.HostStatusTS import HostStatusTS
from quokka.models.ServiceStatusTS import ServiceStatusTS
from quokka.models.Event import Event
DeviceStatusTS.query.delete()
HostStatusTS.query.delete()
ServiceStatusTS.query.delete()
Event.query.delete()

# Pre-populate the DB with device facts
# devices = get_all_devices()
# for device in devices:
#     result, facts = get_device_info(device_name=device["name"], requested_info="facts")
#     if result == "success":
#         set_facts(device, facts)

from quokka.controller.ThreadManager import ThreadManager
ThreadManager.start_device_threads()
ThreadManager.start_service_thread()
ThreadManager.start_discovery_thread()
ThreadManager.start_host_thread()
ThreadManager.start_summaries_thread()


def shutdown():

    log_console("\n\n\n---> Entering shutdown sequence")

    ThreadManager.initiate_terminate_all_threads()
    
    ThreadManager.stop_discovery_thread()
    ThreadManager.stop_host_thread()
    ThreadManager.stop_service_thread()
    ThreadManager.stop_summaries_thread()
    ThreadManager.stop_device_threads()

    log_console("\n---> all threads shut down, terminating.")


import atexit
atexit.register(shutdown)

