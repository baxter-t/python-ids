import time
import socket
import pyshark
from collections import deque
from features import FEATURES
import csv

from mappings.protocols import *

from stream import Stream
from packet import *
from connections import ConnectionList


IP_ADDRESS = "192.168.1.104"
streams = {}
connections = ConnectionList(IP_ADDRESS)


def parse(pkt, wr):
    # All on pkt in, deal with connections from that IP

    packet_in = PacketStats(pkt, IP_ADDRESS)

    if pkt.ip.proto == "6":
        print("Parsing TCP packet")
        if not streams.get(pkt.tcp.stream):
            client = pkt.ip.src if pkt.ip.dst == IP_ADDRESS else pkt.ip.dst
            client_port = (
                pkt.tcp.srcport if pkt.ip.dst == IP_ADDRESS else pkt.tcp.dstport
            )
            server_port = (
                pkt.tcp.dstport if pkt.ip.dst == IP_ADDRESS else pkt.tcp.srcport
            )

            # Add new stream
            streams[pkt.tcp.stream] = Stream(
                pkt.ip.proto, client, client_port, IP_ADDRESS, server_port
            )

            # Add new connection
            connections.new_stream(pkt)

        packet_in.get_tcp_features(pkt)
        streams[pkt.tcp.stream].add_packet(pkt)
        packet_in.get_stream_features(streams[pkt.tcp.stream])

    elif pkt.ip.proto == "17":
        print("Parsing UDP packet")
        if not streams.get(pkt.udp.stream):
            client = pkt.ip.src if pkt.ip.dst == IP_ADDRESS else pkt.ip.dst
            client_port = (
                pkt.udp.srcport if pkt.ip.dst == IP_ADDRESS else pkt.udp.dstport
            )
            server_port = (
                pkt.udp.dstport if pkt.ip.dst == IP_ADDRESS else pkt.udp.srcport
            )

            # Add new stream
            streams[pkt.udp.stream] = Stream(
                pkt.ip.proto, client, client_port, IP_ADDRESS, server_port
            )

            # Add new connection
            connections.new_stream(pkt, udp=True)

        packet_in.get_udp_features(pkt)
        streams[pkt.udp.stream].add_packet(pkt)
        packet_in.get_stream_features(streams[pkt.udp.stream])

    else:
        pkt.pretty_print()

    # generate stats
    packet_in.features[
        "connections_from_ip_3_seconds"
    ] = connections.get_connections_n_seconds(pkt)
    packet_in.features[
        "connections_from_ip_port_3_seconds"
    ] = connections.get_connections_n_seconds(pkt, use_port=True)

    print(packet_in.get_features())
    wr.writerow(packet_in.get_features())


with open('serverOutput.csv', 'w') as outputCsv:
    wr = csv.writer(outputCsv)
    wr.writerow(FEATURES)
    print(FEATURES)
    cap = pyshark.LiveCapture(interface="en0", bpf_filter="ip")
    cap.apply_on_packets(lambda x: parse(x, wr))
