from quokka import app
from flask import request

from quokka.controller.device_info import get_device_info
from quokka.models.apis import get_devices, import_inventory, export_inventory


@app.route("/inventory", methods=["GET", "POST"])
def inventory():

    to_file = request.args.get("export_to")
    from_file = request.args.get("import_from")

    if request.method == "GET":
        return {"inventory": get_devices()}

    elif request.method == "POST":

        if to_file and from_file:
            return "Specify only 'export_to' or 'import_from' on POST inventory, not both."

        if to_file:
            return export_inventory(to_file, 'json')
        elif from_file:
            return import_inventory(from_file, 'json')

        else:
            return "Must specify either 'export_to' or 'import_from' on POST inventory"

    else:
        return "Invalid request method"


@app.route("/device", methods=["GET"])
def device():

    if request.method == "GET":

        device_name = request.args.get("device")
        requested_info = request.args.get("info")
        live = request.args.get("live")

        if not device_name or not requested_info:
            return "Must provide device and info", 400
        if not live:
            get_live_info = False
        else:
            if live.lower() not in {"true", "false"}:
                return "Value of 'live', if specified, must be 'true' or 'false'"
            else:
                get_live_info = bool(live)

        status, result_info = get_device_info(device_name, requested_info, get_live_info)
        if status == "success":
            return result_info, 200
        else:
            return result_info, 406
