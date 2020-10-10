import time
import socket
import pyshark
from collections import deque
from features import FEATURES
import sys
import csv

import mysql.connector

from stream import Stream
from packet import *
from connections import ConnectionStats

db_config = {
    'user': 'root',
    'password': 'root',
    'host': '0.0.0.0',
    'port': 3306,
    'database': 'traffic'
}

SQL_INSERTION = "INSERT INTO packets (src, dst) VALUES (%s, %s)"

IP_ADDRESS = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
# IP_ADDRESS = "192.168.1.104"
streams = {}
connections = ConnectionStats(IP_ADDRESS)


def parse(pkt, wr):
    # All on pkt in, deal with connections from that IP
    try:

        packet_in = PacketStats(pkt, IP_ADDRESS)

        if pkt.ip.proto == "6":
            if not streams.get(pkt.tcp.stream):
                streams[pkt.tcp.stream] = Stream(pkt, IP_ADDRESS)

            connections.packet_in(pkt)
            streams[pkt.tcp.stream].add_packet(pkt)

            packet_in.get_tcp_features(pkt)
            packet_in.get_stream_features(streams[pkt.tcp.stream])

        elif pkt.ip.proto == "17":
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

        wr.writerow(packet_in.get_features())
        dbcursor.execute(SQL_INSERTION, (2, 2))
        print("inserted to dB")
    except:
        print(sys.exc_info()[0])


with open(OUTPUT_FILE, 'w') as outputCsv:

    db = mysql.connector.connect(**db_config)
    dbcursor = db.cursor()

    dbcursor.execute("SELECT * FROM packets")
    for x in dbcursor: 
        print(x)

    wr = csv.writer(outputCsv)
    wr.writerow(FEATURES)
    print(FEATURES)
    cap = pyshark.LiveCapture(interface="ens4", bpf_filter="ip")
    # cap = pyshark.FileCapture('http-flood.pcap')
    cap.apply_on_packets(lambda x: parse(x, wr))
