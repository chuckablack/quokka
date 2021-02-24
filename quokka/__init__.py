from flask import Flask
from flask_cors import CORS

from quokka.controller.utils import log_console


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Get configuration from environment variables
import os

interval = os.environ.get("DEVICE_MONITOR_INTERVAL", default="60")
if interval.isnumeric():
    device_monitor_interval = max(10, int(interval))
else:
    device_monitor_interval = 60
interval = os.environ.get("COMPLIANCE_MONITOR_INTERVAL", default="300")
if interval.isnumeric():
    compliance_monitor_interval = max(10, int(interval))
else:
    compliance_monitor_interval = 300
interval = os.environ.get("CONFIGURATION_MONITOR_INTERVAL", default="300")
if interval.isnumeric():
    configuration_monitor_interval = max(10, int(interval))
else:
    configuration_monitor_interval = 300
interval = os.environ.get("HOST_MONITOR_INTERVAL", default="60")
if interval.isnumeric():
    host_monitor_interval = max(10, int(interval))
else:
    host_monitor_interval = 60
interval = os.environ.get("SERVICE_MONITOR_INTERVAL", default="60")
if interval.isnumeric():
    service_monitor_interval = max(10, int(interval))
else:
    service_monitor_interval = 60
interval = os.environ.get("DISCOVERY_INTERVAL", default="3600")
if interval.isnumeric():
    discovery_interval = max(10, int(interval))
else:
    discovery_interval = 3600
interval = os.environ.get("WORKER_MONITOR_INTERVAL", default="60")
if interval.isnumeric():
    worker_monitor_interval = max(10, int(interval))
else:
    worker_monitor_interval = 60

from flask_sqlalchemy import SQLAlchemy

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///quokka"
db = SQLAlchemy(app)

import quokka.views.ui.misc_views
import quokka.views.ui.device_views
import quokka.views.ui.host_views
import quokka.views.ui.service_views
import quokka.views.device.device_views
import quokka.views.worker.capture_views
import quokka.views.worker.portscan_views
import quokka.views.worker.traceroute_views
import quokka.views.worker.worker_views

import quokka.models
db.create_all()

from quokka.models.apis.device_model_apis import import_devices, import_compliance
from quokka.models.apis.service_model_apis import import_services
from quokka.models.apis.worker_model_apis import import_workers

import_devices(filename="devices.yaml", filetype="yaml")
import_compliance(filename="compliance.yaml")
import_services(filename="services.yaml")
import_workers(filename="workers.yaml", filetype="yaml")

from quokka.controller.ThreadManager import ThreadManager

ThreadManager.start_device_threads(
    device_monitor_interval=device_monitor_interval,
    compliance_monitor_interval=compliance_monitor_interval,
    configuration_monitor_interval=configuration_monitor_interval,
)
ThreadManager.start_service_thread(service_monitor_interval)
ThreadManager.start_discovery_thread(discovery_interval)
ThreadManager.start_host_thread(host_monitor_interval)
ThreadManager.start_summaries_thread()
ThreadManager.start_worker_thread(worker_monitor_interval)
ThreadManager.start_db_maintenance_thread()

# from quokka.controller.CaptureManager import CaptureManager
# capture_manager = CaptureManager()
# from quokka.controller.PortscanManager import PortscanManager
# portscan_manager = PortscanManager()
# from quokka.controller.TracerouteManager import TracerouteManager
# traceroute_manager = TracerouteManager()


def shutdown():

    log_console("\n\n\n---> Entering shutdown sequence")

    ThreadManager.initiate_terminate_all_threads()

    ThreadManager.stop_discovery_thread()
    ThreadManager.stop_host_thread()
    ThreadManager.stop_service_thread()
    ThreadManager.stop_summaries_thread()
    ThreadManager.stop_worker_thread()
    ThreadManager.stop_device_threads()
    ThreadManager.stop_db_maintenance_thread()

    log_console("\n---> all threads shut down, terminating.")


import atexit

atexit.register(shutdown)
