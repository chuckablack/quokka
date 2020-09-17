import pika
import nmap
import pprint
import json

portscan_queue = "portscan-queue"


def on_portscan_request(ch, method_frame, properties, host_ip):

    ip = host_ip.decode("utf-8")
    print(f"portscan worker: received request for host: {ip}")

    nm = nmap.PortScanner()
    scan_output = nm.scan(ip, '22-1024', arguments="-sS -sU -O --host-time 300")

    scan_output_str = pprint.pformat(scan_output, indent=4)
    scan_results = {"result": "success",
                    "output": scan_output_str}

    print(f"result: {scan_results['result']}")
    print(scan_output_str)

    ch.basic_publish("", routing_key=properties.reply_to, body=json.dumps(scan_results))
    print("\nportscan worker: waiting for requests")


with pika.BlockingConnection() as conn:

    channel = conn.channel()
    channel.queue_declare(queue=portscan_queue,
                          exclusive=True,
                          auto_delete=True)

    print("\nportscan worker: waiting for requests")
    channel.basic_consume(portscan_queue, on_portscan_request)

    try:
        channel.start_consuming()

    except KeyboardInterrupt as e:
        print("\nPortscan worker shutting down")
        conn.close()
