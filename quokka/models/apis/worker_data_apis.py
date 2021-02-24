import time
from datetime import datetime
from pprint import pformat

from sqlalchemy import desc, or_, func

from quokka import db
from quokka.controller.utils import log_console
from quokka.models.Capture import Capture
from quokka.models.Command import Command
from quokka.models.Portscan import Portscan
from quokka.models.Traceroute import Traceroute
from quokka.models.util import get_model_as_dict


def record_capture(timestamp, source, captured_packets):

    for captured_packet in captured_packets:

        packet = dict()
        packet["timestamp"] = str(datetime.now())[:-3]
        packet["local_timestamp"] = timestamp
        packet["source"] = source

        if "Ethernet" in captured_packet:
            if "dst" in captured_packet["Ethernet"]:
                packet["ether_dst"] = captured_packet["Ethernet"]["dst"]
            if "src" in captured_packet["Ethernet"]:
                packet["ether_src"] = captured_packet["Ethernet"]["src"]

        if "IP" in captured_packet:
            if "dst" in captured_packet["IP"]:
                packet["ip_dst"] = captured_packet["IP"]["dst"]
            if "src" in captured_packet["IP"]:
                packet["ip_src"] = captured_packet["IP"]["src"]

        if "TCP" in captured_packet:
            packet["protocol"] = "TCP"
            if "dport" in captured_packet["TCP"]:
                packet["dport"] = captured_packet["TCP"]["dport"]
            if "sport" in captured_packet["TCP"]:
                packet["sport"] = captured_packet["TCP"]["sport"]

            if packet["sport"] == 443 or packet["dport"] == 443:
                packet["protocol"] = "HTTPS"
            elif packet["sport"] == 80 or packet["dport"] == 80:
                packet["protocol"] = "HTTP"

        elif "UDP" in captured_packet:
            packet["protocol"] = "UDP"
            if "dport" in captured_packet["UDP"]:
                packet["dport"] = captured_packet["UDP"]["dport"]
            if "sport" in captured_packet["UDP"]:
                packet["sport"] = captured_packet["UDP"]["sport"]

            if packet["sport"] == 123 or packet["dport"] == 123:
                packet["protocol"] = "NTP"

        if "DNS" in captured_packet:
            packet["protocol"] = "DNS"
        elif "ARP" in captured_packet:
            packet["protocol"] = "ARP"
        elif "DHCP" in captured_packet:
            packet["protocol"] = "DCHP"
        elif "ICMP" in captured_packet:
            packet["protocol"] = "ICMP"

        # capture["packet_json"] = json.dumps(packet)
        packet["packet_hexdump"] = captured_packet["hexdump"]
        del captured_packet["hexdump"]
        packet["packet_json"] = pformat(captured_packet)

        capture_obj = Capture(**packet)
        db.session.add(capture_obj)

        db.session.commit()


def get_capture(ip, protocol, port, num_packets):

    # We must generate and implement specific queries based on what has been requested
    # Note that if we add more imports, we'll have to modify this simple method to handle all cases
    if ip and not protocol:  # Note that if not protocol, port isn't relevant
        packet_objs = (
            db.session.query(Capture)
            .filter(or_(Capture.ip_src == ip, Capture.ip_dst == ip))
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )
    elif ip and protocol and not port:
        packet_objs = (
            db.session.query(Capture)
            .filter(or_(Capture.ip_src == ip, Capture.ip_dst == ip))
            .filter(func.lower(Capture.protocol) == func.lower(protocol))
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )
    elif ip and protocol and port:
        packet_objs = (
            db.session.query(Capture)
            .filter(or_(Capture.ip_src == ip, Capture.ip_dst == ip))
            .filter(func.lower(Capture.protocol) == func.lower(protocol))
            .filter(or_(Capture.sport == port, Capture.dport == port))
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )
    elif not ip and protocol and not port:
        packet_objs = (
            db.session.query(Capture)
            .filter(func.lower(Capture.protocol) == func.lower(protocol))
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )
    elif not ip and protocol and port:
        packet_objs = (
            db.session.query(Capture)
            .filter(func.lower(Capture.protocol) == func.lower(protocol))
            .filter(or_(Capture.sport == port, Capture.dport == port))
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )
    else:  # Not sure what was requested, so just get everything
        packet_objs = (
            db.session.query(Capture)
            .order_by(desc(Capture.timestamp))
            .limit(num_packets)
        )

    packets = list()
    for packet_obj in packet_objs:
        packet = get_model_as_dict(packet_obj)
        packets.append(packet)

    return packets


def record_portscan(portscan_info):

    portscan = dict()
    if "source" not in portscan_info:
        log_console(f"record_portscan: missing 'source' in portscan info")
        return
    if "host_ip" not in portscan_info:
        log_console(f"record_portscan: missing 'host_ip' in portscan info")
        return
    if "host_name" not in portscan_info:
        log_console(f"record_portscan: missing 'host_name' in portscan info")
        return
    if "token" not in portscan_info:
        log_console(f"record_portscan: missing 'token' in portscan_info")
        return
    if "timestamp" not in portscan_info:
        log_console(f"record_portscan: missing 'timestamp' in portscan info")
        return
    if "scan_output" not in portscan_info:
        log_console(f"record_portscan: missing 'scan_output' in portscan info")
        return

    portscan["source"] = portscan_info["source"]
    portscan["host_ip"] = portscan_info["host_ip"]
    portscan["host_name"] = portscan_info["host_name"]
    portscan["token"] = portscan_info["token"]
    portscan["timestamp"] = portscan_info["timestamp"]
    portscan["scan_output"] = portscan_info["scan_output"]

    portscan_obj = Portscan(**portscan)
    db.session.add(portscan_obj)

    db.session.commit()


def get_port_scan_extended(host_ip, host_name, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        search = {"host_ip": host_ip, "host_name": host_name, "token": token}
        portscan_obj = db.session.query(Portscan).filter_by(**search).one_or_none()

        if not portscan_obj:
            time.sleep(2)
            continue

        portscan = get_model_as_dict(portscan_obj)
        return "success", portscan["scan_output"]

    return "failed", "No scan results in time provided"


def record_traceroute(traceroute_info):

    traceroute = dict()
    if "source" not in traceroute_info:
        log_console(f"record_traceroute: missing 'source' in traceroute info")
        return
    if "target" not in traceroute_info:
        log_console(f"record_traceroute: missing 'target' in traceroute info")
        return
    if "token" not in traceroute_info:
        log_console(f"record_traceroute: missing 'token' in traceroute_info")
        return
    if "timestamp" not in traceroute_info:
        log_console(f"record_traceroute: missing 'timestamp' in traceroute info")
        return
    if "traceroute_img" not in traceroute_info:
        log_console(f"record_traceroute: missing 'traceroute_img' in traceroute info")
        return

    traceroute["source"] = traceroute_info["source"]
    traceroute["target"] = traceroute_info["target"]
    traceroute["token"] = traceroute_info["token"]
    traceroute["timestamp"] = traceroute_info["timestamp"]
    traceroute["traceroute_img"] = traceroute_info["traceroute_img"]

    traceroute_obj = Traceroute(**traceroute)
    db.session.add(traceroute_obj)

    db.session.commit()


def get_traceroute(target, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        # search = {"target": target, "token": token}  # 'target' may have been modified
        search = {"token": token}
        traceroute_obj = db.session.query(Traceroute).filter_by(**search).one_or_none()

        if not traceroute_obj:
            time.sleep(2)
            continue

        traceroute = get_model_as_dict(traceroute_obj)
        return "success", traceroute["traceroute_img"]

    return "failed", "No traceroute results in time provided"


def set_command(command):

    command_obj = Command(**command)
    db.session.add(command_obj)

    db.session.commit()


def get_commands(serial=None, host=None, worker_type=None, set_delivered=False):

    if not serial and not host:
        return "failed", "Must provide serial or host"
    if not worker_type:
        return "failed", "must provide worker_type"

    search = dict()
    if serial:
        search["serial"] = serial
    if host:
        search["host"] = host
    search["worker_type"] = worker_type
    search["delivered"] = False

    command_objs = db.session.query(Command).filter_by(**search).all()

    commands = list()
    for command_obj in command_objs:
        commands.append(get_model_as_dict(command_obj))

    if set_delivered:
        for command_obj in command_objs:
            command_obj.delivered = True
        db.session.commit()

    return "success", commands
