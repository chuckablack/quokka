import json
import yaml
import time
from datetime import datetime
from sqlalchemy import desc, or_, func
from pprint import pformat

from quokka import db

from quokka.models.Device import Device
from quokka.models.DeviceFacts import DeviceFacts
from quokka.models.Compliance import Compliance
from quokka.models.Host import Host
from quokka.models.Service import Service
from quokka.models.Worker import Worker
from quokka.models.Command import Command

from quokka.models.Event import Event
from quokka.models.Capture import Capture
from quokka.models.Portscan import Portscan
from quokka.models.Traceroute import Traceroute

from quokka.models.DeviceStatus import DeviceStatus
from quokka.models.HostStatus import HostStatus
from quokka.models.ServiceStatus import ServiceStatus
from quokka.models.WorkerStatus import WorkerStatus
from quokka.models.HostStatusSummary import HostStatusSummary
from quokka.models.ServiceStatusSummary import ServiceStatusSummary

from quokka.models.DeviceConfig import DeviceConfig

from quokka.models.util import get_model_as_dict
from quokka.controller.utils import log_console


def get_device(device_id=None, device_name=None):

    if device_id and device_name:
        return "failed", "Must provide either device_id or device_name, but not both"

    if device_id:
        search = {"id": device_id}
    elif device_name:
        search = {"name": device_name}
    else:
        return "failed", "Must provide either device_id or device_name"

    device_obj = db.session.query(Device).filter_by(**search).one_or_none()
    if not device_obj:
        return "failed", "Could not find device in DB"

    return "success", get_model_as_dict(device_obj)


def get_all_devices():

    device_objs = db.session.query(Device).all()

    devices = list()
    for device_obj in device_objs:
        devices.append(get_model_as_dict(device_obj))

    return devices


def get_all_device_ids():

    device_ids = db.session.query(Device.id).all()
    return [
        device_id for device_id, in device_ids
    ]  # The query returns IDs in tuples, this strips the tuple-ness


def get_facts(device_name):

    facts_obj = (
        db.session.query(DeviceFacts)
        .filter_by(**{"device_name": device_name})
        .one_or_none()
    )
    if not facts_obj:
        return "failed", "Could not find device facts in DB"

    return "success", get_model_as_dict(facts_obj)


def set_devices(devices):

    # validate devices: make sure no duplicate ids or names
    ids = set()
    names = set()

    for device in devices:

        if device["id"] in ids:
            log_event(
                str(datetime.now())[:-3],
                "importing devices",
                "devices.yaml",
                "ERROR",
                f"Duplicate device id: {device['id']}",
            )
            continue
        if device["name"] in names:
            log_event(
                str(datetime.now())[:-3],
                "importing devices",
                "devices.yaml",
                "ERROR",
                f"Duplicate device name: {device['name']}",
            )
            continue

        ids.add(device["id"])
        names.add(device["name"])

        device_obj = Device(**device)
        db.session.add(device_obj)

    db.session.commit()


def set_device(device):

    search = {"name": device["name"]}
    device_obj = db.session.query(Device).filter_by(**search).one_or_none()
    if not device_obj:
        device_obj = Device(**device)
        db.session.add(device_obj)
    else:
        if "ip_address" in device and device["ip_address"]:
            device_obj.ip_address = device["ip_address"]
        if "serial" in device and device["serial"]:
            device_obj.serial_no = device["serial"]
        if "mac_address" in device and device["mac_address"]:
            device_obj.mac_address = device["mac_address"]
        if "vendor" in device and device["vendor"]:
            device_obj.vendor = device["vendor"]
        if "os" in device and device["os"]:
            device_obj.os = device["os"]
        if "version" in device and device["version"]:
            device_obj.version = device["version"]
        if "model" in device and device["model"]:
            device_obj.model = device["model"]
        if "fqdn" in device and device["fqdn"]:
            device_obj.fqdn = device["fqdn"]
        if "uptime" in device and device["uptime"]:
            device_obj.uptime = device["uptime"]
        if "availability" in device and device["availability"] is not None:
            device_obj.availability = device["availability"]
        if "response_time" in device and device["response_time"]:
            device_obj.response_time = device["response_time"]
        if "last_heard" in device and device["last_heard"]:
            device_obj.last_heard = device["last_heard"]
        if "cpu" in device and device["cpu"]:
            device_obj.cpu = device["cpu"]
        if "memory" in device and device["memory"]:
            device_obj.memory = device["memory"]
        if "os_compliance" in device and device["os_compliance"] is not None:
            device_obj.os_compliance = device["os_compliance"]
        if "config_compliance" in device and device["config_compliance"] is not None:
            device_obj.config_compliance = device["config_compliance"]
        if "last_compliance_check" in device and device["last_compliance_check"]:
            device_obj.last_compliance_check = device["last_compliance_check"]

    db.session.commit()


def set_facts(device, facts):

    device_facts = dict()
    device_facts["fqdn"] = facts["facts"]["fqdn"]
    device_facts["uptime"] = facts["facts"]["uptime"]
    device_facts["vendor"] = facts["facts"]["vendor"]
    device_facts["os_version"] = facts["facts"]["os_version"]
    device_facts["serial_number"] = facts["facts"]["serial_number"]
    device_facts["model"] = facts["facts"]["model"]
    device_facts["hostname"] = facts["facts"]["hostname"]

    device_facts["device_name"] = device["name"]
    device_facts_obj = DeviceFacts(**device_facts)

    facts_obj = (
        db.session.query(DeviceFacts)
        .filter_by(**{"device_name": device_facts["device_name"]})
        .one_or_none()
    )
    if not facts_obj:
        db.session.add(device_facts_obj)

    else:
        facts_obj.fqdn = device_facts["fqdn"]
        facts_obj.uptime = device_facts["uptime"]
        facts_obj.vendor = device_facts["vendor"]
        facts_obj.os_version = device_facts["os_version"]
        facts_obj.serial_number = device_facts["serial_number"]
        facts_obj.model = device_facts["model"]
        facts_obj.hostname = device_facts["hostname"]
        facts_obj.device_name = device_facts["device_name"]

    db.session.commit()


def import_devices(filename=None, filetype=None):

    if not filename or not filetype:
        return None

    db.session.query(Device).delete()
    with open("quokka/data/" + filename, "r") as import_file:

        if filetype.lower() == "json":
            devices = json.loads(import_file.read())
        elif filetype.lower() == "yaml":
            devices = yaml.safe_load(import_file.read())
        else:
            return None

    set_devices(devices)
    return {"devices": devices}


def export_devices(filename=None, filetype=None):

    if not filename or not filetype:
        return None

    devices = get_all_devices()

    with open(filename, "w") as output_file:

        if filetype.lower() == "json":
            output_file.write(json.dumps(devices))
        elif filetype.lower() == "yaml":
            output_file.write(yaml.dump(devices))
        else:
            return None


def import_compliance(filename=None):

    db.session.query(Compliance).delete()

    try:
        with open("quokka/data/" + filename, "r") as import_file:
            standards = yaml.safe_load(import_file.read())
    except FileNotFoundError as e:
        log_console(f"Could not import compliance file: {repr(e)}")

    for standard in standards:
        standard_obj = Compliance(**standard)
        db.session.add(standard_obj)

    db.session.commit()
    return


def import_services(filename=None):

    db.session.query(Service).delete()

    try:
        with open("quokka/data/" + filename, "r") as import_file:
            services = yaml.safe_load(import_file.read())
    except FileNotFoundError as e:
        log_console(f"Could not import services file: {repr(e)}")

    # validate services: make sure no duplicate ids
    ids = set()

    for service in services:

        if service["id"] in ids:
            log_event(
                str(datetime.now())[:-3],
                "importing services",
                filename,
                "ERROR",
                f"Duplicate service id: {service['id']}",
            )
            continue

        ids.add(service["id"])

        service_obj = Service(**service)
        db.session.add(service_obj)

    db.session.commit()
    return


def get_host(host_id):

    search = {"id": host_id}
    host_obj = db.session.query(Host).filter_by(**search).one_or_none()
    if not host_obj:
        return None
    else:
        return get_model_as_dict(host_obj)


def get_all_hosts():

    host_objs = db.session.query(Host).all()

    hosts = list()
    for host_obj in host_objs:
        host = get_model_as_dict(host_obj)
        hosts.append(host)

    return hosts


def set_host(host):

    search = {"name": host["name"], "ip_address": host["ip_address"]}
    host_obj = db.session.query(Host).filter_by(**search).one_or_none()
    if not host_obj:
        host_obj = Host(**host)
        db.session.add(host_obj)
    else:
        if "ip_address" in host:
            host_obj.ip_address = host["ip_address"]
        if "mac_address" in host:
            host_obj.mac_address = host["mac_address"]
        if "availability" in host:
            host_obj.availability = host["availability"]
        if "response_time" in host:
            host_obj.response_time = host["response_time"]
        if "last_heard" in host:
            host_obj.last_heard = host["last_heard"]

    db.session.commit()


def get_service(service_id):

    search = {"id": service_id}
    service_obj = db.session.query(Service).filter_by(**search).one_or_none()
    if not service_obj:
        return None
    else:
        return get_model_as_dict(service_obj)


def get_all_services():

    service_objs = db.session.query(Service).all()

    services = list()
    for service_obj in service_objs:
        service = get_model_as_dict(service_obj)
        services.append(service)

    return services


def set_service(service):

    search = {"name": service["name"]}
    service_obj = db.session.query(Service).filter_by(**search).one_or_none()
    if not service_obj:
        service_obj = Service(**service)
        db.session.add(service_obj)
    else:
        if "type" in service:
            service_obj.availability = service["type"]
        if "target" in service:
            service_obj.availability = service["target"]
        if "username" in service:
            service_obj.availability = service["username"]
        if "password" in service:
            service_obj.availability = service["password"]
        if "availability" in service:
            service_obj.availability = service["availability"]
        if "response_time" in service:
            service_obj.response_time = service["response_time"]
        if "last_heard" in service:
            service_obj.last_heard = service["last_heard"]

    db.session.commit()


def record_device_status(device):

    device_status = dict()
    device_status["device_id"] = device["id"]
    device_status["timestamp"] = str(datetime.now())[:-3]
    device_status["availability"] = device["availability"]
    device_status["response_time"] = device["response_time"]
    device_status["cpu"] = device["cpu"]
    device_status["memory"] = device["memory"]

    device_status_obj = DeviceStatus(**device_status)
    db.session.add(device_status_obj)

    db.session.commit()


def record_host_status(host):

    host_status = dict()
    host_status["host_id"] = host["id"]
    host_status["timestamp"] = str(datetime.now())[:-3]
    host_status["availability"] = host["availability"]
    host_status["response_time"] = host["response_time"]

    host_status_obj = HostStatus(**host_status)
    db.session.add(host_status_obj)

    db.session.commit()


def record_host_hourly_summaries(hourly_summaries):

    for host_id, summary in hourly_summaries.items():

        host_hourly_summary = dict()
        host_hourly_summary["host_id"] = host_id
        host_hourly_summary["timestamp"] = summary["hour"]
        host_hourly_summary["availability"] = summary["availability"]
        host_hourly_summary["response_time"] = summary["response_time"]

        host_status_obj = HostStatusSummary(**host_hourly_summary)
        db.session.add(host_status_obj)

    db.session.commit()


def record_service_status(service):

    service_status = dict()
    service_status["service_id"] = service["id"]
    service_status["timestamp"] = str(datetime.now())[:-3]
    service_status["availability"] = service["availability"]
    service_status["response_time"] = service["response_time"]

    service_status_obj = ServiceStatus(**service_status)
    db.session.add(service_status_obj)

    db.session.commit()


def record_service_hourly_summaries(hourly_summaries):

    for service_id, summary in hourly_summaries.items():

        service_hourly_summary = dict()
        service_hourly_summary["service_id"] = service_id
        service_hourly_summary["timestamp"] = summary["hour"]
        service_hourly_summary["availability"] = summary["availability"]
        service_hourly_summary["response_time"] = summary["response_time"]

        service_status_obj = ServiceStatusSummary(**service_hourly_summary)
        db.session.add(service_status_obj)

    db.session.commit()


def get_host_status_data(host_id, num_datapoints):

    host_status_objs = (
        db.session.query(HostStatus)
        .filter_by(**{"host_id": host_id})
        .order_by(desc(HostStatus.timestamp))
        .limit(num_datapoints)
        .all()
    )

    host_status_data = list()
    for host_status_obj in host_status_objs:
        host_status_data.append(get_model_as_dict(host_status_obj))

    return host_status_data


def get_host_summary_data(host_id, num_datapoints):

    host_summary_objs = (
        db.session.query(HostStatusSummary)
        .filter_by(**{"host_id": host_id})
        .order_by(desc(HostStatusSummary.timestamp))
        .limit(num_datapoints)
        .all()
    )

    host_summary_data = list()
    for host_status_obj in host_summary_objs:
        host_summary_data.append(get_model_as_dict(host_status_obj))

    return host_summary_data


def get_host_status_data_for_hour(host_id, hour):

    host_status_objs = (
        db.session.query(HostStatus)
        .filter_by(**{"host_id": host_id})
        .filter(HostStatus.timestamp.startswith(hour))
        .all()
    )

    host_status_data = list()
    for host_status_obj in host_status_objs:
        host_status_data.append(get_model_as_dict(host_status_obj))

    return host_status_data


def get_service_status_data(service_id, num_datapoints):

    service_status_objs = (
        db.session.query(ServiceStatus)
        .filter_by(**{"service_id": service_id})
        .order_by(desc(ServiceStatus.timestamp))
        .limit(num_datapoints)
        .all()
    )

    service_status_data = list()
    for service_status_obj in service_status_objs:
        service_status_data.append(get_model_as_dict(service_status_obj))

    return service_status_data


def get_service_summary_data(service_id, num_datapoints):

    service_summary_objs = (
        db.session.query(ServiceStatusSummary)
        .filter_by(**{"service_id": service_id})
        .order_by(desc(ServiceStatusSummary.timestamp))
        .limit(num_datapoints)
        .all()
    )

    service_summary_data = list()
    for service_status_obj in service_summary_objs:
        service_summary_data.append(get_model_as_dict(service_status_obj))

    return service_summary_data


def get_service_status_data_for_hour(service_id, hour):

    service_status_objs = (
        db.session.query(ServiceStatus)
        .filter_by(**{"service_id": service_id})
        .filter(ServiceStatus.timestamp.startswith(hour))
        .all()
    )

    service_status_data = list()
    for service_status_obj in service_status_objs:
        service_status_data.append(get_model_as_dict(service_status_obj))

    return service_status_data


def get_device_status_data(device_name, num_datapoints):

    result, info = get_device(device_name=device_name)
    if result != "success":
        return result, info

    device_id = info["id"]
    device_status_objs = (
        db.session.query(DeviceStatus)
        .filter_by(**{"device_id": device_id})
        .order_by(desc(DeviceStatus.timestamp))
        .limit(num_datapoints)
        .all()
    )

    device_status_data = list()
    for device_status_obj in device_status_objs:
        device_status_data.append(get_model_as_dict(device_status_obj))

    return device_status_data


def get_device_status_data_for_hour(device_id, hour):

    device_status_objs = (
        db.session.query(DeviceStatus)
        .filter_by(**{"device_id": device_id})
        .filter(DeviceStatus.timestamp.startswith(hour))
        .all()
    )

    device_status_data = list()
    for device_status_obj in device_status_objs:
        device_status_data.append(get_model_as_dict(device_status_obj))

    return device_status_data


def log_event(time, source_type, source, severity, info):

    event = dict()
    event["time"] = time
    event["source_type"] = source_type
    event["source"] = source
    event["severity"] = severity
    event["info"] = info

    event_obj = Event(**event)
    db.session.add(event_obj)

    db.session.commit()


def get_all_events(num_events):

    event_objs = (
        db.session.query(Event).order_by(desc(Event.time)).limit(num_events).all()
    )

    events = list()
    for event_obj in event_objs:
        event = get_model_as_dict(event_obj)
        events.append(event)

    return events


def record_capture(timestamp, source, captured_packets):

    for captured_packet in captured_packets:

        packet = dict()
        packet["timestamp"] = str(datetime.now())[:-3]
        packet["local_timestamp"] = timestamp
        packet["source"] = source

        if "Ethernet" in captured_packet:
            if "dst" in captured_packet["Ethernet"]:
                packet["ether_dst"] = captured_packet["Ethernet"]["dst"]
            if "src" in captured_packet["Ethernet"]:
                packet["ether_src"] = captured_packet["Ethernet"]["src"]

        if "IP" in captured_packet:
            if "dst" in captured_packet["IP"]:
                packet["ip_dst"] = captured_packet["IP"]["dst"]
            if "src" in captured_packet["IP"]:
                packet["ip_src"] = captured_packet["IP"]["src"]

        if "TCP" in captured_packet:
            packet["protocol"] = "TCP"
            if "dport" in captured_packet["TCP"]:
                packet["dport"] = captured_packet["TCP"]["dport"]
            if "sport" in captured_packet["TCP"]:
                packet["sport"] = captured_packet["TCP"]["sport"]

            if packet["sport"] == 443 or packet["dport"] == 443:
                packet["protocol"] = "HTTPS"
            elif packet["sport"] == 80 or packet["dport"] == 80:
                packet["protocol"] = "HTTP"

        elif "UDP" in captured_packet:
            packet["protocol"] = "UDP"
            if "dport" in captured_packet["UDP"]:
                packet["dport"] = captured_packet["UDP"]["dport"]
            if "sport" in captured_packet["UDP"]:
                packet["sport"] = captured_packet["UDP"]["sport"]

            if packet["sport"] == 123 or packet["dport"] == 123:
                packet["protocol"] = "NTP"

        if "DNS" in captured_packet:
            packet["protocol"] = "DNS"
        elif "ARP" in captured_packet:
            packet["protocol"] = "ARP"
        elif "DHCP" in captured_packet:
            packet["protocol"] = "DCHP"
        elif "ICMP" in captured_packet:
            packet["protocol"] = "ICMP"

        # capture["packet_json"] = json.dumps(packet)
        packet["packet_hexdump"] = captured_packet["hexdump"]
        del captured_packet["hexdump"]
        packet["packet_json"] = pformat(captured_packet)

        capture_obj = Capture(**packet)
        db.session.add(capture_obj)

        db.session.commit()


def get_capture(ip, protocol, port, num_packets):

    # We must generate and implement specific queries based on what has been requested
    # Note that if we add more imports, we'll have to modify this simple method to handle all cases
    if ip and not protocol:  # Note that if not protocol, port isn't relevant
        packet_objs = (
            db.session.query(Capture)
            .filter(or_(Capture.ip_src == ip, Capture.ip_dst == ip))
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )
    elif ip and protocol and not port:
        packet_objs = (
            db.session.query(Capture)
            .filter(or_(Capture.ip_src == ip, Capture.ip_dst == ip))
            .filter(func.lower(Capture.protocol) == func.lower(protocol))
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )
    elif ip and protocol and port:
        packet_objs = (
            db.session.query(Capture)
            .filter(or_(Capture.ip_src == ip, Capture.ip_dst == ip))
            .filter(func.lower(Capture.protocol) == func.lower(protocol))
            .filter(or_(Capture.sport == port, Capture.dport == port))
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )
    elif not ip and protocol and not port:
        packet_objs = (
            db.session.query(Capture)
            .filter(func.lower(Capture.protocol) == func.lower(protocol))
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )
    elif not ip and protocol and port:
        packet_objs = (
            db.session.query(Capture)
            .filter(func.lower(Capture.protocol) == func.lower(protocol))
            .filter(or_(Capture.sport == port, Capture.dport == port))
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )
    else:  # Not sure what was requested, so just get everything
        packet_objs = (
            db.session.query(Capture)
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )

    packets = list()
    for packet_obj in packet_objs:
        packet = get_model_as_dict(packet_obj)
        packets.append(packet)

    return packets


def record_portscan(portscan_info):

    portscan = dict()
    if "source" not in portscan_info:
        log_console(f"record_portscan: missing 'source' in portscan info")
        return
    if "host_ip" not in portscan_info:
        log_console(f"record_portscan: missing 'host_ip' in portscan info")
        return
    if "host_name" not in portscan_info:
        log_console(f"record_portscan: missing 'host_name' in portscan info")
        return
    if "token" not in portscan_info:
        log_console(f"record_portscan: missing 'token' in portscan_info")
        return
    if "timestamp" not in portscan_info:
        log_console(f"record_portscan: missing 'timestamp' in portscan info")
        return
    if "scan_output" not in portscan_info:
        log_console(f"record_portscan: missing 'scan_output' in portscan info")
        return

    portscan["source"] = portscan_info["source"]
    portscan["host_ip"] = portscan_info["host_ip"]
    portscan["host_name"] = portscan_info["host_name"]
    portscan["token"] = portscan_info["token"]
    portscan["timestamp"] = portscan_info["timestamp"]
    portscan["scan_output"] = portscan_info["scan_output"]

    portscan_obj = Portscan(**portscan)
    db.session.add(portscan_obj)

    db.session.commit()


def get_port_scan_extended(host_ip, host_name, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        search = {"host_ip": host_ip, "host_name": host_name, "token": token}
        portscan_obj = db.session.query(Portscan).filter_by(**search).one_or_none()

        if not portscan_obj:
            time.sleep(2)
            continue

        portscan = get_model_as_dict(portscan_obj)
        return "success", portscan["scan_output"]

    return "failed", "No scan results in time provided"


def record_traceroute(traceroute_info):

    traceroute = dict()
    if "source" not in traceroute_info:
        log_console(f"record_traceroute: missing 'source' in traceroute info")
        return
    if "target" not in traceroute_info:
        log_console(f"record_traceroute: missing 'target' in traceroute info")
        return
    if "token" not in traceroute_info:
        log_console(f"record_traceroute: missing 'token' in traceroute_info")
        return
    if "timestamp" not in traceroute_info:
        log_console(f"record_traceroute: missing 'timestamp' in traceroute info")
        return
    if "traceroute_img" not in traceroute_info:
        log_console(f"record_traceroute: missing 'traceroute_img' in traceroute info")
        return

    traceroute["source"] = traceroute_info["source"]
    traceroute["target"] = traceroute_info["target"]
    traceroute["token"] = traceroute_info["token"]
    traceroute["timestamp"] = traceroute_info["timestamp"]
    traceroute["traceroute_img"] = traceroute_info["traceroute_img"]

    traceroute_obj = Traceroute(**traceroute)
    db.session.add(traceroute_obj)

    db.session.commit()


def get_traceroute(target, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        # search = {"target": target, "token": token}  # 'target' may have been modified
        search = {"token": token}
        traceroute_obj = db.session.query(Traceroute).filter_by(**search).one_or_none()

        if not traceroute_obj:
            time.sleep(2)
            continue

        traceroute = get_model_as_dict(traceroute_obj)
        return "success", traceroute["traceroute_img"]

    return "failed", "No traceroute results in time provided"


def record_device_config(device_id, config):

    device_config = dict()
    device_config["device_id"] = device_id
    device_config["timestamp"] = str(datetime.now())[:-3]
    device_config["config"] = config

    device_config_obj = DeviceConfig(**device_config)
    db.session.add(device_config_obj)

    db.session.commit()


def get_device_config_diff(device, num_configs):

    device_configs = (
        db.session.query(DeviceConfig)
        .filter_by(**{"device_id": device["id"]})
        .order_by(desc(DeviceConfig.timestamp))
        .limit(num_configs)
        .all()
    )

    config_diff = {"current": dict(), "old": dict()}
    if len(device_configs) == 0:
        return "success", config_diff

    config_diff["current"]["timestamp"] = device_configs[0].timestamp
    config_diff["current"]["config"] = device_configs[0].config

    for device_config in device_configs[1:]:

        config_diff["old"]["timestamp"] = device_config.timestamp
        config_diff["old"]["config"] = device_config.config

        if config_diff["current"]["config"] != device_config.config:
            return "success", config_diff

    else:
        return "success", config_diff


def get_worker(worker_id=None, serial=None, host=None, worker_type=None):

    search = dict()
    if worker_id:
        search["id"] = worker_id
    else:
        if not serial and not host:
            return "failed", "Must provide serial or host"
        if not worker_type:
            return "failed", "Must provide worker type"
        if serial:
            search["serial"] = serial
        if host:
            search["host"] = host
        search["worker_type"] = worker_type

    worker_obj = db.session.query(Worker).filter_by(**search).one_or_none()
    if not worker_obj:
        return "failed", "Could not find worker in DB"

    return "success", get_model_as_dict(worker_obj)


def get_all_workers():

    worker_objs = db.session.query(Worker).all()

    workers = list()
    for worker_obj in worker_objs:
        workers.append(get_model_as_dict(worker_obj))

    return workers


def get_worker_status_data(worker_id, num_datapoints):

    worker_status_objs = (
        db.session.query(WorkerStatus)
        .filter_by(**{"worker_id": worker_id})
        .order_by(desc(WorkerStatus.timestamp))
        .limit(num_datapoints)
        .all()
    )

    worker_status_data = list()
    for worker_status_obj in worker_status_objs:
        worker_status_data.append(get_model_as_dict(worker_status_obj))

    return worker_status_data


def set_worker(worker):

    search = {"name": worker["name"], "worker_type": worker["worker_type"]}
    worker_obj = db.session.query(Worker).filter_by(**search).one_or_none()
    if not worker_obj:
        worker_obj = Worker(**worker)
        db.session.add(worker_obj)
    else:
        if "ip_address" in worker and worker["ip_address"]:
            worker_obj.ip_address = worker["ip_address"]
        if "serial" in worker and worker["serial"]:
            worker_obj.serial_no = worker["serial"]
        if "uptime" in worker and worker["uptime"]:
            worker_obj.uptime = worker["uptime"]
        if "availability" in worker and worker["availability"] is not None:
            worker_obj.availability = worker["availability"]
        if "response_time" in worker and worker["response_time"]:
            worker_obj.response_time = worker["response_time"]
        if "last_heard" in worker and worker["last_heard"]:
            worker_obj.last_heard = worker["last_heard"]
        if "cpu" in worker and worker["cpu"]:
            worker_obj.cpu = worker["cpu"]
        if "memory" in worker and worker["memory"]:
            worker_obj.memory = worker["memory"]

    db.session.commit()


def record_worker_status(worker):

    worker_status = dict()
    worker_status["worker_id"] = worker["id"]
    worker_status["timestamp"] = str(datetime.now())[:-3]
    worker_status["availability"] = worker["availability"]
    worker_status["response_time"] = worker["response_time"]
    worker_status["cpu"] = worker["cpu"]
    worker_status["memory"] = worker["memory"]

    worker_status_obj = WorkerStatus(**worker_status)
    db.session.add(worker_status_obj)

    db.session.commit()


def import_workers(filename=None, filetype=None):

    if not filename or not filetype:
        return None

    db.session.query(Worker).delete()
    with open("quokka/data/" + filename, "r") as import_file:

        if filetype.lower() == "json":
            workers = json.loads(import_file.read())
        elif filetype.lower() == "yaml":
            workers = yaml.safe_load(import_file.read())
        else:
            return None

    set_workers(workers)
    return {"workers": workers}


def set_workers(workers):

    for worker in workers:

        worker_obj = Worker(**worker)
        db.session.add(worker_obj)

    db.session.commit()


def set_command(command):

    command_obj = Command(**command)
    db.session.add(command_obj)

    db.session.commit()


def get_commands(serial=None, host=None, worker_type=None, set_delivered=False):

    if not serial and not host:
        return "failed", "Must provide serial or host"
    if not worker_type:
        return "failed", "must provide worker_type"

    search = dict()
    if serial:
        search["serial"] = serial
    if host:
        search["host"] = host
    search["worker_type"] = worker_type
    search["delivered"] = False

    command_objs = db.session.query(Command).filter_by(**search).all()

    commands = list()
    for command_obj in command_objs:
        commands.append(get_model_as_dict(command_obj))

    if set_delivered:
        for command_obj in command_objs:
            command_obj.delivered = True
        db.session.commit()

    return "success", commands
