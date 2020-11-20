import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
import pickle


def analyze_pickle(pickle_file_in):
    index = 0
    print("pickle_file_in : " + pickle_file_in + "\n")
    with open(pickle_file_in, 'rb') as pickle_fd:
        packets_for_analysis = pickle.load(pickle_fd)
    # for any object in picle file
    # each object represent a recorded session packet size histogram
    for pickle_object in packets_for_analysis:
        index += 1
        filename = pickle_object['filename']
        client_pkts = pickle_object['PktsHist']
        plt.bar(x=client_pkts.keys(), height=client_pkts.values(),
                width=13, color='black')
        plt.xlabel('Packet Size')
        plt.ylabel('# Packets')
        plt.title('Samples Num' + str(index) +
                  "Label : " + str(pickle_object['Label']))
        plt.savefig("hist_pics\\"+str(filename)+".png")
        plt.close()
        print("\nSaved "+str(filename)+".png\n")


if __name__ == '__main__':
    print("\nanalyze_hist_pickle\n")
    analyze_pickle("hist_pickles\\all_pcaps.pickle")
