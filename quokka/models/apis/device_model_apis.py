import json
from datetime import datetime

import yaml
from sqlalchemy import desc

from quokka import db
from quokka.controller.utils import log_console
from quokka.models.Compliance import Compliance
from quokka.models.Device import Device
from quokka.models.DeviceConfig import DeviceConfig
from quokka.models.DeviceFacts import DeviceFacts
from quokka.models.DeviceStatus import DeviceStatus
from quokka.models.util import get_model_as_dict
from quokka.models.apis.event_model_apis import log_event


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
