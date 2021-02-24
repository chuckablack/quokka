import socket
from datetime import datetime, timedelta
from time import sleep

from quokka.controller.device.device_status import get_device_status
from quokka.controller.utils import log_console
from quokka.models.apis.device_model_apis import (
    get_all_device_ids,
    get_device,
    set_device,
    record_device_status,
)
from quokka.models.apis.event_model_apis import log_event

MAX_NOT_HEARD_SECONDS = 90  # For sdwan devices, time to have not seen a heartbeat


def calculate_cpu(cpu):

    num_cpus = 0
    cpu_total = 0.0
    for cpu, usage in cpu.items():
        cpu_total += usage["%usage"]
        num_cpus += 1

    return int(cpu_total / num_cpus)


def calculate_memory(memory):

    return int((memory["used_ram"] * 100) / memory["available_ram"])


class DeviceMonitorTask:
    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            log_console(f"{self.__class__.__name__}: monitor:device Terminate pending")

    def monitor(self, interval):

        while True and not self.terminate:

            # We get device IDs every time through, so that we can then re-retrieve the device object.
            # The reason for this is because other entities may have changed device (e.g. SDWAN heartbeats)
            device_ids = get_all_device_ids()
            log_console(f"Monitor: Beginning monitoring for {len(device_ids)} devices")

            for device_id in device_ids:

                result, device = get_device(
                    device_id=device_id
                )  # re-retrieve device as it may have been changed

                if result != "success":
                    log_console(
                        f"Device Monitor: Error retrieving device from DB. id: {device_id}, error: {device}"
                    )
                    continue

                if device["transport"] == "HTTP-REST":
                    if not device["last_heard"]:
                        continue

                    last_heard_time = datetime.strptime(
                        device["last_heard"], "%Y-%m-%d %H:%M:%S.%f"
                    )
                    print(f"now: {datetime.now()}, last_heard: {last_heard_time}")
                    if (datetime.now() - last_heard_time) > timedelta(
                        seconds=MAX_NOT_HEARD_SECONDS
                    ):
                        device["availability"] = False
                        record_device_status(device)
                        set_device(device)

                    continue  # HTTP-REST devices (e.g. sdwan) communicate to us, we don't poll them

                try:
                    ip_address = socket.gethostbyname(device["hostname"])
                except (socket.error, socket.gaierror) as e:
                    info = (
                        f"!!! Caught socket error {repr(e)}, continuing to next device"
                    )
                    log_console(info)
                    log_event(
                        str(datetime.now())[:-3],
                        "device",
                        device["name"],
                        "SEVERE",
                        info,
                    )
                    ip_address = None

                if self.terminate:
                    break

                log_console(f"--- monitor:device get environment {device['name']}")
                device_status = get_device_status(device)

                device["ip_address"] = ip_address
                device["availability"] = device_status["availability"]
                device["response_time"] = device_status["response_time"]
                device["cpu"] = device_status["cpu"]
                device["memory"] = device_status["memory"]

                if device_status["last_heard"]:
                    device["last_heard"] = device_status["last_heard"]

                record_device_status(device)
                set_device(device)

            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break

        log_console("...gracefully exiting monitor:device")
