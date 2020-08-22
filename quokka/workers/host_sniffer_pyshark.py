# ---- Worker application to sniff host packets --------------------------------

import pika
import json
import pyshark
import time
from asyncio.exceptions import TimeoutError

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='host_sniffer_queue', durable=True)
print(' [*] Host Sniffer Worker: waiting for messages.')


def receive_sniff_host_request(host_sniffer_channel, method, properties, body):

    print(f"sniffing host: received message")
    sniff_host_info = json.loads(body)
    print(f"sniffing host info: {sniff_host_info}")

    if (
        "interface" not in sniff_host_info
        or "ip" not in sniff_host_info
        or "timeout" not in sniff_host_info
        or not sniff_host_info["timeout"].isnumeric()
    ):
        channel.basic_nack(requeue=False)
        return

    interface = sniff_host_info["interface"]
    host_filter = "host " + sniff_host_info["ip"]
    timeout = int(sniff_host_info["timeout"])
    print(f"sniffer: begin pyshark LiveCapture on interface: {interface} for filter: {host_filter}")

    capture = pyshark.LiveCapture(interface=interface, bpf_filter=host_filter, only_summaries=True)

    print("sniffing host: begin capture")
    start = time.time()
    try:
        capture.sniff(timeout=timeout)
    except TimeoutError as e:  # This is to catch a pyshark bug
        pass
    print("sniffing host: end capture")

    for packet in capture:
        print(f"---- sniffing host: packet sniffed: {packet}")

    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=receive_sniff_host_request, queue='host_sniffer_queue')

channel.start_consuming()
