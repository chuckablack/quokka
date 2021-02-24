from flask import request

from quokka import app
from quokka.controller.utils import log_console
from quokka.models.apis.device_model_apis import get_device
from quokka.models.apis.worker_data_apis import record_capture


@app.route("/capture/register", methods=["GET", "POST"])
def capture_register():

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


@app.route("/capture/store", methods=["POST"])
def capture_store():

    capture_info = request.get_json()
    if not capture_info:
        return "Must provide capture information in JSON body", 400
    if "serial" not in capture_info:
        return "Must provide 'serial' in capture information", 400
    if "source" not in capture_info:
        return "Must provide 'source' in capture information", 400
    if "timestamp" not in capture_info:
        return "Must provide 'timestamp' in capture information", 400
    if "packets" not in capture_info:
        return "Must include 'packets' in capture information", 400

    record_capture(capture_info["timestamp"], capture_info["source"], capture_info["packets"])

    log_console(
        f"Received capture store request from {capture_info['source']}, pkts={len(capture_info['packets'])}"
    )

    return {}, 200
