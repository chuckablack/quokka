from datetime import datetime

from sqlalchemy import desc

from quokka import db
from quokka.models.Host import Host
from quokka.models.HostStatus import HostStatus
from quokka.models.HostStatusSummary import HostStatusSummary
from quokka.models.util import get_model_as_dict


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
