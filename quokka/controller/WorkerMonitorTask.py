import subprocess
from datetime import datetime, timedelta

import time

from quokka.controller.utils import get_response_time
from quokka.models.apis import get_all_workers, set_worker, record_worker_status, log_event
from quokka.controller.utils import log_console

MAX_NOT_HEARD_SECONDS = 90  # For http workers, time to have not seen a heartbeat


class WorkerMonitorTask:
    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            log_console(f"{self.__class__.__name__}: monitor:worker Terminate pending")

    def monitor(self, interval):

        while True and not self.terminate:

            workers = get_all_workers()
            log_console(f"monitor:worker Beginning monitoring for {len(workers)} workers")
            for worker in workers:

                if self.terminate:
                    break

                if worker["connection_type"] == "rabbitmq":

                    log_console(f"--- monitor:worker pinging {worker['host']}")
                    try:
                        ping_output = subprocess.check_output(
                            ["ping", "-c3", "-n", "-i0.5", "-W2", str(worker["host"])]
                        )
                        worker["availability"] = True
                        worker["response_time"] = get_response_time(str(ping_output))
                        worker["last_heard"] = str(datetime.now())[:-3]

                    except subprocess.CalledProcessError:
                        worker["availability"] = False
                        log_event(
                            str(datetime.now())[:-3],
                            "worker monitor",
                            worker["host"],
                            "INFO",
                            f"Availability failed for worker: {worker['host']}",
                        )

                elif worker["connection_type"] == "http":

                    if not worker["last_heard"]:
                        continue

                    last_heard_time = datetime.strptime(worker["last_heard"], "%Y-%m-%d %H:%M:%S.%f")
                    print(f"now: {datetime.now()}, last_heard: {last_heard_time}")
                    if (datetime.now() - last_heard_time) > timedelta(seconds=MAX_NOT_HEARD_SECONDS):
                        worker["availability"] = False
                        record_worker_status(worker)
                        set_worker(worker)

                    continue  # HTTP-REST devices (e.g. sdwan) communicate to us, we don't poll them

                record_worker_status(worker)
                set_worker(worker)

            for _ in range(0, int(interval / 10)):
                time.sleep(10)
                if self.terminate:
                    break

        log_console("...gracefully exiting monitor:worker")
