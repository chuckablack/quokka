from datetime import datetime
import time
import requests

from dns.resolver import Resolver, Timeout, NXDOMAIN
from ntplib import NTPClient, NTPException

from quokka.models.apis.event_model_apis import log_event
from quokka.models.apis.service_model_apis import (
    get_all_services,
    set_service,
    record_service_status,
)
from quokka.controller.utils import log_console


def get_avail_and_rsp_time(service):

    time_start = time.time()
    if service["type"] == "https" or service["type"] == "http":

        try:
            response = requests.get(service["target"])
        except BaseException as e:
            log_console(f"!!! Exception in HTTP service monitoring: {repr(e)}")
            return False, None

        if response.status_code == requests.codes.ok:
            availability = True
            response_time = time.time() - time_start
        else:
            return False, None

    elif service["type"] == "dns":
        target_resolver = Resolver()
        target_resolver.nameservers = [service["target"]]

        time_start = time.time()
        try:
            response = target_resolver.query(service["data"])
        except NXDOMAIN as e:
            log_console(f'!!! DNS monitor: nonexistent domain name {service["data"]}')
            return False, None
        except Timeout as e:
            log_console(
                f'!!! DNS monitor: DNS request timed out for {service["target"]}'
            )
            return False, None
        except BaseException as e:
            log_console(f"!!! DNS monitor: Exception occurred: {repr(e)}")
            return False, None

        if (
            response is not None
            and response.response is not None
            and len(response.response.answer) > 0
        ):
            availability = True
            response_time = time.time() - time_start
        else:
            return False, None

    elif service["type"] == "ntp":
        server = service["target"]
        c = NTPClient()
        time_start = time.time()
        try:
            result = c.request(server, version=3)
        except NTPException as e:
            log_console(
                f"!!! NTP error encountered for {service['target']}, error: {repr(e)}"
            )
            return False, None

        availability = True
        response_time = time.time() - time_start

    else:
        log_console(f"!!! Unknown service type: {service['type']}")
        return False, None

    return availability, response_time


class ServiceMonitorTask:
    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            log_console(f"{self.__class__.__name__}: Terminate pending")

    def monitor(self, interval):

        log_console(f"Service monitoring starting, interval={interval}")
        while True and not self.terminate:

            services = get_all_services()
            log_console(f"Monitor: Beginning monitoring for {len(services)} services")
            for service in services:

                if self.terminate:
                    break

                log_console(f"--- service monitor for {service['name']}")
                availability, response_time = get_avail_and_rsp_time(service)
                service["availability"] = availability
                if not availability:
                    record_service_status(service)
                    set_service(service)
                    log_event(
                        str(datetime.now())[:-3],
                        "service monitor",
                        service["name"],
                        "WARNING",
                        f"Availability failed for service: {service['name']}",
                    )
                    continue

                service["response_time"] = int(response_time * 1000)
                service["last_heard"] = str(datetime.now())[:-3]

                record_service_status(service)
                set_service(service)

            for _ in range(0, int(interval / 10)):
                time.sleep(10)
                if self.terminate:
                    break

        log_console("...gracefully exiting monitor:service")
