import json
import yaml

from quokka import db

from quokka.models.Device import Device
from quokka.models.DeviceFacts import DeviceFacts
from quokka.models.Compliance import Compliance
from quokka.models.Host import Host
from quokka.models.Service import Service

from quokka.models.util import get_model_as_dict


def get_device(device_id=None, device_name=None):

    if device_id and device_name:
        return "failed", "Must provide either device_id or device_name, but not both"

    if device_id:
        search = {"id": device_id}
    elif device_name:
        search = {"name": device_name}
    else:
        return "failed", "Must provide either device_id or device_name"

    device_obj = Device.query.filter_by(**search).one_or_none()
    if not device_obj:
        return "failed", "Could not find device in DB"

    # return "success", dict(device_obj)
    return "success", device_obj.__dict__


def get_all_devices():

    device_objs = Device.query.all()

    devices = list()
    for device_obj in device_objs:
        devices.append(get_model_as_dict(device_obj))

    return devices


def get_facts(device_name):

    facts_obj = DeviceFacts.query.filter_by(**{"device_name": device_name}).one_or_none()
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
    device_obj = Device.query.filter_by(**search).one_or_none()
    if not device_obj:
        device_obj = Device(**device)
        db.session.add(device_obj)
    else:
        if "ip_address" in device and device["ip_address"]:
            device_obj.ip_address = device["ip_address"]
        if "mac_address" in device and device["mac_address"]:
            device_obj.mac_address = device["mac_address"]
        if "availability" in device and device["availability"]:
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

    facts_obj = DeviceFacts.query.filter_by(**{"device_name": device_facts["device_name"]}).one_or_none()
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

    Device.query.delete()
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

    Compliance.query.delete()

    try:
        with open("quokka/data/" + filename, "r") as import_file:
            standards = yaml.safe_load(import_file.read())
    except FileNotFoundError as e:
        print(f"Could not import compliance file: {repr(e)}")

    for standard in standards:
        standard_obj = Compliance(**standard)
        db.session.add(standard_obj)

    db.session.commit()
    return


def import_services(filename=None):

    Service.query.delete()

    try:
        with open("quokka/data/" + filename, "r") as import_file:
            services = yaml.safe_load(import_file.read())
    except FileNotFoundError as e:
        print(f"Could not import services file: {repr(e)}")

    for service in services:
        service_obj = Compliance(**service)
        db.session.add(service_obj)

    db.session.commit()
    return


def get_host(hostname):

    search = {"name": hostname}
    host_obj = Host.query.filter_by(**search).one_or_none()
    if not host_obj:
        return None
    else:
        return get_model_as_dict(host_obj)


def get_all_hosts():

    host_objs = Host.query.all()

    hosts = list()
    for host_obj in host_objs:
        host = get_model_as_dict(host_obj)
        hosts.append(host)

    return hosts


def set_host(host):

    search = {"name": host["name"]}
    host_obj = Host.query.filter_by(**search).one_or_none()
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


def get_status():
    return None


def get_versions():
    return None
