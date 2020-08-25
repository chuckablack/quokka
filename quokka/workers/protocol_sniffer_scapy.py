# ---- Worker application to sniff protocol packets --------------------------------

import pika
import json
import scapy.all as scapy
from datetime import datetime

from util import get_packets_from_capture, send_capture

quokka_ip = "localhost"
serial_no = "111.111.111"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='protocol_sniffer_queue', durable=True)
print(' [*] Protocol Sniffer Worker: waiting for messages.')


def receive_sniff_protocol_request(protocol_sniffer_channel, method, properties, body):

    print(f"sniffing protocol: received message")
    sniff_protocol_info = json.loads(body)
    print(f"sniffing protocol info: {sniff_protocol_info}")

    if (
        "interface" not in sniff_protocol_info
        or "protocol" not in sniff_protocol_info
        or "count" not in sniff_protocol_info
        or not sniff_protocol_info["count"].isnumeric()
    ):
        channel.basic_nack(requeue=False)
        return

    interface = sniff_protocol_info["interface"]
    protocol_filter = sniff_protocol_info["protocol"]
    if "port" in sniff_protocol_info and sniff_protocol_info["port"]:
        protocol_filter += " port " + sniff_protocol_info["port"]
    count = int(sniff_protocol_info["count"])

    if count < 1 or count > 1000:
        count = 100

    print(f"sniffer: begin scapy sniff on interface: {interface} for filter: {protocol_filter}")

    capture = scapy.sniff(iface=interface, filter=protocol_filter, count=count)

    packets = get_packets_from_capture(capture)
    send_capture(quokka_ip, serial_no, str(datetime.now())[:-1], packets)

    channel.basic_ack(delivery_tag=method.delivery_tag)
    print('\n\n [*] Protocol Sniffer Worker: waiting for messages.')


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=receive_sniff_protocol_request, queue='protocol_sniffer_queue')

try:
    channel.start_consuming()

except KeyboardInterrupt as e:
    print("\nProtocol sniffer shutting down")
    connection.close()
