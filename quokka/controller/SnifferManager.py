import pika
import json
from quokka.controller.utils import log_console


class SnifferManager:

    log_console("Initializing SnifferManager")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='host_sniffer_queue', durable=True)
    channel.queue_declare(queue='device_sniffer_queue', durable=True)
    channel.queue_declare(queue='service_sniffer_queue', durable=True)

    @staticmethod
    def close():
        SnifferManager.connection.close()

    @staticmethod
    def sniff_host(interface, ip, count):

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='host_sniffer_queue', durable=True)

        sniff_host_info = {"interface": interface,
                           "ip": ip,
                           "count": count}

        sniff_host_info_json = json.dumps(sniff_host_info)
        channel.basic_publish(exchange='',
                              routing_key='host_sniffer_queue',
                              body=sniff_host_info_json)

        log_console(f"Sniffer Manager: starting sniffing for {ip} on interface {interface} with count {count}")


