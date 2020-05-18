import json
import yaml
from quokka import db
from quokka.models.Device import Device
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


def get_devices():

    device_objs = Device.query.all()

    devices = list()
    for device_obj in device_objs:
        devices.append(get_model_as_dict(device_obj))

    return devices


def set_devices(inventory):

    for device in inventory:
        device_obj = Device(**device)
        db.session.add(device_obj)

    db.session.commit()


def import_inventory(filename=None, filetype=None):

    if not filename or not filetype:
        return None

    Device.query.delete()
    with open("quokka/data/" + filename, "r") as import_file:

        if filetype.lower() == "json":
            inventory = json.loads(import_file.read())
        elif filetype.lower() == "yaml":
            inventory = yaml.load(import_file.read())
        else:
            return None

    set_devices(inventory)
    return {"inventory": inventory}


def export_inventory(filename=None, filetype=None):

    if not filename or not filetype:
        return None

    inventory = get_devices()

    with open(filename, "w") as output_file:

        if filetype.lower() == "json":
            output_file.write(json.dumps(inventory))
        elif filetype.lower() == "yaml":
            output_file.write(yaml.dump(inventory))
        else:
            return None


def get_status():
    return


def get_versions():
    return
