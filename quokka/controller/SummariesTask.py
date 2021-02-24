from datetime import datetime
import time

from quokka.controller.utils import log_console
from quokka.models.apis.event_model_apis import log_event
from quokka.models.apis.service_model_apis import (
    get_all_services,
    get_service_status_data_for_hour,
    record_service_hourly_summaries,
)
from quokka.models.apis.host_model_apis import (
    get_all_hosts,
    get_host_status_data_for_hour,
    record_host_hourly_summaries,
 )
from quokka.models.apis.device_model_apis import (
    get_all_devices,
    get_device_status_data_for_hour,
)


class SummariesTask:
    def __init__(self):
        self.terminate = False
        self.current_hour = str(datetime.now())[:-13]

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            log_console(f"{self.__class__.__name__}: Terminate pending")

    def get_summaries(self, items, item_type, get_hour_data_function):

        log_console(f"Calculating {item_type} summaries for {self.current_hour}")
        hourly_summaries = dict()

        for item in items:
            service_status_data = get_hour_data_function(item["id"], self.current_hour)

            hourly_summary = dict()
            hourly_summary["id"] = item["id"]
            hourly_summary["hour"] = str(datetime.fromisoformat(self.current_hour))
            hourly_summary["availability"] = 0
            hourly_summary["response_time"] = 0

            num_availability_records = 0
            num_response_time_records = 0

            for service_status_data_item in service_status_data:
                num_availability_records += 1
                if service_status_data_item["availability"]:
                    hourly_summary["availability"] += 100
                    hourly_summary["response_time"] += service_status_data_item["response_time"]
                    num_response_time_records += 1

            if num_response_time_records > 0:
                hourly_summary["response_time"] = (
                    hourly_summary["response_time"] / num_response_time_records
                )
            if num_availability_records > 0:
                hourly_summary["availability"] = (
                    hourly_summary["availability"] / num_availability_records
                )

            log_console(f"Summary: {item_type} hourly summary for {item['name']}: {hourly_summary}")
            hourly_summaries[item["id"]] = hourly_summary

            rsp_time_in_seconds = hourly_summary["response_time"] / 1000
            if "sla_response_time" in item and rsp_time_in_seconds > item["sla_response_time"]:
                info = f"SLA response time violation, {rsp_time_in_seconds:.2f} > {item['sla_response_time']}"
                log_event(str(datetime.now())[:-3], item_type, item["name"], "WARNING", info)
            if (
                "sla_availability" in item
                and hourly_summary["availability"] < item["sla_availability"]
            ):
                info = f"SLA availability violation, {hourly_summary['availability']:.2f} < {item['sla_availability']}"
                log_event(str(datetime.now())[:-3], item_type, item["name"], "WARNING", info)

        return hourly_summaries

    def start(self, interval):

        while True and not self.terminate:

            this_hour = str(datetime.now())[:-13]
            if this_hour == self.current_hour:
                time.sleep(60)
                continue

            service_hourly_summaries = self.get_summaries(
                get_all_services(), "services", get_service_status_data_for_hour
            )
            record_service_hourly_summaries(service_hourly_summaries)
            host_hourly_summaries = self.get_summaries(
                get_all_hosts(), "hosts", get_host_status_data_for_hour
            )
            record_host_hourly_summaries(host_hourly_summaries)
            self.get_summaries(get_all_devices(), "devices", get_device_status_data_for_hour)

            self.current_hour = this_hour

        log_console("...gracefully exiting summaries task")
