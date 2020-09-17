from flask import Flask
from flask_cors import CORS

from quokka.controller.utils import log_console


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Get configuration from environment variables
import os
interval = os.environ.get("DEVICE_MONITOR_INTERVAL", default='60')
if interval.isnumeric():
    device_monitor_interval = max(10, int(interval))
else:
    device_monitor_interval = 60
interval = os.environ.get("COMPLIANCE_MONITOR_INTERVAL", default='300')
if interval.isnumeric():
    compliance_monitor_interval = max(10, int(interval))
else:
    compliance_monitor_interval = 300
interval = os.environ.get("HOST_MONITOR_INTERVAL", default='60')
if interval.isnumeric():
    host_monitor_interval = max(10, int(interval))
else:
    host_monitor_interval = 60
interval = os.environ.get("SERVICE_MONITOR_INTERVAL", default='60')
if interval.isnumeric():
    service_monitor_interval = max(10, int(interval))
else:
    service_monitor_interval = 60
interval = os.environ.get("DISCOVERY_INTERVAL", default='3600')
if interval.isnumeric():
    discovery_interval = max(10, int(interval))
else:
    discovery_interval = 3600


from flask_sqlalchemy import SQLAlchemy

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres:///quokka'
db = SQLAlchemy(app)

import quokka.views.ui_views
import quokka.views.device_views
import quokka.views.capture_views
import quokka.views.portscan_views
import quokka.models

db.create_all()

from quokka.models.apis import import_devices, import_compliance, import_services
from quokka.models.apis import get_all_devices, set_facts
from quokka.models.Host import Host

import_devices(filename="devices.yaml", filetype="yaml")
import_compliance(filename="compliance.yaml")
import_services(filename="services.yaml")

Host.query.delete()

# Reset time-series data tables
from quokka.models.DeviceStatus import DeviceStatusTS
from quokka.models.HostStatus import HostStatus
from quokka.models.ServiceStatus import ServiceStatus
DeviceStatusTS.query.delete()
HostStatus.query.delete()
ServiceStatus.query.delete()

# Reset event log and packet capture tables
from quokka.models.Event import Event
from quokka.models.Capture import Capture
Event.query.delete()
Capture.query.delete()

db.session.commit()

from quokka.controller.ThreadManager import ThreadManager
ThreadManager.start_device_threads(device_monitor_interval, compliance_monitor_interval)
ThreadManager.start_service_thread(service_monitor_interval)
ThreadManager.start_discovery_thread(discovery_interval)
ThreadManager.start_host_thread(host_monitor_interval)
ThreadManager.start_summaries_thread()

from quokka.controller.CaptureManager import CaptureManager
capture_manager = CaptureManager()
from quokka.controller.PortscanManager import PortscanManager
portscan_manager = PortscanManager()


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

