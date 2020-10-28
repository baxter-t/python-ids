def classify_portscan(f):

    if f['connections_from_ip_port_3_seconds'] <= 1.5:
        if f['connections_from_ip_1_seconds'] <= 4:
            if f['dstport'] <= 12:
                return 1
            else:
                if f['dstport'] <= 12671:
                    return 0
                else:
                    return 1
        else:
            if f['connections_acked_percentage'] <= 1.597:
                return 1
    else:
        if f['flags'] <= 10:
            if f['connections_from_ip_1_seconds'] <= 39:
                return 0
            else:
                if f['pkt_count_diff'] <= -0.5:
                    return 1
        else:
            if f['time_delta'] <= 0.289:
                return 0
            else:
                if f['time_relative'] <= 0.569:
                    return 1

    return 0

def classify_httpflood(f):
    if f['dstport'] <= 262.5:
        if f['connections_acked_percentage'] <= 1.735:
            if f['inbound'] <= 0.5:
                return 0
            else :
                if f['connections_inbound_pkts_to_ip'] <= 8.5:
                    if f['flags'] <= 9:
                        return 1
                    else: 
                        return 0
                else:
                    return 1
        else:
            if f['srcport'] <= 47706.5:
                return 1
            else: 
                return 0
    else:
        return 0
    
