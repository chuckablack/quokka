import re
from datetime import datetime
import socket

def get_response_time(ping_output):

    m = re.search(r"time=([0-9]*)", ping_output)
    if m.group(1).isnumeric():
        return int(m.group(1))


def log_console(output):
    print(f"{str(datetime.now())[:-3]}: {output}")


def get_this_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))         # dest doesn't even have to be reachable
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP