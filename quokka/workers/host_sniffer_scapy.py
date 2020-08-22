# ---- Worker application to sniff host packets --------------------------------

import pika
import json
import scapy.all as scapy
from scapy2dict import to_dict
from pprint import pprint
import requests
from datetime import datetime

quokka_ip = "localhost"

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
        or "count" not in sniff_host_info
        or not sniff_host_info["count"].isnumeric()
    ):
        channel.basic_nack(requeue=False)
        return

    interface = sniff_host_info["interface"]
    host_filter = "host " + sniff_host_info["ip"]
    count = int(sniff_host_info["count"])

    if count < 1 or count > 1000:
        count = 100

    print(f"sniffer: begin scapy sniff on interface: {interface} for filter: {host_filter}")

    capture = scapy.sniff(iface=interface, filter=host_filter, count=count)

    packets = list()
    for packet in capture:
        # print(f"---- sniffing host: packet sniffed: {packet.show()}")
        packet_dict = to_dict(packet, strict=True)
        if "Raw" in packet_dict:
            del packet_dict["Raw"]
        packets.append(packet_dict)

    print("\n---- Summaries --------------------")
    print(capture.nsummary())
    pprint(packets)

    capture_payload = {"name": "host_sniffer_1",
                       "serial": "1",
                       "packets": packets}
    rsp = requests.post(
        "http://" + quokka_ip + ":5000/capture/store", json=capture_payload
    )
    if rsp.status_code != 200:
        print(
            f"{str(datetime.now())[:-3]}: Error calling /capture/store response: {rsp.status_code}, {rsp.json()}"
        )

    channel.basic_ack(delivery_tag=method.delivery_tag)
    print('\n\n [*] Host Sniffer Worker: waiting for messages.')


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=receive_sniff_host_request, queue='host_sniffer_queue')

try:
    channel.start_consuming()

except KeyboardInterrupt as e:
    print("\nHost sniffer shutting down")
    connection.close()
