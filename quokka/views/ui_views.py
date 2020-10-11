from quokka import app
from flask import request
from datetime import datetime

from quokka.controller.device.device_info import get_device_info
from quokka.models.apis import (
    get_device,
    get_all_devices,
    import_devices,
    export_devices,
    get_device_status_data,
    get_host,
    get_all_hosts,
    get_host_status_data,
    get_service,
    get_all_services,
    get_service_status_data,
    get_all_events,
    get_service_summary_data,
    get_host_summary_data,
    # get_host_capture,
    # get_protocol_capture,
    get_capture,
    get_port_scan_extended,
    get_device_config_diff,
)
import quokka.models.reset
from quokka.controller.ThreadManager import ThreadManager
from quokka.controller.CaptureManager import CaptureManager
from quokka.controller.PortscanManager import PortscanManager
from quokka.controller.host.portscan import get_port_scan_tcp_connection


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


@app.route("/ui/host/status", methods=["GET"])
def host_status():

    host_id = request.args.get("hostid")
    num_datapoints = request.args.get("datapoints")

    if not host_id or not num_datapoints:
        return "Must provide hostid and datapoints", 400

    return {
        "host_data": get_host_status_data(host_id, num_datapoints),
        "host_summary": get_host_summary_data(host_id, num_datapoints),
        "host": get_host(host_id),
    }


@app.route("/ui/service/status", methods=["GET"])
def service_status():

    service_id = request.args.get("serviceid")
    num_datapoints = request.args.get("datapoints")

    if not service_id or not num_datapoints:
        return "Must provide serviceid and datapoints", 400

    return {
        "service_data": get_service_status_data(service_id, num_datapoints),
        "service_summary": get_service_summary_data(service_id, num_datapoints),
        "service": get_service(service_id),
    }


@app.route("/ui/device/status", methods=["GET"])
def device_status():

    device_name = request.args.get("device")
    num_datapoints = request.args.get("datapoints")

    if not device_name or not num_datapoints:
        return "Must provide deviceid and datapoints", 400

    result, info = get_device(device_name=device_name)
    if result != "success":
        return "Could not find device in DB", 404

    device = info
    return {
        "device_data": get_device_status_data(device_name, num_datapoints),
        "device": device,
    }


@app.route("/ui/reset/devices", methods=["POST"])
def reset_devices():
    ThreadManager.stop_device_threads()
    quokka.models.reset.reset_devices()
    ThreadManager.start_device_threads()
    return "Devices reset and monitoring threads restarted"


@app.route("/ui/reset/hosts", methods=["POST"])
def reset_hosts():
    ThreadManager.stop_host_thread()
    quokka.models.reset.reset_hosts()
    ThreadManager.start_host_thread()
    return "Hosts reset and host thread restarted"


@app.route("/ui/reset/services", methods=["POST"])
def reset_services():
    ThreadManager.stop_service_thread()
    quokka.models.reset.reset_services()
    ThreadManager.start_service_thread()
    return "Services reset and service thread restarted"


@app.route("/ui/reset/events", methods=["POST"])
def reset_events():
    quokka.models.reset.reset_events()
    return "Events table reset"


@app.route("/ui/reset/capture", methods=["POST"])
def reset_capture():
    quokka.models.reset.reset_capture()
    return "Capture table reset"


@app.route("/ui/capture", methods=["GET", "POST"])
def capture():

    ip = request.args.get("ip")
    protocol = request.args.get("protocol")
    port = request.args.get("port")
    num_packets = request.args.get("num_packets")

    if not num_packets:
        num_packets = 10

    if request.method == "GET":
        return {"packets": get_capture(ip, protocol, port, num_packets)}

    elif request.method == "POST":
        CaptureManager.initiate_capture(ip, protocol, port, num_packets)
        return "Capture initiated"

    else:
        return "Invalid request method"


@app.route("/ui/scan", methods=["GET"])
def scan():

    host_id = request.args.get("hostid")

    if not host_id:
        return "Must provide hostid", 400

    host = get_host(host_id)
    if not host:
        return f"Unknown host id={host_id}", 404

    result, scan_results = get_port_scan_tcp_connection(host["ip_address"])
    return {
        "result": result,
        "open_ports": str(scan_results),
        "host": host,
    }


@app.route("/ui/scan/extended", methods=["GET", "POST"])
def scan_extended():

    host_id = request.args.get("hostid")

    if not host_id:
        return "Must provide hostid", 400

    host = get_host(host_id)
    if not host:
        return f"Unknown host id={host_id}", 404

    if request.method == "GET":
        token = request.args.get("token")
        if not token:
            return "Must provide token on GET request", 400

        result, scan_results = get_port_scan_extended(host["ip_address"], host["name"], token)
        return {
            "result": result,
            "scan_output": str(scan_results),
            "host": host,
        }

    elif request.method == "POST":
        token = str(datetime.now())[:-3]
        PortscanManager.initiate_portscan(host["ip_address"], host["name"], token)
        return {"result": f"Portscan initiated for host: {host['name']}, ip: {host['ip_address']}",
                "token": token}

    else:
        return "Invalid request method"
