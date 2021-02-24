import napalm
from quokka.models.apis.device_model_apis import get_facts, set_facts
from quokka.controller.utils import log_console
from ncclient import manager
# the following comment/lines are to workaround a PyCharm bug
# noinspection PyUnresolvedReferences
from xml.dom.minidom import parseString


def get_napalm_device(device):

    if device["os"] == "ios" or device["os"] == "iosxe":
        driver = napalm.get_network_driver("ios")
    elif device["os"] == "nxos-ssh":
        driver = napalm.get_network_driver("nxos_ssh")
    elif device["os"] == "nxos":
        driver = napalm.get_network_driver("nxos")
    else:
        return "failed", "Unsupported OS"

    if device["os"] in {"ios", "iosxe", "nxos-ssh"}:
        napalm_device = driver(
            hostname=device["hostname"],
            username=device["username"],
            password=device["password"],
            optional_args={"port": device["ssh_port"]},
        )
    else:
        napalm_device = driver(
            hostname=device["hostname"],
            username=device["username"],
            password=device["password"],
        )

    return napalm_device


def get_device_info(device, requested_info, get_live_info=False):

    if device["transport"] == "napalm":
        return get_device_info_napalm(device, requested_info, get_live_info)
    elif device["transport"] == "ncclient":
        # log_console(f"Getting device info via ncclient for {device['name']}")
        return get_device_info_ncclient(device, requested_info, get_live_info)
    elif device["transport"] == "HTTP-REST" and requested_info == "facts":
        # HTTP-REST devices will update device information with their heartbeats, no need to fetch it
        facts = {
            "fqdn": device["hostname"],
            "hostname": device["hostname"],
            "os_version": device["version"],
            "serial_number": device["serial"],
            "uptime": device["uptime"],
            "vendor": device["vendor"]
        }
        return "success", {"facts": facts}

    else:
        return "failure", "Unable to retrieve requested info from device"


def get_device_info_napalm(device, requested_info, get_live_info=False):

    # Try to get the info from the DB first
    if requested_info == "facts" and not get_live_info:
        result, facts = get_facts(device["name"])
        if result == "success":
            return "success", {"facts": facts}

    napalm_device = get_napalm_device(device)

    try:
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

    except BaseException as e:
        log_console(f"!!! Exception in get device info: {repr(e)}")
        return "failure", repr(e)


def get_device_info_ncclient(device, requested_info, get_live_info=False):

    # Try to get the info from the DB first
    if requested_info == "facts" and not get_live_info:
        result, facts = get_facts(device["name"])
        if result == "success":
            return "success", {"facts": facts}

    nc_connection = manager.connect(
        host=device["hostname"],
        port=device["netconf_port"],
        username=device["username"],
        password=device["password"],
        device_params={"name": device["ncclient_name"]},
        hostkey_verify=False,
    )

    config = nc_connection.get_config("running")

    if requested_info == "config":
        return "success", {"config": {"running": config.xml}}

    elif requested_info == "facts":
        facts = {"vendor": device["vendor"],
                 "os_version": None,
                 "hostname": None,
                 "fqdn": None,
                 "serial_number": None
                 }

        xml_doc = parseString(str(config))

        version = xml_doc.getElementsByTagName("version")
        hostname = xml_doc.getElementsByTagName("hostname")

        if len(version) > 0:
            facts["os_version"] = version[0].firstChild.nodeValue
        if len(hostname) > 0:
            facts["hostname"] = hostname[0].firstChild.nodeValue
            facts["fqdn"] = hostname[0].firstChild.nodeValue

        serial_number = """
            <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
            <serial/>
            </System>
            """
        rsp = nc_connection.get(("subtree", serial_number))
        xml_doc = parseString(str(rsp))

        nc_connection.close_session()
        return "success", {"facts": facts}

    else:
        if nc_connection:
            nc_connection.close_session()
        return "failure", "unsupported requested info"
