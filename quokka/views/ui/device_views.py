from flask import request

from quokka import app
from quokka.controller.device.device_info import get_device_info
from quokka.models.apis.device_model_apis import (
    get_device,
    get_all_devices,
    import_devices,
    export_devices,
    get_device_status_data,
    get_device_config_diff,
)


@app.route("/ui/devices", methods=["GET", "POST"])
def devices():

    to_file = request.args.get("export_to")
    from_file = request.args.get("import_from")

    if request.method == "GET":
        return {"devices": get_all_devices()}

    elif request.method == "POST":

        if to_file and from_file:
            return (
                "Specify only 'export_to' or 'import_from' on POST devices, not both."
            )

        if to_file:
            return export_devices(to_file, "json")
        elif from_file:
            return import_devices(from_file, "json")

        else:
            return "Must specify either 'export_to' or 'import_from' on POST devices"


@app.route("/ui/device", methods=["GET"])
def device_info():

    device_name = request.args.get("device")
    requested_info = request.args.get("info")
    live = request.args.get("live")

    if not device_name or not requested_info:
        return "Must provide device and info", 400

    result, info = get_device(device_name=device_name)
    if result == "failed":
        return info, 406
    device = info

    if not live:
        get_live_info = False
    else:
        if live.lower() not in {"true", "false"}:
            return "Value of 'live', if specified, must be 'true' or 'false'"
        else:
            get_live_info = bool(live)

    status, result_info = get_device_info(device, requested_info, get_live_info)
    if status == "success":
        return result_info, 200
    else:
        return result_info, 406


@app.route("/ui/device/config", methods=["GET"])
def device_config_diff():

    device_name = request.args.get("device")
    num_configs = request.args.get("configs", 10)

    if not device_name:
        return "Must provide device name", 400

    result, info = get_device(device_name=device_name)
    if result == "failed":
        return info, 406
    device = info

    status, result_info = get_device_config_diff(device, num_configs)
    if status == "success":
        return result_info, 200
    else:
        return result_info, 406


@app.route("/ui/device/status", methods=["GET"])
def device_status():

    device_name = request.args.get("device")
    num_datapoints = request.args.get("datapoints")

    if not device_name or not num_datapoints:
        return "Must provide deviceid and datapoints", 400

    result, info = get_device(device_name=device_name)
    if result != "success":
        return "Could not find device in DB", 400

    device = info
    return {
        "device_data": get_device_status_data(device_name, num_datapoints),
        "device": device,
    }


