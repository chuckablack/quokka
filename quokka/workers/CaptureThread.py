from scapy.all import sniff, hexdump, conf, get_if_list, get_if_addr
from threading import Thread
from util import get_filter
from scapy2dict import to_dict
from pprint import pprint
from datetime import datetime

from util import bytes_to_string, send_capture


class CaptureThread(Thread):
    def __init__(self, quokka_ip, serial_no, capture_info):

        super().__init__()

        print(
            f"CaptureThread: initializing thread object: quokka_ip={quokka_ip}, serial={serial_no}, capture info={capture_info}"
        )
        self.interface = CaptureThread.get_interface(capture_info["ip"])
        if not self.interface:
            self.interface = capture_info["interface"]

        self.capture_filter = get_filter(
            capture_info["ip"], capture_info["protocol"], capture_info["port"]
        )
        print(f"CaptureThread: listening on interface: {self.interface}, filter: {self.capture_filter}")

        self.quokka_ip = quokka_ip
        self.serial_no = serial_no

    @staticmethod
    def get_interface(ip):

        route = conf.route.route(ip)
        if route:
            return route[0]

        else:
            if_list = get_if_list()
            for interface in if_list:
                ip = get_if_addr(interface)
                if ip and ip != "127.0.0.1":
                    return interface

        return None

    def process_packet(self, packet):

        print(f"CaptureThread: processing packet: {packet}")
        packet_dict = to_dict(packet, strict=True)
        if "Raw" in packet_dict:
            del packet_dict["Raw"]
        packet_dict["hexdump"] = hexdump(packet, dump=True)
        packet_dict_no_bytes = bytes_to_string(packet_dict)

        pprint(packet_dict_no_bytes)

        print(f"CaptureThread: sending capture: {packet_dict_no_bytes}")
        status_code = send_capture(
            self.quokka_ip,
            self.serial_no,
            str(datetime.now())[:-1],
            [packet_dict_no_bytes],
        )
        print(f"CaptureThread: capture sent, result={status_code}\n")

    def run(self):

        print(
            f"CaptureThread: starting capture: iface={self.interface}, filter={self.capture_filter}"
        )
        sniff(
            iface=self.interface,
            filter=self.capture_filter,
            timeout=180,
            prn=self.process_packet,
        )

        print(f"\n\n-----> CaptureThread: competed capture")
