import json
import yaml
from datetime import datetime
from sqlalchemy import desc

from quokka import db

from quokka.models.Device import Device
from quokka.models.DeviceFacts import DeviceFacts
from quokka.models.Compliance import Compliance
from quokka.models.Host import Host
from quokka.models.Service import Service
from quokka.models.Event import Event

from quokka.models.DeviceStatusTS import DeviceStatusTS
from quokka.models.HostStatusTS import HostStatusTS
from quokka.models.ServiceStatusTS import ServiceStatusTS
from quokka.models.HostStatusSummary import HostStatusSummary
from quokka.models.ServiceStatusSummary import ServiceStatusSummary

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

    # device_objs = Device.query.all()
    device_objs = db.session.query(Device).all()

    devices = list()
    for device_obj in device_objs:
        devices.append(get_model_as_dict(device_obj))

    return devices


def get_facts(device_name):

    facts_obj = db.session.query(DeviceFacts).filter_by(
        **{"device_name": device_name}
    ).one_or_none()
    if not facts_obj:
        return "failed", "Could not find device facts in DB"

    return "success", get_model_as_dict(facts_obj)


def set_devices(devices):

    for device in devices:
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
        if "mac_address" in device and device["mac_address"]:
            device_obj.mac_address = device["mac_address"]
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
        if "os_compliance" in device and device["os_compliance"]:
            device_obj.os_compliance = device["os_compliance"]
        if "config_compliance" in device and device["config_compliance"]:
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

    facts_obj = db.session.query(DeviceFacts).filter_by(
        **{"device_name": device_facts["device_name"]}
    ).one_or_none()
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

    for service in services:
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

    device_status_obj = DeviceStatusTS(**device_status)
    db.session.add(device_status_obj)

    db.session.commit()


def record_host_status(host):

    host_status = dict()
    host_status["host_id"] = host["id"]
    host_status["timestamp"] = str(datetime.now())[:-3]
    host_status["availability"] = host["availability"]
    host_status["response_time"] = host["response_time"]

    host_status_obj = HostStatusTS(**host_status)
    db.session.add(host_status_obj)

    db.session.commit()


def record_service_status(service):

    service_status = dict()
    service_status["service_id"] = service["id"]
    service_status["timestamp"] = str(datetime.now())[:-3]
    service_status["availability"] = service["availability"]
    service_status["response_time"] = service["response_time"]

    service_status_obj = ServiceStatusTS(**service_status)
    db.session.add(service_status_obj)

    db.session.commit()


def record_service_hourly_summaries(hourly_summaries):

    for id, summary in hourly_summaries.items():

        service_hourly_summary = dict()
        service_hourly_summary["service_id"] = id
        service_hourly_summary["timestamp"] = summary["hour"]
        service_hourly_summary["availability"] = summary["availability"]
        service_hourly_summary["response_time"] = summary["response_time"]

        service_status_obj = ServiceStatusSummary(**service_hourly_summary)
        db.session.add(service_status_obj)

    db.session.commit()


def get_host_ts_data(host_id, num_datapoints):

    host_ts_objs = (
        db.session.query(HostStatusTS).filter_by(**{"host_id": host_id})
        .order_by(desc(HostStatusTS.timestamp))
        .limit(num_datapoints)
        .all()
    )

    host_ts_data = list()
    for host_ts_obj in host_ts_objs:
        host_ts_data.append(get_model_as_dict(host_ts_obj))

    return host_ts_data


def get_host_ts_data_for_hour(host_id, hour):

    host_ts_objs = (
        db.session.query(HostStatusTS).filter_by(**{"host_id": host_id})
        .filter(HostStatusTS.timestamp.startswith(hour))
        .all()
    )

    host_ts_data = list()
    for host_ts_obj in host_ts_objs:
        host_ts_data.append(get_model_as_dict(host_ts_obj))

    return host_ts_data


def get_service_ts_data(service_id, num_datapoints):

    service_ts_objs = (
        db.session.query(ServiceStatusTS).filter_by(**{"service_id": service_id})
        .order_by(desc(ServiceStatusTS.timestamp))
        .limit(num_datapoints)
        .all()
    )

    service_ts_data = list()
    for service_ts_obj in service_ts_objs:
        service_ts_data.append(get_model_as_dict(service_ts_obj))

    return service_ts_data


def get_service_summary_data(service_id, num_datapoints):

    service_summary_objs = (
        db.session.query(ServiceStatusSummary).filter_by(**{"service_id": service_id})
        .order_by(desc(ServiceStatusSummary.timestamp))
        .limit(num_datapoints)
        .all()
    )

    service_summary_data = list()
    for service_ts_obj in service_summary_objs:
        service_summary_data.append(get_model_as_dict(service_ts_obj))

    return service_summary_data


def get_service_ts_data_for_hour(service_id, hour):

    service_ts_objs = (
        db.session.query(ServiceStatusTS).filter_by(**{"service_id": service_id})
        .filter(ServiceStatusTS.timestamp.startswith(hour))
        .all()
    )

    service_ts_data = list()
    for service_ts_obj in service_ts_objs:
        service_ts_data.append(get_model_as_dict(service_ts_obj))

    return service_ts_data


def get_device_ts_data(device_name, num_datapoints):

    result, info = get_device(device_name=device_name)
    if result != "success":
        return result, info

    device_id = info["id"]
    device_ts_objs = (
        db.session.query(DeviceStatusTS).filter_by(**{"device_id": device_id})
        .order_by(desc(DeviceStatusTS.timestamp))
        .limit(num_datapoints)
        .all()
    )

    device_ts_data = list()
    for device_ts_obj in device_ts_objs:
        device_ts_data.append(get_model_as_dict(device_ts_obj))

    return device_ts_data


def get_device_ts_data_for_hour(device_id, hour):

    device_ts_objs = (
        db.session.query(DeviceStatusTS).filter_by(**{"device_id": device_id})
        .filter(DeviceStatusTS.timestamp.startswith(hour))
        .all()
    )

    device_ts_data = list()
    for device_ts_obj in device_ts_objs:
        device_ts_data.append(get_model_as_dict(device_ts_obj))

    return device_ts_data


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

    event_objs = db.session.query(Event).order_by(desc(Event.time)).limit(num_events).all()

    events = list()
    for event_obj in event_objs:
        event = get_model_as_dict(event_obj)
        events.append(event)

    return events
