# ---- Worker application to sniff host packets --------------------------------

import pika
import json
import scapy.all as scapy
from datetime import datetime

from util import get_packets_from_capture, send_capture

quokka_ip = "localhost"
serial_no = "111.111.111"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='host_sniffer_queue', durable=True)
print(' [*] Host Sniffer Worker: waiting for messages.')


def receive_sniff_host_request(host_sniffer_channel, method, properties, body):

    print(f"sniffing host: received message")
    sniff_host_info = json.loads(body)
    print(f"sniffing host info: {sniff_host_info}")

    channel.basic_ack(delivery_tag=method.delivery_tag)

    if (
        "interface" not in sniff_host_info
        or "ip" not in sniff_host_info
        or "count" not in sniff_host_info
        or not sniff_host_info["count"].isnumeric()
    ):
        print("received invalid or missing sniff_host_info")
        return

    interface = sniff_host_info["interface"]
    host_filter = "host " + sniff_host_info["ip"]
    count = int(sniff_host_info["count"])

    if count < 1 or count > 1000:
        count = 100

    print(f"sniffer: begin scapy sniff on interface: {interface} for filter: {host_filter}")

    capture = scapy.sniff(iface=interface, filter=host_filter, count=count)

    packets = get_packets_from_capture(capture)
    send_capture(quokka_ip, serial_no, str(datetime.now())[:-1], packets)

    print('\n\n [*] Host Sniffer Worker: waiting for messages.')


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=receive_sniff_host_request, queue='host_sniffer_queue')

try:
    channel.start_consuming()

except KeyboardInterrupt as e:
    print("\nHost sniffer shutting down")
    connection.close()
