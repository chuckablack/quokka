import subprocess
from datetime import datetime

from time import sleep

from quokka.models.apis import get_all_hosts
from quokka.models.apis import set_host

stop_thread = False


def monitor(interval):

    while True and not stop_thread:

        hosts = get_all_hosts()
        print(f"Beginning monitoring for {len(hosts)} hosts")
        for host in hosts:

            if stop_thread:
                break

            active = subprocess.call(["ping", "-c1", "-n", "-i0.5", "-W2", str(host["ip_address"])])
            if active == 0:
                host["availability"] = True
                host["response_time"] = 1.0
                host["last_heard"] = str(datetime.now())

            else:
                host["availability"] = False

            set_host(host)

        sleep(interval)

    print("gracefully exiting monitor")
