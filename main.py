import time
import socket
import pyshark
from collections import deque
from features import FEATURES
import sys
import csv
import argparse
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from sklearn import tree, svm
from joblib import dump, load

from connections import *
from packet import *
from features import *
from stream import *
from classify import *

import pandas as pd
import numpy as np

import signal

parser = argparse.ArgumentParser(description="Network Classifier.")
parser.add_argument("IP_ADDRESS", metavar="S", type=str, help="IP Address IDS is deployed on")
parser.add_argument("OUTPUT", metavar="O", type=str, help="Output filename")
parser.add_argument("-c", dest="CLASSIFY", action="store_const", const=1, default=0)
args = parser.parse_args()

OUTPUT_FILE = args.OUTPUT
IP_ADDRESS = args.IP_ADDRESS
CLASSIFY = args.CLASSIFY

streams = {}
connections = ConnectionStats(IP_ADDRESS)
PACKET_DATAFRAME = pd.DataFrame(columns = FEATURES)

def shutdown_handler(signal, frame):
    global PACKET_DATAFRAME
    PACKET_DATAFRAME.to_csv(OUTPUT_FILE, header=True, index=False)
    exit(0)

signal.signal(signal.SIGINT, shutdown_handler)

def dealWithPacket(pkt):
    global PACKET_DATAFRAME
    packetFeatures = parse(pkt)

    if CLASSIFY and packetFeatures:
        if classify(packetFeatures):
            print("Malicious packet Identified")
    else: 
        PACKET_DATAFRAME = PACKET_DATAFRAME.append(packetFeatures, ignore_index=True) 

def parse(pkt):

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

        return packet_in.get_features()
    
    except Exception as e:
        print(e)


if __name__ == '__main__':
    cap = pyshark.LiveCapture(interface="en0", bpf_filter="ip")
    cap.apply_on_packets(lambda x: dealWithPacket(x))

