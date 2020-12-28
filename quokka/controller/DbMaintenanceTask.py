from datetime import datetime, timedelta
import time

from quokka.controller.utils import log_console
from quokka.models.DeviceStatus import DeviceStatus
from quokka.models.HostStatus import HostStatus
from quokka.models.ServiceStatus import ServiceStatus
from quokka.models.WorkerStatus import WorkerStatus
from quokka.models.Capture import Capture
from quokka.models.Portscan import Portscan
from quokka.models.Traceroute import Traceroute
from quokka.models.Command import Command

from quokka import db


class DbMaintenanceTask:
    def __init__(self):
        self.terminate = False
        self.current_hour = str(datetime.now())[:-13]

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            log_console(f"{self.__class__.__name__}: Terminate pending")

    def start(self, interval):

        while True and not self.terminate:

            this_hour = str(datetime.now())[:-13]
            if this_hour == self.current_hour:
                time.sleep(60)
                continue

            # Get datetime for 24 hours ago
            now = datetime.now()
            now_minus_24_hours = now - timedelta(hours=24)
            now_minus_2_hours = now - timedelta(hours=2)

            try:

                # Clean up time-series data, which can be deleted after 24 hours
                for table in [DeviceStatus, HostStatus, ServiceStatus, WorkerStatus]:
                    count = table.query.filter(table.timestamp < str(now_minus_2_hours)).delete()
                    log_console(f"DbMaintenanceTask: deleted {count} records from {table}")

                # Clean up packet capture data, which we allow to hang around for 24 hours
                for table in [Capture, Portscan, Traceroute]:
                    count = table.query.filter(table.timestamp < str(now_minus_24_hours)).delete()
                    log_console(f"DbMaintenanceTask: deleted {count} records from {table}")

                # Clean up commands greater than 24 hours old
                count = Command.query.filter(Command.timestamp < str(now_minus_24_hours)).delete()
                log_console(f"DbMaintenanceTask: deleted {count} records from Command")

                db.session.commit()

            except BaseException as e:
                log_console(f"!!! uh-oh, exception in DbMaintenance thread: {e}")

            self.current_hour = this_hour

        log_console("...gracefully exiting db maintenance task")
