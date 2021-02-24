from flask import request

from quokka import app
from quokka.controller.utils import log_console
from quokka.models.apis.device_model_apis import get_device
from quokka.models.apis.worker_data_apis import record_portscan


@app.route("/portscan/register", methods=["GET", "POST"])
def portscan_register():

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

    return {}, 200


@app.route("/portscan/store", methods=["POST"])
def portscan_store():

    portscan_info = request.get_json()
    if not portscan_info:
        return "Must provide portscan information in JSON body", 400
    if "source" not in portscan_info:
        return "Must provide 'source' in portscan information", 400
    if "serial" not in portscan_info:
        return "Must provide 'serial' in portscan information", 400
    if "host_ip" not in portscan_info:
        return "Must provide 'host_ip' in portscan information", 400
    if "host_name" not in portscan_info:
        return "Must provide 'host_name' in portscan information", 400
    if "timestamp" not in portscan_info:
        return "Must provide 'timestamp' in portscan information", 400
    if "scan_output" not in portscan_info:
        return "Must include 'scan_output' in portscan information", 400

    record_portscan(portscan_info)

    log_console(
        f"Received portscan store request from {portscan_info['source']} for host {portscan_info['host_name']}"
    )

    return {}, 200
