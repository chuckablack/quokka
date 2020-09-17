import nmap
import pika
import json
from quokka.controller.utils import log_console


def get_port_scan_tcp_connection(ip):

    nm = nmap.PortScanner()
    nm.scan(ip, '1-1024')

    try:
        nm[ip]
    except KeyError as e:
        return "failed", "nmap port scan failed"

    return "success", nm[ip].all_tcp()


def get_port_scan_extended(ip):

    log_console(f"portscan: sending request for scan: {ip}")
    portscan_queue = "portscan-queue"

    with pika.BlockingConnection() as conn:
        channel = conn.channel()

        channel.basic_consume('amq.rabbitmq.reply-to',
                              on_portscan_worker_reply,
                              auto_ack=True)
        channel.basic_publish(
            exchange='',
            routing_key=portscan_queue,
            body=ip,
            properties=pika.BasicProperties(reply_to='amq.rabbitmq.reply-to'))
        channel.start_consuming()

        return "success", "this is a bogus portscan result"


def on_portscan_worker_reply(ch, method_frame, properties, portscan_results_str):

    log_console(f"portscan: received reply: {portscan_results_str}")
    portscan_results = json.loads(portscan_results_str)

    ch.close()
