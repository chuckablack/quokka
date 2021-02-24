from datetime import datetime

from flask import request

import quokka.models.apis.reset_apis
from quokka import app
from quokka.controller.CaptureManager import CaptureManager
from quokka.controller.PortscanManager import PortscanManager
from quokka.controller.ThreadManager import ThreadManager
from quokka.controller.TracerouteManager import TracerouteManager
from quokka.controller.host.portscan import get_port_scan_tcp_connection
from quokka.models.apis.worker_data_apis import (
    get_capture,
    get_port_scan_extended,
    get_traceroute,
)
from quokka.models.apis.worker_model_apis import (
    get_worker,
    get_all_workers,
    get_worker_status_data,
)
from quokka.models.apis.host_model_apis import get_host
from quokka.models.apis.event_model_apis import get_all_events


@app.route("/ui/events", methods=["GET"])
def events():

    num_events = request.args.get("num_events", default=1000)
    return {"events": get_all_events(num_events)}


@app.route("/ui/reset/devices", methods=["POST"])
def reset_devices():
    ThreadManager.stop_device_threads()
    quokka.models.apis.reset_apis.reset_devices()
    ThreadManager.start_device_threads()
    return "Devices reset and monitoring threads restarted"


@app.route("/ui/reset/hosts", methods=["POST"])
def reset_hosts():
    ThreadManager.stop_discovery_thread()
    ThreadManager.stop_host_thread()
    quokka.models.apis.reset_apis.reset_hosts()
    ThreadManager.start_discovery_thread()
    ThreadManager.start_host_thread()
    return "Hosts reset and host thread restarted"


@app.route("/ui/reset/services", methods=["POST"])
def reset_services():
    ThreadManager.stop_service_thread()
    quokka.models.apis.reset_apis.reset_services()
    ThreadManager.start_service_thread()
    return "Services reset and service thread restarted"


@app.route("/ui/reset/events", methods=["POST"])
def reset_events():
    quokka.models.apis.reset_apis.reset_events()
    return "Events table reset"


@app.route("/ui/reset/capture", methods=["POST"])
def reset_capture():
    quokka.models.apis.reset_apis.reset_capture()
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


@app.route("/ui/scan", methods=["GET"])
def scan():

    host_id = request.args.get("hostid")

    if not host_id:
        return "Must provide hostid", 400

    host = get_host(host_id)
    if not host:
        return f"Unknown host id={host_id}", 400

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
        return f"Unknown host id={host_id}", 400

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


@app.route("/ui/traceroute", methods=["GET", "POST"])
def traceroute():

    target = request.args.get("target")

    if not target:
        return "Must provide target", 400

    if request.method == "GET":
        token = request.args.get("token")
        if not token:
            return "Must provide token on GET request", 400

        result, traceroute_image = get_traceroute(target, token)
        return {
            "result": result,
            "traceroute_output": str(traceroute_image),
            "target": target,
        }

    elif request.method == "POST":
        token = str(datetime.now())
        TracerouteManager.initiate_traceroute(target, token)
        return {"result": f"Traceroute initiated for target: {target}",
                "token": token}


@app.route("/ui/workers", methods=["GET"])
def workers():

    return {"workers": get_all_workers()}


@app.route("/ui/worker/status", methods=["GET"])
def worker_status():

    worker_id = request.args.get("workerid")
    num_datapoints = request.args.get("datapoints")

    if not worker_id or not num_datapoints:
        return "Must provide workerid and datapoints", 400

    return {
        "worker_data": get_worker_status_data(worker_id, num_datapoints),
        "worker": get_worker(worker_id),
    }
