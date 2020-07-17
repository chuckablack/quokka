from datetime import datetime
from time import sleep

from quokka.controller.device.device_info import get_device_info
from quokka.controller.device.device_status import get_device_status
from quokka.controller.device.config_diff import config_diff
from quokka.models.Compliance import Compliance
from quokka.models.apis import get_all_devices
from quokka.models.apis import set_device
from quokka.controller.utils import log_console


def check_os_compliance(device):

    standard = Compliance.query.filter_by(**{"vendor": device["vendor"], "os": device["os"]}).one_or_none()
    if standard is None:
        log_console(f"!!! Error retrieving compliance record for this device {device['name']}")
        return False

    try:
        result, facts = get_device_info(device, "facts", get_live_info=True)
    except BaseException as e:
        log_console(f"!!! Exception getting device info in compliance monitoring for {device['name']}")
        result = "failed"

    if result == "success":
        if standard.standard_version == facts["facts"]["os_version"]:
            return True
        else:
            return False  # Just a normal incorrect version
    else:
        log_console(f"!!! Error retrieving version info for this device {device['name']}")
        return False


def check_config_compliance(device):

    standard = Compliance.query.filter_by(**{"vendor": device["vendor"], "os": device["os"]}).one_or_none()
    if standard is None:
        log_console(f"!!! Error retrieving compliance record for this device {device['name']}")
        return False

    standard_filename = "quokka/data/" + standard.standard_config_file
    result, diff = config_diff(device, standard_filename)

    if result != "success":
        return False
    if len(diff) > 0:
        with open(standard_filename + ".diff." + device["name"], "w") as config_out:
            config_out.write(diff)
        return False

    return True


class ComplianceMonitorTask:

    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            log_console(f"{self.__class__.__name__}: monitor:compliance Terminate pending")

    def monitor(self, interval):

        while True and not self.terminate:

            devices = get_all_devices()
            log_console(f"Monitor: Beginning compliance monitoring for {len(devices)} devices")
            for device in devices:

                if self.terminate:
                    break

                device["availability"] = get_device_status(device)["availability"]
                if device["availability"]:
                    device["os_compliance"] = check_os_compliance(device)
                    device["config_compliance"] = check_config_compliance(device)
                    device["last_compliance_check"] = str(datetime.now())[:-3]

                set_device(device)

            for _ in range(0, int(interval / 10)):
                sleep(10)
                if self.terminate:
                    break

        log_console("...gracefully exiting monitor:compliance")
