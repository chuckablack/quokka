import time
from datetime import datetime, timedelta

from quokka.controller.utils import log_console
from quokka.models.apis.worker_model_apis import get_all_workers, set_worker, record_worker_status

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

                if not worker["last_heard"]:
                    continue

                last_heard_time = datetime.strptime(worker["last_heard"], "%Y-%m-%d %H:%M:%S.%f")
                print(f"now: {datetime.now()}, last_heard: {last_heard_time}")
                if (datetime.now() - last_heard_time) > timedelta(seconds=MAX_NOT_HEARD_SECONDS):
                    worker["availability"] = False
                    record_worker_status(worker)
                    set_worker(worker)

            for _ in range(0, int(interval / 10)):
                time.sleep(10)
                if self.terminate:
                    break

        log_console("...gracefully exiting monitor:worker")
