import subprocess
import re
from datetime import datetime

from time import sleep

from quokka.models.apis import get_all_hosts
from quokka.models.apis import set_host


def get_response_time(ping_output):

    m = re.search(r"time=([0-9]*)", ping_output)
    if m.group(1).isnumeric():
        return int(m.group(1))


class MonitorTask:

    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        self.terminate = True
        print(self.__class__.__name__, "Terminate pending")

    def monitor(self, interval):

        while True and not self.terminate:

            hosts = get_all_hosts()
            print(f"Monitor: Beginning monitoring for {len(hosts)} hosts")
            for host in hosts:

                if self.terminate:
                    break

                print(f"--- monitor pinging {host['ip_address']}")
                try:
                    ping_output = subprocess.check_output(
                        ["ping", "-c1", "-n", "-i0.5", "-W2", str(host["ip_address"])])
                    host["availability"] = True
                    host["response_time"] = get_response_time(str(ping_output))
                    host["last_heard"] = str(datetime.now())[:-3]

                except subprocess.CalledProcessError:
                    host["availability"] = False

                set_host(host)

            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break

        print("...gracefully exiting monitor")
