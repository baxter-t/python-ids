import time

from packet import *


class Stream:
    def __init__(self, proto, client_ip, client_port, server_ip, server_port):
        self.pkts = []
        self.proto = proto
        self.client = client_ip
        self.server = server_ip
        self.client_port = int(client_port)
        self.server_port = int(server_port)
        self.start_time = time.time()
        self.last_time = time.time()

        self.outbound_pkt_count = 0
        self.inbound_pkt_count = 0
        self.outbound_bytes = 0
        self.inbound_bytes = 0
        self.outbound_bytes_mean = 0
        self.inbound_bytes_mean = 0

        self.inbound_avg_interpacket_time = 0
        self.outbound_avg_interpacket_time = 0

    def add_packet(self, pkt):
        if pkt.ip.proto == "6":
            new_packet = TCPPacket(pkt)
        else:
            new_packet = UDPPacket(pkt)

        if pkt.ip.src == self.server:
            self.outbound_avg_interpacket_time = (
                self.outbound_avg_interpacket_time * self.outbound_pkt_count
                + int(new_packet.length)
            ) / (self.outbound_pkt_count + 1)

            # Outbound
            self.outbound_pkt_count += 1
            self.outbound_bytes += int(new_packet.length)
            self.outbound_bytes_mean = self.outbound_bytes / self.outbound_pkt_count
        elif pkt.ip.dst == self.server:
            self.inbound_avg_interpacket_time = (
                self.inbound_avg_interpacket_time * self.inbound_pkt_count
                + int(new_packet.length)
            ) / (self.inbound_pkt_count + 1)

            # Inbound
            self.inbound_pkt_count += 1
            self.inbound_bytes += int(new_packet.length)
            self.inbound_bytes_mean = self.inbound_bytes / self.inbound_pkt_count

        self.last_time = time.time()
        self.duration =  self.last_time - self.start_time

