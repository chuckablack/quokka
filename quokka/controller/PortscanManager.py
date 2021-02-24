import pika
import json
import yaml
from netaddr import IPNetwork
from quokka.controller.utils import log_console, get_this_ip
from quokka.models.apis.worker_data_apis import set_command
from quokka.models.apis.worker_model_apis import get_worker


class PortscanManager:

    try:
        with open("quokka/data/" + "portscanmonitors.yaml", "r") as import_file:
            portscan_monitors = yaml.safe_load(import_file.read())
    except FileNotFoundError as e:
        log_console(f"Could not import portscan monitors file: {repr(e)}")
        portscan_monitors["0.0.0.0/0"] = "localhost"

    worker_type = "portscan"

    @staticmethod
    def get_channel(monitor):

        credentials = pika.PlainCredentials('quokkaUser', 'quokkaPass')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=monitor, credentials=credentials))
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

        if "0.0.0.0/0" in PortscanManager.portscan_monitors:
            return PortscanManager.portscan_monitors["0.0.0.0/0"]

        # If we didn't find a specific monitor, default to localhost
        return "localhost"

    @staticmethod
    def initiate_portscan(host_ip, host_name, token):

        monitor = PortscanManager.find_monitor(host_ip)
        worker = get_worker(host=monitor, worker_type=PortscanManager.worker_type)
        if worker is None:
            log_console(
                f"Portscan Manager: could not find worker, host={monitor}, worker_type={PortscanManager.worker_type} in DB"
            )
            return

        portscan_info = {
            "quokka": get_this_ip(),
            "host_ip": host_ip,
            "host_name": host_name,
            "token": token,
        }
        portscan_info_json = json.dumps(portscan_info)

        if worker["connection_type"] == "rabbitmq":

            channel = PortscanManager.get_channel(monitor)

            channel.basic_publish(
                exchange="", routing_key="portscan_queue", body=portscan_info_json
            )

            log_console(
                f"Portscan Manager: starting portscan: host_ip   : {host_ip}"
                f"Portscan Manager: starting portscan: host_name : {host_name}"
            )

        elif worker["connection_type"] == "http":

            command = dict()
            command["host"] = worker["host"]
            command["serial"] = worker["serial"]
            command["worker_type"] = PortscanManager.worker_type
            command["command"] = "start-capture"
            command["command_info"] = portscan_info_json
            command["delivered"] = False

            set_command(command)
