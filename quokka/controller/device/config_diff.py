import napalm
from quokka.models.apis import get_device, get_facts, set_facts
from quokka.controller.utils import log_console


def config_diff(device, config_to_diff):

    if device["os"] == "ios" or device["os"] == "iosxe":
        driver = napalm.get_network_driver("ios")
    elif device["os"] == "nxos":
        driver = napalm.get_network_driver("nxos_ssh")
    else:
        return "failed", "Unsupported OS"

    napalm_device = driver(
        hostname=device["ssh_hostname"],
        username=device["ssh_username"],
        password=device["ssh_password"],
        optional_args={"port": device["ssh_port"]},
    )

    try:
        napalm_device.open()

        napalm_device.load_merge_candidate(filename=config_to_diff)
        return "success", napalm_device.compare_config()

    except BaseException as e:
        log_console(f"!!! Exception in doing load_merge_candidate: {repr(e)}")
        return "failure", repr(e)

