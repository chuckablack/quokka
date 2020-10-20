import base64
from datetime import datetime
from socket import gethostname
from threading import Thread

from scapy.layers.inet import traceroute
from util import send_traceroute


class TracerouteThread(Thread):

    def __init__(self, quokka_ip, serial_no, traceroute_info):
        super().__init__()
        print(f"TracerouteThread: initializing thread object: traceroute_info={traceroute_info}")

        if "target" not in traceroute_info:
            print(f"TracerouteThread: missing information in traceroute_info: {traceroute_info}")
            return

        self.quokka_ip = quokka_ip
        self.serial_no = serial_no
        self.target = traceroute_info["target"]
        self.token = traceroute_info["token"]

    def process_traceroute(self, traceroute):

        print(f"TracerouteThread: generating traceroute image: {traceroute}")
        tmp_png = 'tmp-traceroute-graph.png'
        traceroute.graph(format='png', target=tmp_png)
        with open(tmp_png, 'rb') as png_file:
            traceroute_graph_bytes = base64.b64encode(png_file.read())

        print(f"TracerouteThread: sending traceroute: {traceroute_graph_bytes[:1024]}")
        status_code = send_traceroute(
            gethostname(),
            self.quokka_ip,
            self.serial_no,
            self.target,
            self.token,
            str(datetime.now())[:-1],
            traceroute_graph_bytes,
        )
        print(f"TracerouteThread: traceroute sent, result={status_code}\n")

    def run(self):

        print(f"TracerouteThread: starting traceroute: target = {self.target}")

        try:
            traceroute_output = traceroute(self.target, verbose=0)
            self.process_traceroute(traceroute_output[0])
        except BaseException as e:
            print(f"!!! Caught error attempting to do traceroute: {e}")

        print(f"\n\n-----> TracerouteThread: competed traceroute")
