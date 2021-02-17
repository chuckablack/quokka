# ---- Worker application to capture packets --------------------------------

import pika
import json
import threading
import time
import requests
from datetime import datetime
import psutil

from CaptureThread import CaptureThread
from PortscanThread import PortscanThread
from TracerouteThread import TracerouteThread


class WorkerThread(threading.Thread):

    def __init__(self, quokka, worker_type, connection_type, serial_no, heartbeat):

        threading.Thread.__init__(self)

        self.quokka = quokka
        self.worker_type = worker_type
        self.connection_type = connection_type
        self.serial_no = serial_no
        self.heartbeat_interval = int(heartbeat)

        self.channel = None
        self.connection = None

        self.latest_response_time = 0
        self.creation_time = int(time.time())

        self.terminate = False

    def run(self):

        print(f"{self.worker_type} worker: starting work, quokka={self.quokka}")
        heartbeat_thread = threading.Thread(target=self.heartbeat, args=(self.heartbeat_interval,))
        heartbeat_thread.start()

        if self.connection_type == "rabbitmq":
            self.start_receiving()

        heartbeat_thread.join()
        print(f"{self.worker_type} worker: Worker thread shutting down")

    def heartbeat(self, interval):

        while True and not self.terminate:

            heartbeat_info = {
                "name": None,
                "hostname": None,
                "serial": self.serial_no,
                "worker_type": self.worker_type,
                "response_time": self.latest_response_time,
                "cpu": psutil.cpu_percent(),
                "memory": psutil.virtual_memory()[2],
                "uptime": int(time.time()) - self.creation_time,
            }

            try:
                start = time.time()
                rsp = requests.post(
                    "http://" + self.quokka + ":5000/worker/heartbeat", json=heartbeat_info
                )
                self.latest_response_time = (time.time() - start) * 1000
                if rsp.status_code != 200:
                    print(f"{str(datetime.now())[:-3]}: --- {self.worker_type} heartbeat failed, response: {rsp.status_code}")
                    print(f"{str(datetime.now())[:-3]}: --- --- reason: {rsp.reason}")
                else:
                    print(f"{str(datetime.now())[:-3]}: --- {self.worker_type} heartbeat successful, response: {rsp.status_code} {rsp.json()}")

                if rsp.headers.get("content-type") == "application/json" and "commands" in rsp.json():
                    for command in rsp.json()["commands"]:
                        print(f"{str(datetime.now())[:-3]}: --- --- begin processing command: {command}")
                        command_info = json.loads(command["command_info"])
                        self.process_command(command_info)
                        print(f"{str(datetime.now())[:-3]}: --- --- end processing command: {command}")

            except BaseException as e:
                print(f"{str(datetime.now())[:-3]}: --- {self.worker_type} error connecting to quokka server: {e}")

            time.sleep(interval)

        print(f"[!]{self.worker_type} worker: heartbeat terminating")

    def start_receiving(self):

        print(f"{self.worker_type} worker: starting rabbitmq listening")

        self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        self.channel = self.connection.channel()
        worker_queue = self.worker_type + "_queue"
        self.channel.queue_declare(queue=worker_queue, durable=True)
        print(f"\n\n [*] {self.worker_type} worker: waiting for messages on queue: {worker_queue}.")

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            on_message_callback=self.receive_capture_request, queue=worker_queue
        )

        # try:
        self.channel.start_consuming()

        # except BaseException as e:
        #     print(f"\nworker thread: {self.worker_type} worker shutting down")

    def receive_capture_request(self, capture_channel, method, properties, body):

        print(f"{self.worker_type} worker: received message")
        worker_info = json.loads(body)
        print(f"{self.worker_type} worker info: {worker_info}")

        self.channel.basic_ack(delivery_tag=method.delivery_tag)

        self.process_command(worker_info)
        print("\n\n [*] Capture Worker: waiting for messages.")

    def process_command(self, worker_info):

        if "quokka" not in worker_info:
            self.quokka = "localhost"
        else:
            self.quokka = worker_info["quokka"]

        if self.worker_type == "capture":
            worker_thread = CaptureThread(self.quokka, self.serial_no, worker_info)
        elif self.worker_type == "portscan":
            worker_thread = PortscanThread(self.quokka, self.serial_no, worker_info)
        elif self.worker_type == "traceroute":
            worker_thread = TracerouteThread(self.quokka, self.serial_no, worker_info)
        else:
            print(f"Invalid worker_type: {self.worker_type}, exiting")
            return

        worker_thread.start()
