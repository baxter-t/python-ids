import time

from packet import *


class Stream:
    def __init__(self, proto, client_ip, client_port, server_ip, server_port):
        self.pkts = []
        self.proto = proto
        self.client = client_ip
        self.server = server_ip
        self.client_port = client_port
        self.server_port = server_port
        self.start_time = time.time()
        self.last_time = time.time()

        self.outbound_pkt_count = 0
        self.inbound_pkt_count = 0
        self.outbound_bytes = 0
        self.inbound_bytes = 0
        self.outbound_bytes_mean = 0
        self.inbound_bytes_mean = 0

    def add_packet(self, pkt):
        if pkt.ip.proto == "6":
            new_packet = TCPPacket(pkt)
        else:
            new_packet = UDPPacket(pkt)

        self.last_time = time.time()

        if pkt.ip.src == self.server:
            # Outbound
            self.outbound_pkt_count += 1
            self.outbound_bytes += int(new_packet.length)
            self.outbound_bytes_mean = self.outbound_bytes / self.outbound_pkt_count
        elif pkt.ip.dst == self.server:
            # Inbound
            self.inbound_pkt_count += 1
            self.inbound_bytes += int(new_packet.length)
            self.inbound_bytes_mean = self.inbound_bytes / self.inbound_pkt_count

    def pretty_print(self):
        print(
            f'{"TCP" if self.proto == "6" else "UDP"}Stream: {self.client}:{self.client_port} -> :{self.server_port}'
        )
        print(f"    {self.client}")
        print(f"    {self.client_port}")
        print(f"    {self.server_port}")
        print(f"    {self.start_time}")
        print(f"    {self.last_time}")
        print(f"    {self.outbound_pkt_count}")
        print(f"    {self.inbound_pkt_count}")
        print(f"    {self.outbound_bytes}")
        print(f"    {self.inbound_bytes}")
        print(f"    {self.outbound_bytes_mean}")
        print(f"    {self.inbound_bytes_mean}")
