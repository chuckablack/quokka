from quokka import app
from flask import request

from quokka.controller import get_device_info
from quokka.models import get_devices, get_status, get_versions, import_inventory, export_inventory


@app.route("/inventory", methods=["GET", "POST"])
def inventory():

    to_file = request.args.get("export_to")
    from_file = request.args.get("import_from")

    if request.method == "GET":
        return "GET inventory"

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

        if not device_name or not requested_info:
            return "Must provide device and info", 400

        status, result_info = get_device_info(device_name, requested_info)
        if status == "success":
            return result_info, 200
        else:
            return result_info, 406


