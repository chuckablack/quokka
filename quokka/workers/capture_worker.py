# ---- Worker application to capture packets --------------------------------

import pika
import json
from CaptureThread import CaptureThread
import scapy.all as scapy
from datetime import datetime

from util import get_packets_from_capture, send_capture, get_filter

quokka_ip = "localhost"
serial_no = "111.111.111"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='capture_queue', durable=True)
print('\n\n [*] Capture Worker: waiting for messages.')


def receive_capture_request(capture_channel, method, properties, body):

    print(f"capture worker: received message")
    capture_info = json.loads(body)
    print(f"capture info: {capture_info}")

    channel.basic_ack(delivery_tag=method.delivery_tag)

    capture_thread = CaptureThread(quokka_ip, serial_no, capture_info)
    capture_thread.start()

    # interface = capture_info["interface"]
    # capture_filter = get_filter(capture_info["ip"], capture_info["protocol"], capture_info["port"])
    # count = int(capture_info["count"])
    #
    # if count < 1 or count > 1000:
    #     count = 100
    #
    # print(f"capture worker: begin scapy sniff on interface: {interface} for filter: {capture_filter}")
    #
    # # capture = scapy.sniff(iface=interface, filter=capture_filter, count=count)
    # capture = scapy.sniff(iface=interface, filter=capture_filter, count=10, timeout=100)
    #
    # packets = get_packets_from_capture(capture)
    # send_capture(quokka_ip, serial_no, str(datetime.now())[:-1], packets)

    print('\n\n [*] Capture Worker: waiting for messages.')


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=receive_capture_request, queue='capture_queue')

try:
    channel.start_consuming()

except KeyboardInterrupt as e:
    print("\nCapture worker shutting down")
    connection.close()
