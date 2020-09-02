from scapy.all import sniff, hexdump
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
        self.interface = capture_info["interface"]
        self.capture_filter = get_filter(
            capture_info["ip"], capture_info["protocol"], capture_info["port"]
        )
        self.quokka_ip = quokka_ip
        self.serial_no = serial_no

    def process_packet(self, packet):

        print(f"CaptureThread: processing packet: {packet}")
        packet_dict = to_dict(packet, strict=True)
        if "Raw" in packet_dict:
            del packet_dict["Raw"]
        packet_dict["hexdump"] = hexdump(packet, dump=True)
        packet_dict_no_bytes = bytes_to_string(packet_dict)

        pprint(packet_dict_no_bytes)

        print(f"CaptureThread: sending capture: {packet_dict_no_bytes}")
        send_capture(
            self.quokka_ip,
            self.serial_no,
            str(datetime.now())[:-1],
            [packet_dict_no_bytes],
        )

    def run(self):

        print(
            f"CaptureThread: starting capture: iface={self.interface}, filter={self.capture_filter}"
        )
        sniff(
            iface=self.interface,
            filter=self.capture_filter,
            timeout=300,
            prn=self.process_packet,
        )

        print(f"\n\n-----> CaptureThread: competed capture")
