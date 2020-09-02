import pika
import json
from quokka.controller.utils import log_console

interface = "enp0s3"


class CaptureManager:

    log_console("Initializing CaptureManager")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="capture_queue", durable=True)

    @staticmethod
    def close():
        CaptureManager.connection.close()

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
    def initiate_capture(ip, protocol, port, count):

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()
        channel.queue_declare(queue="capture_queue", durable=True)

        if protocol:  # Translate port and protocol if necessary, e.g. 'http' must become 'tcp', '80'
            protocol, port = CaptureManager.translate_protocol_and_port(protocol, port)

        capture_info = {
            "interface": interface,
            "ip": ip,
            "protocol": protocol,
            "port": port,
            "count": count,
        }

        capture_info_json = json.dumps(capture_info)
        channel.basic_publish(
            exchange="", routing_key="capture_queue", body=capture_info_json
        )

        log_console(
            f"Capture Manager: starting capture: ip:{ip} protocol:{protocol} port:{port} count:{count}"
        )
