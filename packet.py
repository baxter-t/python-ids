from features import FEATURES


class TCPPacket:
    def __init__(self, pkt):

        self.length = int(pkt.tcp.len)
        self.src_ip_addr = pkt.ip.src
        self.dst_ip_addr = pkt.ip.dst
        self.sttl = int(pkt.ip.ttl)
        self.flags = float(int(str(pkt.tcp.flags), 16))

        if "time_delta" in pkt.tcp.field_names:
            self.time_delta = float(pkt.tcp.time_delta)
        if "time_relative" in pkt.tcp.field_names:
            self.time_relative = float(pkt.tcp.time_relative)

    def __str__(self):
        return f"""TCP Packet: {self.src_ip_addr} -> {self.dst_ip_addr}
    length: {self.length}
    src_ip_addr: {self.src_ip_addr}
    dst_ip_addr: {self.dst_ip_addr}
    sttl: {self.sttl}
    time_delta: {self.time_delta}
    time_relative: {self.time_relative}"""


class UDPPacket:
    def __init__(self, pkt):
        self.length = int(pkt.udp.length) - 8
        self.src_ip_addr = pkt.ip.src
        self.dst_ip_addr = pkt.ip.dst
        self.ttl = int(pkt.ip.ttl)
        if "time_delta" in pkt.udp.field_names:
            self.time_delta = float(pkt.udp.time_delta)
        if "time_relative" in pkt.udp.field_names:
            self.time_relative = float(pkt.udp.time_relative)

    def __str__(self):
        return f"""TCP Packet: {self.src_ip_addr} -> {self.dst_ip_addr}
    length: {self.length}
    sttl: {self.sttl}
    time_delta: {self.time_delta}
    time_relative: {self.time_relative}"""


class PacketStats:
    def __init__(self, pkt, IP_ADDRESS):
        self.features = {
            "src": pkt.ip.src,
            "dst": pkt.ip.dst,
            "proto": int(pkt.ip.proto),
            "ttl": int(pkt.ip.ttl),
            "inbound": 1 if pkt.ip.src != IP_ADDRESS else 0,
        }

    def get_udp_features(self, pkt):
        self.features["srcport"] = int(pkt.udp.srcport)
        self.features["dstport"] = int(pkt.udp.dstport)
        self.features["length"] = int(pkt.udp.length)
        self.features["time_delta"] = float(pkt.udp.time_delta)
        self.features["time_relative"] = float(pkt.udp.time_relative)

    def get_tcp_features(self, pkt):
        self.features["srcport"] = int(pkt.tcp.srcport)
        self.features["dstport"] = int(pkt.tcp.dstport)

        self.features["length"] = int(pkt.tcp.len)
        self.features["time_delta"] = float(pkt.tcp.time_delta)
        self.features["time_relative"] = float(pkt.tcp.time_relative)
        self.features["flags"] = float(int(str(pkt.tcp.flags), 16))

    def get_stream_features(self, stream):

        self.features["outbound_pkt_count"] = stream.outbound_pkt_count
        self.features["inbound_pkt_count"] = stream.inbound_pkt_count
        self.features["pkt_count_diff"] = (
            stream.outbound_pkt_count - stream.inbound_pkt_count
        )

        self.features["outbound_bytes"] = stream.outbound_bytes
        self.features["inbound_bytes"] = stream.inbound_bytes
        self.features["bytes_diff"] = stream.outbound_bytes - stream.inbound_bytes

        self.features["outbound_bytes_mean"] = stream.outbound_bytes_mean
        self.features["inbound_bytes_mean"] = stream.inbound_bytes_mean

        self.features["transaction_duration"] = stream.duration

        self.features[
            "inbound_avg_interpacket_time"
        ] = stream.inbound_avg_interpacket_time
        self.features[
            "outbound_avg_interpacket_time"
        ] = stream.outbound_avg_interpacket_time

    def get_connection_features(self, connections, pkt):
        self.features[
            "connections_from_ip_1_seconds"
        ] = connections.get_connections_n_seconds(pkt, n=1)
        self.features[
            "connections_from_ip_3_seconds"
        ] = connections.get_connections_n_seconds(pkt)
        self.features[
            "connections_from_ip_port_1_seconds"
        ] = connections.get_connections_n_seconds(pkt, n=1, use_port=True)
        self.features[
            "connections_from_ip_port_3_seconds"
        ] = connections.get_connections_n_seconds(pkt, use_port=True)

        self.features[
            "connections_acked_percentage"
        ] = connections.get_acked_percentage_ip(pkt)
        self.features[
            "connections_outbound_pkts_to_ip"
        ] = connections.get_outbound_pkts_to_ip(pkt)
        self.features[
            "connections_inbound_pkts_to_ip"
        ] = connections.get_inbound_pkts_to_ip(pkt)

    def get_features(self):
        featureDict = {}
        for f in FEATURES:
            featureDict[f] = self.features.get(f, 0)

        return featureDict
