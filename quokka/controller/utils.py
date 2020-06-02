import re


def get_response_time(ping_output):

    m = re.search(r"time=([0-9]*)", ping_output)
    if m.group(1).isnumeric():
        return int(m.group(1))


