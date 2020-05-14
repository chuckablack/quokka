import json
import yaml
from quokka import db


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    ip_address = db.Column(db.Text, unique=True, nullable=False)
    vendor = db.Column(db.Text)
    os = db.Column(db.Text)
    ssh_username = db.Column(db.Text)
    ssh_password = db.Column(db.Text)

    def __repr__(self):
        return '<Device %r>' % self.name


def get_devices():

    devices_obj = Device.query.all()

    devices = list()
    for device_obj in devices_obj:
        devices.append(dict(device_obj))

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
    with open(filename, "r") as import_file:

        if filetype.lower() == "json":
            inventory = json.loads(import_file.read())
        elif filetype.lower() == "yaml":
            inventory = yaml.load(import_file.read())
        else:
            return None

    set_devices(inventory)


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


