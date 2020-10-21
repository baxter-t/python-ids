FEATURES = [
    # IP
    "src",
    "dst",
    "proto",
    "ttl",
    "inbound",
    # UDP OR TCP
    "srcport",
    "dstport",
    "length",
    "time_delta",
    "time_relative",
    # TCP
    "flags",
    # STREAM
    "outbound_pkt_count",
    "inbound_pkt_count",
    "pkt_count_diff",
    "outbound_bytes",
    "inbound_bytes",
    "bytes_diff",
    "outbound_bytes_mean",
    "inbound_bytes_mean",
    "transaction_duration",
    "inbound_avg_interpacket_time",
    "outbound_avg_interpacket_time",
    # CONNECTION
    "connections_from_ip_1_seconds",
    "connections_from_ip_port_1_seconds",
    "connections_from_ip_3_seconds",
    "connections_from_ip_port_3_seconds",
    "connections_acked_percentage",
    "connections_outbound_pkts_to_ip",
    "connections_inbound_pkts_to_ip",
]
