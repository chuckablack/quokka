import pika
import json
import yaml
from netaddr import IPNetwork
from quokka.controller.utils import log_console


class PortscanManager:

    try:
        with open("quokka/data/" + "portscanmonitors.yaml", "r") as import_file:
            portscan_monitors = yaml.safe_load(import_file.read())
    except FileNotFoundError as e:
        log_console(f"Could not import portscan monitors file: {repr(e)}")
        portscan_monitors["0.0.0.0/0"] = "localhost"

    @staticmethod
    def get_channel(monitor):

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=monitor))
        channel = connection.channel()
        channel.queue_declare(queue="portscan_queue", durable=True)

        return channel

    @staticmethod
    def find_monitor(ip=None):

        if not ip:
            return "localhost"

        if ip in PortscanManager.portscan_monitors:
            return PortscanManager.portscan_monitors[ip]

        # If not a per-IP monitor, get the subnet for this IP and find match
        for network, monitor in PortscanManager.portscan_monitors.items():
            if ip in IPNetwork(network):
                return PortscanManager.portscan_monitors[network]

        else:
            # If we didn't find a specific monitor, default to localhost
            return "localhost"

    @staticmethod
    def initiate_portscan(host_ip, host_name, token):

        monitor = PortscanManager.find_monitor(host_ip)
        channel = PortscanManager.get_channel(monitor)

        portscan_info = {
            "host_ip": host_ip,
            "host_name": host_name,
            "token": token,
        }

        portscan_info_json = json.dumps(portscan_info)
        channel.basic_publish(
            exchange="", routing_key="portscan_queue", body=portscan_info_json
        )

        log_console(
            f"Portscan Manager: starting portscan: host_ip   : {host_ip}"
            f"Portscan Manager: starting portscan: host_name : {host_name}"
        )
