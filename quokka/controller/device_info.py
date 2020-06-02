import napalm
from quokka.models.apis import get_device, get_facts, set_facts


def get_device_info(device_name, requested_info, get_live_info=False):

    result, info = get_device(device_name=device_name)
    if result == "failed":
        return result, info

    device = info

    # Try to get the info from the DB first
    if requested_info == "facts" and not get_live_info:
        result, facts = get_facts(device["name"])
        if result == "success":
            return "success", {"facts": facts}

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

    napalm_device.open()

    if requested_info == "facts":
        facts = napalm_device.get_facts()
        set_facts(device, {"facts": facts})
        return "success", {"facts": napalm_device.get_facts()}
    elif requested_info == "environment":
        return "success", {"environment": napalm_device.get_environment()}
    elif requested_info == "interfaces":
        return "success", {"interfaces": napalm_device.get_interfaces()}
    elif requested_info == "arp":
        return "success", {"arp": napalm_device.get_arp_table()}
    elif requested_info == "mac":
        return "success", {"mac": napalm_device.get_mac_address_table()}
    elif requested_info == "config":
        return "success", {"config": napalm_device.get_config()}
    elif requested_info == "counters":
        return "success", {"counters": napalm_device.get_interfaces_counters()}

    else:
        return "failure", "Unknown requested info"
