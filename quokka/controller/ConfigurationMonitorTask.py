from time import sleep
from datetime import datetime

from quokka.controller.utils import log_console
from quokka.controller.device.device_info import get_device_info
from quokka.models.apis.device_model_apis import (
    get_all_device_ids,
    get_device,
    record_device_config,
)
from quokka.models.apis.event_model_apis import log_event


class ConfigurationMonitorTask:
    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            log_console(
                f"{self.__class__.__name__}: monitor:Configuration Terminate pending"
            )

    def monitor(self, interval):

        while True and not self.terminate:

            device_ids = get_all_device_ids()
            log_console(
                f"Monitor: Beginning Configuration monitoring for {len(device_ids)} devices"
            )

            for device_id in device_ids:

                if self.terminate:
                    break

                result, device = get_device(
                    device_id=device_id
                )  # re-retrieve device as it may have been changed

                if result != "success":
                    log_console(
                        f"Configuration Monitor: Error retrieving device from DB. id: {device_id}, error: {device}"
                    )
                    continue

                try:
                    result, config = get_device_info(
                        device, "config", get_live_info=True
                    )
                    if result != "success":
                        log_console(
                            f"!!! Unable to get device info (config) for {device['name']}"
                        )
                        continue

                except BaseException as e:
                    log_console(
                        f"!!! Exception getting device info in configuration monitoring for {device['name']}: {repr(e)}"
                    )
                    continue

                # If we made it here, we got the configuration, so store it in the DB
                record_device_config(device_id, config["config"]["running"])
                log_event(
                    str(datetime.now())[:-3],
                    "configuration",
                    device['name'],
                    "INFO",
                    f"Stored configuration for: {device['name']}",
                )

            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break

        log_console("...gracefully exiting monitor:configuration")
