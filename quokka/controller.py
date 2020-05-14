import napalm
import json


def get_device_info(device_name, requested_info):
    return "success", f"device info {requested_info} from {device_name}"
