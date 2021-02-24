from ipaddress import ip_network
import socket
import subprocess
from datetime import datetime
from time import sleep

from quokka.models.apis.host_model_apis import set_host
from quokka.controller.utils import get_response_time
from quokka.controller.utils import log_console

from pprint import pprint

try:
    from python_arptable import get_arp_table
except FileNotFoundError as e:
    log_console("!!! Error loading python_arptable, WSL perhaps issue?")
    get_arp_table = None


def learn_mac_addresses():

    try:
        if get_arp_table:
            arp_table_list = get_arp_table()
        else:
            return {}
    except FileNotFoundError as e:
        return {}

    arp_table = dict()
    for arp_entry in arp_table_list:

        if arp_entry["HW address"] != "00:00:00:00:00:00":
            arp_table[arp_entry["IP address"]] = arp_entry["HW address"]

    pprint(arp_table)
    return arp_table


class DiscoverTask:

    def __init__(self):
        self.terminate = False

    def set_terminate(self):
        if not self.terminate:
            self.terminate = True
            log_console(f"{self.__class__.__name__}: Terminate pending")

    def discover(self, interval):

        while True and not self.terminate:

            mac_addresses = learn_mac_addresses()

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            my_ip_addr = s.getsockname()[0]
            log_console(f"My IP address is {my_ip_addr}")

            found_hosts = []
            subnet = ip_network(my_ip_addr + "/24", False)
            for ip_addr in subnet.hosts():

                if self.terminate:
                    break

                log_console(f"--- discovery pinging {str(ip_addr)}")
                try:
                    ping_output = subprocess.check_output(["ping", "-c3", "-n", "-i0.5", "-W2", str(ip_addr)])
                except subprocess.CalledProcessError:
                    continue

                log_console(f"--- found one: {str(ip_addr)}")
                try:
                    hostname = socket.gethostbyaddr(str(ip_addr))
                except (socket.error, socket.gaierror) as e:
                    hostname = (str(ip_addr), [], [str(ip_addr)])

                if hostname:
                    log_console(f"--- found its hostname: {hostname}")

                host = dict()
                host["name"] = hostname[0]
                host["ip_address"] = str(ip_addr)
                host["mac_address"] = mac_addresses[str(ip_addr)] if str(ip_addr) in mac_addresses else ""
                host["availability"] = True
                host["response_time"] = get_response_time(str(ping_output))
                host["last_heard"] = str(datetime.now())

                set_host(host)
                found_hosts.append({"hostname": hostname, "ip": str(ip_addr)})

            for active_host in found_hosts:
                log_console(f"host: {active_host['hostname'][0]:30}   ip: {str(active_host['ip']):16}")

            for _ in range(0, int(interval/10)):
                sleep(10)
                if self.terminate:
                    break

        log_console("...gracefully exiting discovery")
