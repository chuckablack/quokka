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

from quokka.models.apis import import_devices, import_compliance, import_services
from quokka.models.apis import get_all_devices, set_facts
from quokka.controller.device_info import get_device_info

import_devices(filename="devices.yaml", filetype="yaml")
import_compliance(filename="compliance.yaml")
import_services(filename="services.yaml")

# Reset time-series data
from quokka.models.DeviceStatusTS import DeviceStatusTS
from quokka.models.HostStatusTS import HostStatusTS
from quokka.models.ServiceStatusTS import ServiceStatusTS
DeviceStatusTS.query.delete()
HostStatusTS.query.delete()
ServiceStatusTS.query.delete()

# Pre-populate the DB with device facts
devices = get_all_devices()
for device in devices:
    result, facts = get_device_info(device_name=device["name"], requested_info="facts")
    if result == "success":
        set_facts(device, facts)

from quokka.controller.DiscoverTask import DiscoverTask
discover_task = DiscoverTask()
discover_thread = threading.Thread(target=discover_task.discover, args=(3600,))
discover_thread.start()

from quokka.controller.HostMonitorTask import HostMonitorTask
host_monitor_task = HostMonitorTask()
host_monitor_thread = threading.Thread(target=host_monitor_task.monitor, args=(60,))
host_monitor_thread.start()

from quokka.controller.DeviceMonitorTask import DeviceMonitorTask
device_monitor_task = DeviceMonitorTask()
device_monitor_thread = threading.Thread(target=device_monitor_task.monitor, args=(60,))
device_monitor_thread.start()

from quokka.controller.ComplianceMonitorTask import ComplianceMonitorTask
compliance_monitor_task = ComplianceMonitorTask()
compliance_monitor_thread = threading.Thread(target=compliance_monitor_task.monitor, args=(60,))
compliance_monitor_thread.start()

from quokka.controller.ServiceMonitorTask import ServiceMonitorTask
service_monitor_task = ServiceMonitorTask()
service_monitor_thread = threading.Thread(target=service_monitor_task.monitor, args=(60,))
service_monitor_thread.start()


def shutdown():
    print("\n\n\n---> Entering shutdown sequence")
    discover_task.set_terminate()
    host_monitor_task.set_terminate()
    device_monitor_task.set_terminate()
    compliance_monitor_task.set_terminate()
    service_monitor_task.set_terminate()

    print("--- ---> Shutting down threads")
    discover_thread.join()
    host_monitor_thread.join()
    device_monitor_thread.join()
    compliance_monitor_thread.join()
    service_monitor_thread.join()

    print("--- ---> all threads shut down, terminating.")


import atexit
atexit.register(shutdown)

