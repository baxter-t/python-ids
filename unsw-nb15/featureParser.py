import csv

# with open('NUSW-NB15_features.csv') as features:
#     reader = csv.reader(features, delimiter=',')
#     types = {}
#     for line in reader:
#         types[line[2]] = types.get(line[2], []) + [line[1]]


nominalValues = {
    "proto": [
        "3pc",
        "a/n",
        "aes-sp3-d",
        "any",
        "argus",
        "aris",
        "arp",
        "ax.25",
        "bbn-rcc",
        "bna",
        "br-sat-mon",
        "cbt",
        "cftp",
        "chaos",
        "compaq-peer",
        "cphb",
        "cpnx",
        "crtp",
        "crudp",
        "dcn",
        "ddp",
        "ddx",
        "dgp",
        "egp",
        "eigrp",
        "emcon",
        "encap",
        "etherip",
        "fc",
        "fire",
        "ggp",
        "gmtp",
        "gre",
        "hmp",
        "i-nlsp",
        "iatp",
        "ib",
        "icmp",
        "idpr",
        "idpr-cmtp",
        "idrp",
        "ifmp",
        "igmp",
        "igp",
        "il",
        "ip",
        "ipcomp",
        "ipcv",
        "ipip",
        "iplt",
        "ipnip",
        "ippc",
        "ipv6",
        "ipv6-frag",
        "ipv6-no",
        "ipv6-opts",
        "ipv6-route",
        "ipx-n-ip",
        "irtp",
        "isis",
        "iso-ip",
        "iso-tp4",
        "kryptolan",
        "l2tp",
        "larp",
        "leaf-1",
        "leaf-2",
        "merit-inp",
        "mfe-nsp",
        "mhrp",
        "micp",
        "mobile",
        "mtp",
        "mux",
        "narp",
        "netblt",
        "nsfnet-igp",
        "nvp",
        "ospf",
        "pgm",
        "pim",
        "pipe",
        "pnni",
        "pri-enc",
        "prm",
        "ptp",
        "pup",
        "pvp",
        "qnx",
        "rdp",
        "rsvp",
        "rtp",
        "rvd",
        "sat-expak",
        "sat-mon",
        "sccopmce",
        "scps",
        "sctp",
        "sdrp",
        "secure-vmtp",
        "sep",
        "skip",
        "sm",
        "smp",
        "snp",
        "sprite-rpc",
        "sps",
        "srp",
        "st2",
        "stp",
        "sun-nd",
        "swipe",
        "tcf",
        "tcp",
        "tlsp",
        "tp++",
        "trunk-1",
        "trunk-2",
        "ttp",
        "udp",
        "unas",
        "uti",
        "vines",
        "visa",
        "vmtp",
        "vrrp",
        "wb-expak",
        "wb-mon",
        "wsn",
        "xnet",
        "xns-idp",
        "xtp",
        "zero",
    ],
    "service": [
        "-",
        "dhcp",
        "dns",
        "ftp",
        "ftp-data",
        "http",
        "irc",
        "pop3",
        "radius",
        "smtp",
        "snmp",
        "ssh",
        "ssl",
    ],
    "state": [
        "ACC",
        "CLO",
        "CON",
        "ECO",
        "FIN",
        "INT",
        "PAR",
        "REQ",
        "RST",
        "URN",
        "no",
    ],
    "attack_cat": [
        "Analysis",
        "Backdoor",
        "DoS",
        "Exploits",
        "Fuzzers",
        "Generic",
        "Normal",
        "Reconnaissance",
        "Shellcode",
        "Worms",
    ],
}

for nom in nominalValues:
    nominalValues[nom] = sorted(nominalValues[nom])


with open("UNSW_NB15_training-set.csv") as trainingSet:
    with open("UNSW_NB15_training-set_processed.csv", "w") as output:

        count = 0
        first = True
        reader = csv.DictReader(trainingSet, delimiter=",")

        for line in reader:
            if first:
                first = False
                writer = csv.DictWriter(output, fieldnames=line.keys())
                writer.writeheader()

            for field in nominalValues:
                line[field] = nominalValues[field].index(line[field])

            writer.writerow(line)

            count += 1


print("< || Mappings Used || >")
print()
for m in nominalValues:
    print("Mapping for field: {}".format(m))
    for i, x in enumerate(nominalValues[m]):
        print("    {} -> {}".format(i, x))
    print()
