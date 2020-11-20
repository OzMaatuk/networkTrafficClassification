import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import os
import sys
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
from enum import Enum
import time
import pickle


class PktDirection(Enum):
    not_defined = 0
    client_to_server = 1
    server_to_client = 2


def analyze_pickle(pickle_file_in):
    print("\pickle_file_in : " + pickle_file_in + "\n")
    packets_for_analysis = []

    with open("pickles\\"+pickle_file_in, 'rb') as pickle_fd:
        client_ip_addr_port = pickle.load(pickle_fd)
        server_ip_addr_port = pickle.load(pickle_fd)
        packets_for_analysis = pickle.load(pickle_fd)

    # Plot the receive window size on the client side.
    client_pkts = []

    # TIME-SIZE GRAPH

    for pkt_data in packets_for_analysis:
        # if pkt_data['direction'] == PktDirection.server_to_client:
        #     continue
        # Don't include the SYN packet
        if 'S' in pkt_data['tcp_flags']:
            continue
        client_pkts.append({'Packet Order': pkt_data['ordinal'],
                            'Packet size': pkt_data['tcp_payload_len']})
        # print("ordinal : " + str(pkt_data['ordinal']
        #                          ) + "  at length : " + str(pkt_data['tcp_payload_len']))

    df = pd.DataFrame(data=client_pkts)
    df.plot(x='Packet Order', y='Packet size', color='r')
    # plt.show()
    plt.savefig("pics\\"+pickle_file_in+".png")
    print("\nSaved " + pickle_file_in+".png\n")

    # SIZE HISTOGRAM
    client_pkts = []
    for pkt_data in packets_for_analysis:
        # if pkt_data['direction'] == PktDirection.server_to_client:
        #     continue
        # Don't include the SYN packet
        if 'S' in pkt_data['tcp_flags']:
            continue
        client_pkts.append({'Packet size': pkt_data['tcp_payload_len']})

    df = pd.DataFrame(data=client_pkts)
    df.plot.hist(bins=len(client_pkts))
    # plt.show()
    plt.savefig("pics\\hist_"+pickle_file_in+".png")
    print("\nSaved " + pickle_file_in+".png\n")

    plt.close()


if __name__ == '__main__':
    print("\nanalyze_pickle\n")
    for filename in os.listdir("pickles\\"):
        analyze_pickle(filename)
