from flask import request

from quokka import app
from quokka.models.apis.host_model_apis import (
    get_host,
    get_all_hosts,
    get_host_status_data,
    get_host_summary_data,
)


@app.route("/ui/hosts", methods=["GET"])
def hosts():
    return {"hosts": get_all_hosts()}


@app.route("/ui/host/status", methods=["GET"])
def host_status():

    host_id = request.args.get("hostid")
    num_datapoints = request.args.get("datapoints")

    if not host_id or not num_datapoints:
        return "Must provide hostid and datapoints", 400

    return {
        "host_data": get_host_status_data(host_id, num_datapoints),
        "host_summary": get_host_summary_data(host_id, num_datapoints),
        "host": get_host(host_id),
    }
