from quokka import db

from quokka.models.Device import Device
from quokka.models.DeviceStatusTS import DeviceStatusTS
from quokka.models.DeviceFacts import DeviceFacts
from quokka.models.Compliance import Compliance
from quokka.models.Host import Host
from quokka.models.HostStatusTS import HostStatusTS
from quokka.models.Service import Service
from quokka.models.ServiceStatusTS import ServiceStatusTS
from quokka.models.Event import Event
from quokka.models.apis import import_devices, import_services, import_compliance


def reset_devices():
    Device.query.delete()
    DeviceFacts.query.delete()
    DeviceStatusTS.query.delete()
    Compliance.query.delete()
    db.session.commit()

    import_devices(filename="devices.yaml", filetype="yaml")
    import_compliance(filename="compliance.yaml")
    return


def reset_hosts():
    Host.query.delete()
    HostStatusTS.query.delete()
    db.session.commit()

    return


def reset_services():
    Service.query.delete()
    ServiceStatusTS.query.delete()
    import_services(filename="services.yaml")
    db.session.commit()

    return


def reset_events():
    Event.query.delete()
    db.session.commit()

    return
