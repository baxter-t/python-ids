import time


class ConnectionList:
    def __init__(self, server_ip):
        self.server = server_ip
        self.connections_ip = {}
        self.connections_ip_port = {}

    def new_stream(self, pkt, udp=False):
       conn_ip = pkt.ip.src if pkt.ip.dst == self.server else pkt.ip.dst
        conn_port = pkt[2].srcport if pkt.ip.dst == self.server else pkt[2].dstport

        if not self.connections_ip.get(conn_ip):
            self.connections_ip[conn_ip] = []

        if not self.connections_ip_port.get((conn_ip, conn_port)):
            self.connections_ip_port[(conn_ip, conn_port)] = []

        self.connections_ip[conn_ip].append(time.time())
        self.connections_ip_port[(conn_ip, conn_port)].append(time.time())

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
