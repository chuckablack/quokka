import subprocess
import socket
from datetime import datetime
import time

from time import sleep

from quokka.controller.device_info import get_device_info
from quokka.models.apis import get_all_devices
from quokka.models.apis import set_device


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

                ip_address = socket.gethostbyname(device["ssh_hostname"])

                if self.terminate:
                    break

                print(f"--- monitor:device get environment {device['name']}")
                try:
                    time_start = time.time()
                    result, env = get_device_info(device["name"], "environment")
                    response_time = time.time() - time_start

                    if result != "success":
                        device["availability"] = False

                    else:
                        device["availability"] = True
                        device["response_time"] = int(response_time)
                        device["last_heard"] = str(datetime.now())[:-3]

                except subprocess.CalledProcessError:
                    device["availability"] = False

                set_device(device)

            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break

        print("...gracefully exiting monitor:device")
