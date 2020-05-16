import napalm
from quokka.models import get_device


def get_device_info(device_name, requested_info):

    result, info = get_device(device_name=device_name)
    if result == "failed":
        return result, info

    device = info
    if device["os"] == "ios" or device["os"] == "iosxe":
        driver = napalm.get_network_driver("ios")
    else:
        return "failed", "Unsupported OS"

    napalm_device = driver(
        hostname=device["ssh_hostname"],
        username=device["ssh_username"],
        password=device["ssh_password"],
        optional_args={"port": device["ssh_port"]},
    )

    napalm_device.open()

    if requested_info == "facts":
        return "success", {"facts": napalm_device.get_facts()}
    elif requested_info == "interfaces":
        return "success", {"interfaces": napalm_device.get_interfaces()}
    elif requested_info == "arp":
        return "success", {"arp": napalm_device.get_arp_table()}
    elif requested_info == "mac":
        return "success", {"mac": napalm_device.get_mac_address_table()}
    elif requested_info == "config":
        return "success", {"config": napalm_device.get_config()}

    else:
        return "failure", "Unknown requested info"
