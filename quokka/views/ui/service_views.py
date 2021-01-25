from flask import request

from quokka import app
from quokka.models.apis import (
    get_service,
    get_all_services,
    get_service_status_data,
    get_service_summary_data,
)


@app.route("/ui/services", methods=["GET"])
def services():

    if request.method == "GET":
        return {"services": get_all_services()}

    else:
        return "Invalid request method"


@app.route("/ui/service/status", methods=["GET"])
def service_status():

    service_id = request.args.get("serviceid")
    num_datapoints = request.args.get("datapoints")

    if not service_id or not num_datapoints:
        return "Must provide serviceid and datapoints", 400

    return {
        "service_data": get_service_status_data(service_id, num_datapoints),
        "service_summary": get_service_summary_data(service_id, num_datapoints),
        "service": get_service(service_id),
    }
