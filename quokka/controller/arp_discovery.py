from python_arptable import get_arp_table
from pprint import pprint

arp_table_list = get_arp_table()
# pprint(arp_table_list)

arp_table = dict()
for arp_entry in arp_table_list:

    if arp_entry["HW address"] != "00:00:00:00:00:00":
        arp_table[arp_entry["IP address"]] = arp_entry["HW address"]

pprint(arp_table)
