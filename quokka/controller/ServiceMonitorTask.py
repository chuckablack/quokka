from datetime import datetime
import time
import requests

from dns.resolver import Resolver, Timeout, NXDOMAIN
from ntplib import NTPClient, NTPException

from quokka.models.apis import get_all_services
from quokka.models.apis import set_service


def get_avail_and_rsp_time(service):

    time_start = time.time()
    if service["type"] == "http":
        try:
            response = requests.get(service["target"])
        except BaseException as e:
            print(f"!!! Exception in HTTP service monitoring: {repr(e)}")
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
            print(f'!!! DNS monitor: nonexistent domain name {service["data"]}')
            return False, None
        except Timeout as e:
            print(f'!!! DNS monitor: DNS request timed out for {service["target"]}')
            return False, None
        except BaseException as e:
            print(f"!!! DNS monitor: Exception occurred: {repr(e)}")
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
            print(
                f"!!! NTP error encountered for {service['target']}, error: {repr(e)}"
            )
            return False, None

        availability = True
        response_time = time.time() - time_start

    else:
        print(f"!!! Unknown service type: {service['type']}")
        return False, None

    return availability, response_time


class ServiceMonitorTask:
    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        self.terminate = True
        print(self.__class__.__name__, "Terminate pending")

    def monitor(self, interval):

        while True and not self.terminate:

            services = get_all_services()
            print(f"Monitor: Beginning monitoring for {len(services)} services")
            for service in services:

                if self.terminate:
                    break

                print(f"--- service monitor for {service['name']}")
                availability, response_time = get_avail_and_rsp_time(service)
                service["availability"] = availability
                if not availability:
                    set_service(service)
                    continue

                service["response_time"] = int(response_time * 1000)
                service["last_heard"] = str(datetime.now())[:-3]

                set_service(service)

            for _ in range(0, int(interval / 10)):
                time.sleep(10)
                if self.terminate:
                    break

        print("...gracefully exiting monitor:service")
