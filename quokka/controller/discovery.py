from ipaddress import ip_network
import socket
import subprocess
from datetime import datetime
from time import sleep

from quokka.models.apis import set_host

from python_arptable import get_arp_table
from pprint import pprint

stop_thread = False


def learn_mac_addresses():
    arp_table_list = get_arp_table()

    arp_table = dict()
    for arp_entry in arp_table_list:

        if arp_entry["HW address"] != "00:00:00:00:00:00":
            arp_table[arp_entry["IP address"]] = arp_entry["HW address"]

    pprint(arp_table)
    return arp_table


def discover(interval):

    while True and not stop_thread:

        mac_addresses = learn_mac_addresses()

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        my_ip_addr = s.getsockname()[0]
        print(f"My IP address is {my_ip_addr}")

        found_hosts = []
        subnet = ip_network(my_ip_addr + "/24", False)
        for ip_addr in subnet.hosts():

            if stop_thread:
                break

            print(f"--- pinging {str(ip_addr)}")
            active = subprocess.call(["ping", "-c1", "-n", "-i0.5", "-W2", str(ip_addr)])
            if active == 0:

                print(f"--- found one: {str(ip_addr)}")
                try:
                    hostname = socket.gethostbyaddr(str(ip_addr))
                except BaseException as e:
                    hostname = (str(ip_addr), [], [str(ip_addr)])

                if hostname:
                    print(f"--- found its hostname: {hostname}")

                host = dict()
                host["name"] = hostname[0]
                host["ip_address"] = str(ip_addr)
                host["mac_address"] = mac_addresses[str(ip_addr)] if str(ip_addr) in mac_addresses else ""
                host["availability"] = True
                host["response_time"] = 1.0
                host["last_heard"] = str(datetime.now())

                set_host(host)
                found_hosts.append({"hostname": hostname, "ip": str(ip_addr)})

        for active_host in found_hosts:
            print(f"host: {active_host['hostname'][0]:30}   ip: {str(active_host['ip']):16}")

        sleep(interval)

    print("gracefully exiting discovery")
