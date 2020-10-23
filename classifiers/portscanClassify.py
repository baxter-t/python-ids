def classify(f):
    if f['connections_from_ip_port_1_seconds'] <= 1.5 and f['connections_inbound_pkts_to_ip'] <= 2.5 and f['ttl'] <= 56.5 and f['connections_from_ip_1_seconds'] <= 2 and f['ttl'] > 47 and f['transaction_duration'] > 0.001:
        return 1

    if f['connections_from_ip_port_1_seconds'] <= 1.5 and f['connections_inbound_pkts_to_ip'] <= 2.5 and f['ttl'] <= 56.5 and f['connections_from_ip_1_seconds'] > 2.0 :
        return 1

    if f['connections_from_ip_port_1_seconds'] <= 1.5 and f['connections_inbound_pkts_to_ip'] > 2.5 and f['flags'] <= 9 :
        return 1

    if f['connections_from_ip_port_1_seconds'] > 1.5 and f['flags'] <= 10.0 and f['ttl'] <= 56:
        return 1

    if ['connections_from_ip_port_1_seconds'] > 1.5 and f['flags'] > 10.0 and f['time_delta'] > 0.289 and f['time_relative'] > 0.569:
        return 1

    return 0
