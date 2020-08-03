from quokka import app
from flask import request

from quokka.controller.device.device_info import get_device_info
from quokka.models.apis import (
    get_device,
    get_all_devices,
    import_devices,
    export_devices,
    get_device_ts_data,
    get_host,
    get_all_hosts,
    get_host_ts_data,
    get_service,
    get_all_services,
    get_service_ts_data,
    get_all_events,
    get_service_summary_data,
    get_host_summary_data,
)
import quokka.models.reset
from quokka.controller.ThreadManager import ThreadManager


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

    else:
        return "Invalid request method"


@app.route("/ui/device", methods=["GET"])
def device_info():

    if request.method == "GET":

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


@app.route("/ui/hosts", methods=["GET"])
def hosts():

    if request.method == "GET":
        return {"hosts": get_all_hosts()}

    else:
        return "Invalid request method"


@app.route("/ui/events", methods=["GET"])
def events():

    num_events = request.args.get("num_events", default=1000)

    if request.method == "GET":
        return {"events": get_all_events(num_events)}

    else:
        return "Invalid request method"


@app.route("/ui/services", methods=["GET"])
def services():

    if request.method == "GET":
        return {"services": get_all_services()}

    else:
        return "Invalid request method"


@app.route("/ui/host/ts", methods=["GET"])
def host_ts():

    host_id = request.args.get("hostid")
    num_datapoints = request.args.get("datapoints")

    if not host_id or not num_datapoints:
        return "Must provide hostid and datapoints", 400

    return {
        "host_data": get_host_ts_data(host_id, num_datapoints),
        "host_summary": get_host_summary_data(host_id, num_datapoints),
        "host": get_host(host_id),
    }


@app.route("/ui/service/ts", methods=["GET"])
def service_ts():

    service_id = request.args.get("serviceid")
    num_datapoints = request.args.get("datapoints")

    if not service_id or not num_datapoints:
        return "Must provide serviceid and datapoints", 400

    return {
        "service_data": get_service_ts_data(service_id, num_datapoints),
        "service_summary": get_service_summary_data(service_id, num_datapoints),
        "service": get_service(service_id),
    }


@app.route("/ui/device/ts", methods=["GET"])
def device_ts():

    device_name = request.args.get("device")
    num_datapoints = request.args.get("datapoints")

    if not device_name or not num_datapoints:
        return "Must provide deviceid and datapoints", 400

    result, info = get_device(device_name=device_name)
    if result != "success":
        return "Could not find device in DB", 404

    device = info
    return {
        "device_data": get_device_ts_data(device_name, num_datapoints),
        "device": device,
    }


@app.route("/ui/reset/devices", methods=["POST"])
def reset_devices():
    ThreadManager.stop_device_threads()
    quokka.models.reset.reset_devices()
    ThreadManager.start_device_threads()
    return "Devices reset"


@app.route("/ui/reset/hosts", methods=["POST"])
def reset_hosts():
    ThreadManager.stop_host_thread()
    quokka.models.reset.reset_hosts()
    ThreadManager.start_host_thread()
    return "Hosts reset"


@app.route("/ui/reset/services", methods=["POST"])
def reset_services():
    ThreadManager.stop_service_thread()
    quokka.models.reset.reset_services()
    ThreadManager.start_service_thread()
    return "Services reset"


@app.route("/ui/reset/events", methods=["POST"])
def reset_events():
    quokka.models.reset.reset_events()
    return "Services reset"