import pyshark
import mappings

'''
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
'''

cap = pyshark.LiveCapture(interface='en0', bpf_filter='ip')

sbytes_history = {}

def print_callback(pkt):
    print(pkt)
        

cap.apply_on_packets(print_callback)

