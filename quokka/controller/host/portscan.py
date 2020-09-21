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


def on_portscan_worker_reply(ch, method_frame, properties, portscan_results_str):

    log_console(f"portscan: received reply: {portscan_results_str}")
    portscan_results = json.loads(portscan_results_str)

    ch.close()
