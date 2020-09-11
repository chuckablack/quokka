import nmap


def get_port_scan_tcp_connection(ip):

    nm = nmap.PortScanner()
    nm.scan(ip, '1-1024')

    try:
        nm[ip]
    except KeyError as e:
        return "failed", "nmap port scan failed"

    return "success", nm[ip].all_tcp()
