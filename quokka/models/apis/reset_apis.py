from quokka import db

from quokka.models.Device import Device
from quokka.models.DeviceStatus import DeviceStatus
from quokka.models.DeviceFacts import DeviceFacts
from quokka.models.Compliance import Compliance
from quokka.models.Host import Host
from quokka.models.HostStatus import HostStatus
from quokka.models.Service import Service
from quokka.models.ServiceStatus import ServiceStatus
from quokka.models.Event import Event
from quokka.models.Capture import Capture
from quokka.models.apis.device_model_apis import import_devices, import_compliance
from quokka.models.apis.service_model_apis import import_services


def reset_devices():
    db.session.query(Device).delete()
    db.session.query(DeviceFacts).delete()
    db.session.query(DeviceStatus).delete()
    db.session.query(Compliance).delete()
    db.session.commit()

    import_devices(filename="devices.yaml", filetype="yaml")
    import_compliance(filename="compliance.yaml")
    return


def reset_hosts():
    db.session.query(HostStatus).delete()
    db.session.query(Host).delete()
    db.session.commit()

    return


def reset_services():
    db.session.query(ServiceStatus).delete()
    db.session.query(Service).delete()
    db.session.commit()
    import_services(filename="services.yaml")
    db.session.commit()

    return


def reset_events():
    db.session.query(Event).delete()
    db.session.commit()

    return


def reset_capture():
    db.session.query(Capture).delete()
    db.session.commit()

    return
