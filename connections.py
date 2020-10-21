import time


class ConnectionStats:
    def __init__(self, server_ip):
        self.server = server_ip

        self.connections_ip_pkts_inbound = {}
        self.connections_ip_pkts_outbound = {}

        self.connections_ip = {}
        self.connections_ip_port = {}

        self.connections_ip_acked = {}

    def packet_in(self, pkt, udp=False):
        conn_ip = pkt.ip.src if pkt.ip.dst == self.server else pkt.ip.dst
        conn_port = pkt[2].srcport if pkt.ip.dst == self.server else pkt[2].dstport

        if not self.connections_ip.get(conn_ip):
            self.connections_ip[conn_ip] = []

        if not self.connections_ip_port.get((conn_ip, conn_port)):
            self.connections_ip_port[(conn_ip, conn_port)] = []

        if not self.connections_ip_acked.get(conn_ip):
            self.connections_ip_acked[conn_ip] = 0

        if not self.connections_ip_pkts_inbound.get(conn_ip):
            self.connections_ip_pkts_inbound[conn_ip] = 0

        if not self.connections_ip_pkts_outbound.get(conn_ip):
            self.connections_ip_pkts_outbound[conn_ip] = 0

        if pkt.ip.src == self.server:
            self.connections_ip_pkts_outbound[conn_ip] += 1
        else:
            self.connections_ip_pkts_inbound[conn_ip] += 1

        self.connections_ip[conn_ip].append(time.time())
        self.connections_ip_port[(conn_ip, conn_port)].append(time.time())

        if not udp:
            # Tally the ACKs for that connection
            self.connections_ip_acked[conn_ip] += 1 if int(str(pkt.tcp.flags), 16) & 16 != 0 else 0

    def get_acked_percentage_ip(self, pkt):
        conn_ip = pkt.ip.src if pkt.ip.dst == self.server else pkt.ip.dst

        if self.connections_ip_pkts_outbound[conn_ip]:
            return (
                self.connections_ip_acked[conn_ip]
                / self.connections_ip_pkts_outbound[conn_ip]
            )
        else:
            return 1

    def get_outbound_pkts_to_ip(self, pkt):
        conn_ip = pkt.ip.src if pkt.ip.dst == self.server else pkt.ip.dst
        return self.connections_ip_pkts_outbound[conn_ip]

    def get_inbound_pkts_to_ip(self, pkt):
        conn_ip = pkt.ip.src if pkt.ip.dst == self.server else pkt.ip.dst
        return self.connections_ip_pkts_inbound[conn_ip]

    def get_connections_n_seconds(self, pkt, n=3, use_port=False):
        conn_ip = pkt.ip.src if pkt.ip.dst == self.server else pkt.ip.dst
        conn_port = pkt[2].srcport if pkt.ip.dst == self.server else pkt[2].dstport
        threshold = time.time() - n * 1000

        if use_port:
            return len(
                [
                    x
                    for x in self.connections_ip_port[(conn_ip, conn_port)]
                    if x > threshold
                ]
            )
        else:
            return len([x for x in self.connections_ip[conn_ip] if x > threshold])
