import pika
import json
import yaml
from netaddr import IPNetwork
from quokka.controller.utils import log_console, get_this_ip
from quokka.models.apis.worker_data_apis import set_command
from quokka.models.apis.worker_model_apis import get_worker

interface = "enp0s3"


class CaptureManager:

    try:
        with open("quokka/data/" + "capturemonitors.yaml", "r") as import_file:
            capture_monitors = yaml.safe_load(import_file.read())
    except FileNotFoundError as e:
        log_console(f"Could not import capture monitors file: {repr(e)}")
        capture_monitors["0.0.0.0/0"] = "localhost"

    worker_type = "capture"

    @staticmethod
    def get_channel(monitor):

        credentials = pika.PlainCredentials("quokkaUser", "quokkaPass")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=monitor, credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue="capture_queue", durable=True)

        return channel

    @staticmethod
    def translate_protocol_and_port(protocol, port):

        # Take common protocol terms and translate into tcpdump protocol/port combinations
        if protocol.lower() == "dns":
            return "udp", "53"
        elif protocol.lower() == "https":
            return "tcp", "443"
        elif protocol.lower() == "http":
            return "tcp", "80"
        elif protocol.lower() == "ntp":
            return "udp", "123"

        else:
            return protocol, port

    @staticmethod
    def find_monitor(ip=None):

        if ip:

            if ip in CaptureManager.capture_monitors:
                return CaptureManager.capture_monitors[ip]

            # If not a per-IP monitor, get the subnet for this IP and find match
            for network, monitor in CaptureManager.capture_monitors.items():
                if ip in IPNetwork(network):
                    return CaptureManager.capture_monitors[network]

        if "0.0.0.0/0" in CaptureManager.capture_monitors:
            return CaptureManager.capture_monitors["0.0.0.0/0"]

        # If we didn't find a specific monitor, default to localhost
        return "localhost"

    @staticmethod
    def initiate_capture(ip, protocol, port, count):

        monitor = CaptureManager.find_monitor(ip)
        worker = get_worker(host=monitor, worker_type=CaptureManager.worker_type)
        if worker is None:
            log_console(
                f"Capture Manager: could not find worker, host={monitor}, worker_type={CaptureManager.worker_type} in DB"
            )
            return

        if (
            protocol
        ):  # Translate port and protocol if necessary, e.g. 'http' must become 'tcp', '80'
            protocol, port = CaptureManager.translate_protocol_and_port(protocol, port)

        capture_info = {
            "quokka": get_this_ip(),
            "interface": interface,
            "ip": ip,
            "protocol": protocol,
            "port": port,
            "count": count,
        }
        capture_info_json = json.dumps(capture_info)

        if worker["connection_type"] == "rabbitmq":

            channel = CaptureManager.get_channel(monitor)
            channel.basic_publish(exchange="", routing_key="capture_queue", body=capture_info_json)

            log_console(
                f"Capture Manager: starting capture: ip:{ip} protocol:{protocol} port:{port} count:{count}"
            )

        elif worker["connection_type"] == "http":

            command = dict()
            command["host"] = worker["host"]
            command["serial"] = worker["serial"]
            command["worker_type"] = CaptureManager.worker_type
            command["command"] = "start-capture"
            command["command_info"] = capture_info_json
            command["delivered"] = False

            set_command(command)
