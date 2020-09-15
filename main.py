import time
import socket
import pyshark
from mappings.protocols import *

from stream import Stream
from packet import TCPPacket, UDPPacket


"""
    proto: 0.005927314613696935
    service: 0.0013659108479552023
    sbytes: 0.06782617945260296
    dbytes: 0.025579069315682657
    sttl: 0.5264658547173781
    sloss: 0.18642726015230146
    sinpkt: 0.013057944890424536
    smean: 0.0004578638877515533
    ct_srv_src: 0.06798488547203052
    ct_srv_dst: 0.10490771665017604
"""

IP_ADDRESS = "192.168.1.104"
streams = {}


def parse(pkt):
    # All on pkt in, deal with connections from that IP
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

            streams[pkt.tcp.stream] = Stream(
                pkt.ip.proto, client, client_port, IP_ADDRESS, server_port
            )

        streams[pkt.tcp.stream].add_packet(pkt)

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

            streams[pkt.udp.stream] = Stream(
                pkt.ip.proto, client, client_port, IP_ADDRESS, server_port
            )

        streams[pkt.udp.stream].add_packet(pkt)

    else:
        pkt.pretty_print()

    if len(streams.keys()) == 5:
        for x in streams:
            streams[x].pretty_print()

        exit()


cap = pyshark.LiveCapture(interface="en0", bpf_filter="ip")
cap.apply_on_packets(parse)
