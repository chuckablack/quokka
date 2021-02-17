import napalm
from quokka.controller.utils import log_console
from quokka.controller.device.device_info import get_napalm_device


def config_diff(device, config_to_diff):

    if device["transport"] == "napalm":

        napalm_device = get_napalm_device(device)

        try:
            napalm_device.open()

            napalm_device.load_replace_candidate(filename=config_to_diff)
            return "success", napalm_device.compare_config()

        except BaseException as e:
            log_console(f"!!! Exception in doing load_merge_candidate: {repr(e)}")
            return "failure", repr(e)

    else:
        log_console(f"!!! Unable to compare configurations, no live config to compare")
        return "failure", "Unable to compare configurations"

