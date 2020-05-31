from ipaddress import ip_network
import socket
import subprocess
from datetime import datetime

from quokka.models.apis import set_host


def discover():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip_addr = s.getsockname()[0]
    print(f"My IP address is {my_ip_addr}")

    found_hosts = []
    subnet = ip_network(my_ip_addr + "/24", False)
    for ip_addr in subnet.hosts():
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
            host["mac_address"] = ""
            host["availability"] = True
            host["response_time"] = 1.0
            host["last_heard"] = str(datetime.now())

            set_host(host)

            found_hosts.append({"hostname": hostname, "ip": str(ip_addr)})

    for active_host in found_hosts:
        print(f"host: {active_host['hostname'][0]:30}   ip: {str(active_host['ip']):16}")

