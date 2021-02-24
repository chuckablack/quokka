from datetime import datetime

from quokka import app
from flask import request
from quokka.models.apis.worker_data_apis import get_commands
from quokka.models.apis.worker_model_apis import get_worker, set_worker, record_worker_status

from quokka.controller.utils import log_console


@app.route("/worker/register", methods=["GET", "POST"])
def worker_register():

    registration_info = request.get_json()
    if not registration_info:
        return "Must provide registration information in JSON body", 400
    if "serial" not in registration_info:
        return "Must provide 'serial' in registration information", 400
    if "name" not in registration_info:
        return "Must provide 'name' in registration information", 400

    worker = get_worker(host=registration_info["name"], worker_type=registration_info["worker_type"])
    if worker is None:
        return "Unknown worker name in registration information", 400
    if registration_info["serial"] != worker["serial"]:
        return "Serial number in registration information does not match worker serial", 400

    log_console(
        f"Received registration request from {registration_info['name']}, serial no: {registration_info['serial']}"
    )
    worker["availability"] = True
    worker["last_heard"] = str(datetime.now())[:-3]
    set_worker(worker)

    return {}, 200


@app.route("/worker/heartbeat", methods=["POST"])
def worker_heartbeat():

    heartbeat_info = request.get_json()
    if not heartbeat_info:
        return "Must provide heartbeat information in JSON body", 400
    if "serial" not in heartbeat_info:
        return "Must provide 'serial' in heartbeat information", 400

    worker = get_worker(serial=heartbeat_info["serial"], worker_type=heartbeat_info["worker_type"])
    if worker is None:
        return "Unknown worker serial number in heartbeat information", 400

    worker["availability"] = True
    worker["last_heard"] = str(datetime.now())[:-3]

    if "response_time" in heartbeat_info:
        worker["response_time"] = heartbeat_info["response_time"]
    if "cpu" in heartbeat_info:
        worker["cpu"] = heartbeat_info["cpu"]
    if "memory" in heartbeat_info:
        worker["memory"] = heartbeat_info["memory"]
    if "uptime" in heartbeat_info:
        worker["uptime"] = heartbeat_info["uptime"]

    record_worker_status(worker)
    set_worker(worker)
    log_console(f"Received heartbeat from {heartbeat_info['name']}, info={heartbeat_info}")

    result, commands = get_commands(
        serial=heartbeat_info["serial"],
        worker_type=heartbeat_info["worker_type"],
        set_delivered=True,
    )
    if result != "success":
        log_console(f"Failed to retrieve commands for {heartbeat_info['serial']}")
    else:
        log_console(f"Delivered commands to {heartbeat_info['serial']}, commands={commands}")

    return {"commands": commands}, 200
