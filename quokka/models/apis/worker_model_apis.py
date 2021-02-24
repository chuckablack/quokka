import json
from datetime import datetime

import yaml
from sqlalchemy import desc

from quokka import db
from quokka.models.Worker import Worker
from quokka.models.WorkerStatus import WorkerStatus
from quokka.models.util import get_model_as_dict


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
        return None
    else:
        return get_model_as_dict(worker_obj)


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
