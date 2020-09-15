class TCPPacket:
    def __init__(self, pkt):
        
        self.length = pkt.tcp.len
        self.src_ip_addr = pkt.ip.src
        self.dst_ip_addr = pkt.ip.dst
        self.sttl = pkt.ip.ttl
        self.flags = pkt.tcp.flags
        if 'time_delta' in pkt.tcp.field_names:
            self.time_delta = pkt.tcp.time_delta
        if 'time_relative' in pkt.tcp.field_names:
            self.time_relative = pkt.tcp.time_relative
        if 'payload' in pkt.tcp.field_names:
            self.payload = pkt.tcp.payload

    def __str__(self):
        return f'''TCP Packet: {self.src_ip_addr} -> {self.dst_ip_addr}
    length: {self.length}
    src_ip_addr: {self.src_ip_addr}
    dst_ip_addr: {self.dst_ip_addr}
    sttl: {self.sttl}
    time_delta: {self.time_delta}
    time_relative: {self.time_relative}'''

class UDPPacket:
    def __init__(self, pkt):
        self.length = pkt.udp.length
        self.src_ip_addr = pkt.ip.src
        self.dst_ip_addr = pkt.ip.dst
        self.sttl = pkt.ip.ttl
        if 'time_delta' in pkt.udp.field_names:
            self.time_delta = pkt.udp.time_delta
        if 'time_relative' in pkt.udp.field_names:
            self.time_relative = pkt.udp.time_relative

    def __str__(self):
        return f'''TCP Packet: {self.src_ip_addr} -> {self.dst_ip_addr}
    length: {self.length}
    sttl: {self.sttl}
    time_delta: {self.time_delta}
    time_relative: {self.time_relative}'''


