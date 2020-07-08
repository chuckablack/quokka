from datetime import datetime
import time

from quokka.controller.utils import log_console
from quokka.models.apis import (
    get_all_hosts,
    get_host_ts_data_for_hour,
    get_all_services,
    get_service_ts_data_for_hour,
    get_all_devices,
    get_device_ts_data_for_hour,
    record_service_hourly_summaries,
    record_host_hourly_summaries,
)


class SummariesTask:
    def __init__(self):
        self.terminate = False
        self.current_hour = str(datetime.now())[:-13]

    def set_terminate(self):
        self.terminate = True
        log_console(f"{self.__class__.__name__}: Terminate pending")

    # def get_device_summaries(self):
    #     log_console(f"Calculating device summaries for {self.current_hour}")
    #     return
    #
    # def get_host_summaries(self):
    #
    #     log_console(f"Calculating host summaries for {self.current_hour}")
    #     hosts = get_all_hosts()
    #     for host in hosts:
    #         host_ts_data = get_host_ts_data_for_hour(host["id"], self.current_hour)
    #
    #         host_hourly_summary = dict()
    #         host_hourly_summary["hour"] = str(datetime.fromisoformat(self.current_hour))
    #         host_hourly_summary["availability"] = 0
    #         host_hourly_summary["response_time"] = 0
    #
    #         num_availability_records = 0
    #         num_response_time_records = 0
    #
    #         for host_ts_data_item in host_ts_data:
    #             num_availability_records += 1
    #             if host_ts_data_item["availability"]:
    #                 host_hourly_summary["availability"] += 100
    #                 host_hourly_summary["response_time"] += host_ts_data_item["response_time"]
    #                 num_response_time_records += 1
    #
    #         if num_response_time_records > 0:
    #             host_hourly_summary["response_time"] = (
    #                 host_hourly_summary["response_time"] / num_response_time_records
    #             )
    #         if num_availability_records > 0:
    #             host_hourly_summary["availability"] = (
    #                 host_hourly_summary["availability"] / num_response_time_records
    #             )
    #
    #         log_console(f"Host hourly summary for {host['name']}: {host_hourly_summary}")
    #
    #     return
    #
    # def get_service_summaries(self):
    #
    #     log_console(f"Calculating service summaries for {self.current_hour}")
    #     services = get_all_services()
    #     for service in services:
    #         service_ts_data = get_service_ts_data_for_hour(service["id"], self.current_hour)
    #
    #         service_hourly_summary = dict()
    #         service_hourly_summary["hour"] = str(datetime.fromisoformat(self.current_hour))
    #         service_hourly_summary["availability"] = 0
    #         service_hourly_summary["response_time"] = 0
    #
    #         num_availability_records = 0
    #         num_response_time_records = 0
    #
    #         for service_ts_data_item in service_ts_data:
    #             num_availability_records += 1
    #             if service_ts_data_item["availability"]:
    #                 service_hourly_summary["availability"] += 100
    #                 service_hourly_summary["response_time"] += service_ts_data_item["response_time"]
    #                 num_response_time_records += 1
    #
    #         if num_response_time_records > 0:
    #             service_hourly_summary["response_time"] = (
    #                 service_hourly_summary["response_time"] / num_response_time_records
    #             )
    #         if num_availability_records > 0:
    #             service_hourly_summary["availability"] = (
    #                 service_hourly_summary["availability"] / num_availability_records
    #             )
    #
    #         log_console(f"Service hourly summary for {service['name']}: {service_hourly_summary}")

    def get_summaries(self, items, item_type, get_hour_data_function):

        log_console(f"Calculating {item_type} summaries for {self.current_hour}")
        hourly_summaries = dict()

        for item in items:
            service_ts_data = get_hour_data_function(item["id"], self.current_hour)

            hourly_summary = dict()
            hourly_summary["id"] = item["id"]
            hourly_summary["hour"] = str(datetime.fromisoformat(self.current_hour))
            hourly_summary["availability"] = 0
            hourly_summary["response_time"] = 0

            num_availability_records = 0
            num_response_time_records = 0

            for service_ts_data_item in service_ts_data:
                num_availability_records += 1
                if service_ts_data_item["availability"]:
                    hourly_summary["availability"] += 100
                    hourly_summary["response_time"] += service_ts_data_item["response_time"]
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

        return hourly_summaries

    def start(self, interval):

        while True and not self.terminate:

            this_hour = str(datetime.now())[:-13]
            if this_hour == self.current_hour:
                time.sleep(60)
                continue

            service_hourly_summaries = self.get_summaries(get_all_services(), "services", get_service_ts_data_for_hour)
            record_service_hourly_summaries(service_hourly_summaries)
            host_hourly_summaries = self.get_summaries(get_all_hosts(), "hosts", get_host_ts_data_for_hour)
            record_host_hourly_summaries(host_hourly_summaries)
            self.get_summaries(get_all_devices(), "devices", get_device_ts_data_for_hour)

            self.current_hour = this_hour

        log_console("...gracefully exiting summaries task")
