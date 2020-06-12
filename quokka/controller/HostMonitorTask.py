import subprocess
from datetime import datetime

from time import sleep

from quokka.controller.utils import get_response_time
from quokka.models.apis import get_all_hosts, set_host, record_host_status


class HostMonitorTask:

    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        self.terminate = True
        print(self.__class__.__name__, "monitor:host Terminate pending")

    def monitor(self, interval):

        while True and not self.terminate:

            hosts = get_all_hosts()
            print(f"monitor:host Beginning monitoring for {len(hosts)} hosts")
            for host in hosts:

                if self.terminate:
                    break

                print(f"--- monitor:host pinging {host['ip_address']}")
                try:
                    ping_output = subprocess.check_output(
                        ["ping", "-c3", "-n", "-i0.5", "-W2", str(host["ip_address"])])
                    host["availability"] = True
                    host["response_time"] = get_response_time(str(ping_output))
                    host["last_heard"] = str(datetime.now())[:-3]

                except subprocess.CalledProcessError:
                    host["availability"] = False

                record_host_status(host)
                set_host(host)

            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break

        print("...gracefully exiting monitor:host")
