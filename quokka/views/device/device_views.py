from datetime import datetime

from quokka import app
from flask import request
from quokka.models.apis.device_model_apis import get_device, set_device, record_device_status

from quokka.controller.utils import log_console


@app.route("/device/register", methods=["GET", "POST"])
def device_register():

    registration_info = request.get_json()
    if not registration_info:
        return "Must provide registration information in JSON body", 400
    if "serial" not in registration_info:
        return "Must provide 'serial' in registration information", 400
    if "name" not in registration_info:
        return "Must provide 'name' in registration information", 400

    result, device = get_device(device_name=registration_info["name"])
    if result != "success":
        return "Unknown device name in registration information", 400
    if registration_info["serial"] != device["serial"]:
        return "Serial number in registration information does not match device serial", 400

    log_console(
        f"Received registration request from {registration_info['name']}, serial no: {registration_info['serial']}"
    )
    device["availability"] = True
    device["last_heard"] = str(datetime.now())[:-3]
    set_device(device)

    return {}, 200


@app.route("/device/heartbeat", methods=["POST"])
def device_heartbeat():

    heartbeat_info = request.get_json()
    if not heartbeat_info:
        return "Must provide heartbeat information in JSON body", 400
    if "serial" not in heartbeat_info:
        return "Must provide 'serial' in heartbeat information", 400
    if "name" not in heartbeat_info:
        return "Must provide 'name' in heartbeat information", 400

    result, device = get_device(device_name=heartbeat_info["name"])
    if result != "success":
        return "Unknown device name in heartbeat information", 400
    if heartbeat_info["serial"] != device["serial"]:
        return "Serial number in heartbeat information does not match device serial", 400

    device["availability"] = True
    device["last_heard"] = str(datetime.now())[:-3]

    if "vendor" in heartbeat_info:
        device["vendor"] = heartbeat_info["vendor"]
    if "model" in heartbeat_info:
        device["model"] = heartbeat_info["model"]
    if "os" in heartbeat_info:
        device["os"] = heartbeat_info["os"]
    if "version" in heartbeat_info:
        device["version"] = heartbeat_info["version"]

    if "response_time" in heartbeat_info:
        device["response_time"] = heartbeat_info["response_time"]
    if "cpu" in heartbeat_info:
        device["cpu"] = heartbeat_info["cpu"]
    if "memory" in heartbeat_info:
        device["memory"] = heartbeat_info["memory"]
    if "uptime" in heartbeat_info:
        device["uptime"] = heartbeat_info["uptime"]

    record_device_status(device)
    set_device(device)

    log_console(
        f"Received heartbeat from {heartbeat_info['name']}, info={heartbeat_info}"
    )

    return {}, 200
