import json
import time
from datetime import datetime
from pprint import pformat

import yaml
from sqlalchemy import desc, or_, func

from quokka import db
from quokka.controller.utils import log_console
from quokka.models.Capture import Capture
from quokka.models.Command import Command
from quokka.models.Event import Event
from quokka.models.Portscan import Portscan
from quokka.models.Service import Service
from quokka.models.ServiceStatus import ServiceStatus
from quokka.models.ServiceStatusSummary import ServiceStatusSummary
from quokka.models.Traceroute import Traceroute
from quokka.models.Worker import Worker
from quokka.models.WorkerStatus import WorkerStatus
from quokka.models.util import get_model_as_dict


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
