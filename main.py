import time
import socket
import pyshark
from collections import deque
from features import FEATURES
import csv

from mappings.protocols import *

from stream import Stream
from packet import *
from connections import ConnectionStats


IP_ADDRESS = "192.168.1.104"
streams = {}
connections = ConnectionStats(IP_ADDRESS)


def parse(pkt, wr):
    # All on pkt in, deal with connections from that IP

    packet_in = PacketStats(pkt, IP_ADDRESS)

    if pkt.ip.proto == "6":
        print("Parsing TCP packet")
        if not streams.get(pkt.tcp.stream):
            streams[pkt.tcp.stream] = Stream(pkt, IP_ADDRESS)
            print(f"TCP STREAM {pkt.tcp.stream}")

        connections.packet_in(pkt)
        streams[pkt.tcp.stream].add_packet(pkt)

        packet_in.get_tcp_features(pkt)
        packet_in.get_stream_features(streams[pkt.tcp.stream])

    elif pkt.ip.proto == "17":
        print("Parsing UDP packet")
        if not streams.get(pkt.udp.stream):
            streams[pkt.udp.stream] = Stream(pkt, IP_ADDRESS, udp=True)

        connections.packet_in(pkt, udp=True)
        streams[pkt.udp.stream].add_packet(pkt)

        packet_in.get_udp_features(pkt)
        packet_in.get_stream_features(streams[pkt.udp.stream])

    else:
        pkt.pretty_print()
        return

    # generate stats
    packet_in.get_connection_features(connections, pkt)

    print(packet_in.get_features())
    wr.writerow(packet_in.get_features())


with open("serverOutput.csv", "w") as outputCsv:
    wr = csv.writer(outputCsv)
    wr.writerow(FEATURES)
    print(FEATURES)
    cap = pyshark.LiveCapture(interface="en0", bpf_filter="ip")
    # cap = pyshark.FileCapture('http-flood.pcap')
    cap.apply_on_packets(lambda x: parse(x, wr))
