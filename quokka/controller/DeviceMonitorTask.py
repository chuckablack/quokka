import socket
from datetime import datetime
import time

from time import sleep

from quokka.controller.device_info import get_device_info
from quokka.models.apis import get_all_devices
from quokka.models.apis import set_device


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
        self.terminate = True
        print(self.__class__.__name__, "monitor:device Terminate pending")

    def monitor(self, interval):

        while True and not self.terminate:

            devices = get_all_devices()
            print(f"Monitor: Beginning monitoring for {len(devices)} devices")
            for device in devices:

                try:
                    ip_address = socket.gethostbyname(device["ssh_hostname"])
                except (socket.error, socket.gaierror) as e:
                    print(f"!!! Caught socket error {repr(e)}, continuing to next device")
                    ip_address = None

                if self.terminate:
                    break

                print(f"--- monitor:device get environment {device['name']}")
                time_start = time.time()
                try:
                    result, env = get_device_info(device["name"], "environment")
                except BaseException as e:
                    print(f"!!! Exception in monitoring device: {repr(e)}")
                    continue

                response_time = time.time() - time_start

                if result != "success":
                    device["availability"] = False

                else:
                    if ip_address:
                        device["ip_address"] = ip_address

                    device["availability"] = True
                    device["response_time"] = int(response_time*1000)
                    device["last_heard"] = str(datetime.now())[:-3]

                    device["cpu"] = calculate_cpu(env["environment"]["cpu"])
                    device["memory"] = calculate_memory(env["environment"]["memory"])

                set_device(device)

            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break

        print("...gracefully exiting monitor:device")
