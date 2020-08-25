

def byte_to_string(data):

    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = byte_to_string(v)
        return data
    elif isinstance(data, list):
        for index, v in enumerate(data):
            data[index] = byte_to_string(v)
        return data
    elif isinstance(data, tuple):
        data_as_list = list(data)
        for index, v in enumerate(data_as_list):
            data_as_list[index] = byte_to_string(v)
        return tuple(data_as_list)
    elif isinstance(data, bytes):
        return data.decode("latin-1")

    else:
        return data


data = {'BOOTP': {'chaddr': b'R\xd4\xf7W*\xda\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            'ciaddr': '192.168.254.112',
            'file': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00\x00',
            'flags': None,
            'giaddr': '0.0.0.0',
            'hlen': 6,
            'hops': 0,
            'htype': 1,
            'op': 2,
            'options': b'c\x82Sc',
            'secs': 0,
            'siaddr': '0.0.0.0',
            'sname': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00',
            'xid': 3958162300,
            'yiaddr': '192.168.254.112'},
  'DHCP options': {'options': [('message-type', 5),
                               ('server_id', '192.168.254.254'),
                               ('lease_time', 14400),
                               ('renewal_time', 7200),
                               ('rebinding_time', 12600),
                               ('subnet_mask', '255.255.255.0'),
                               ('router', '192.168.254.254'),
                               ('name_server', '192.168.254.254'),
                               ('domain', b'home'),
                               ('NTP_server', '74.40.74.60', '74.40.74.61'),
                               (125,
                                b'\x00\x00\r\xe9#\x04\x06001E46\x05\x0f27287'
                                b'5384272720\x06\x08NVG468MQ'),
                               'end']},
  'Ethernet': {'dst': 'ff:ff:ff:ff:ff:ff',
               'src': 'f8:2d:c0:58:f7:50',
               'type': 2048},
  'IP': {'chksum': 31170,
         'dst': '255.255.255.255',
         'flags': None,
         'frag': 0,
         'id': 0,
         'ihl': 5,
         'len': 372,
         'options': [],
         'proto': 17,
         'src': '192.168.254.254',
         'tos': 16,
         'ttl': 128,
         'version': 4},
  'UDP': {'chksum': 22928, 'dport': 68, 'len': 352, 'sport': 67}}

from pprint import pprint
print("\n----- data before conversion --------------------")
pprint(data)

converted_data = byte_to_string(data)

print("\n----- data after conversion --------------------")
pprint(converted_data)


