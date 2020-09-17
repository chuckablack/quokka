from threading import Thread
from pprint import pprint
from datetime import datetime
import nmap
from socket import gethostname

from util import send_portscan


class PortscanThread(Thread):

    def __init__(self, quokka_ip, serial_no, scan_info):
        super().__init__()
        print(
            f"PortscanThread: initializing thread object: scan_info={scan_info}"
        )

        if "port_range" not in scan_info or "scan_arguments" not in scan_info or "host_ip" not in scan_info:
            print(f"PortscanThread: missing information in scan_info: {scan_info}")
            return

        self.quokka_ip = quokka_ip
        self.serial_no = serial_no
        self.host_ip = scan_info["host_ip"]
        self.host_name = scan_info["host_name"]
        self.port_range = scan_info["port_range"]
        self.scan_arguments = scan_info["scan_arguments"]

    def process_scan(self, scan_output):

        print(f"PortscanThread: sending portscan: {scan_output}")
        status_code = send_portscan(
            gethostname(), self.quokka_ip, self.serial_no, self.host_ip, self.host_name, str(datetime.now())[:-1], scan_output
        )
        print(f"PortscanThread: portscan sent, result={status_code}\n")

    def run(self):

        print(f"PortscanThread: starting portscan: host_ip   = {self.host_ip}")
        print(f"PortscanThread: starting portscan: host_name = {self.host_name}")
        print(f"PortscanThread: starting portscan: port_range= {self.port_range}")
        print(f"PortscanThread: starting portscan: arguments = {self.scan_arguments}")

        nm = nmap.PortScanner()
        scan_output = nm.scan(
            self.host_ip, self.port_range, arguments=self.scan_arguments
        )
        pprint(scan_output)
        self.process_scan(scan_output)

        print(f"\n\n-----> PortscanThread: competed portscan")
