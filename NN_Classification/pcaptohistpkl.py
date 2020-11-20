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
from collections import Counter


class PktDirection(Enum):
    not_defined = 0
    client_to_server = 1
    server_to_client = 2


def printable_timestamp(ts, resol=1):
    ts_sec = ts // resol
    ts_subsec = ts % resol
    ts_sec_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts_sec))
    return '{}.{}'.format(ts_sec_str, ts_subsec)


def pickle_pcap(pcap_file_in):
    print("\n\n\n")
    print('Processing {}...'.format(pcap_file_in))

    MTU = 3000
    file_name = pcap_file_in
    record_info_index_eliminator = "TCP_"
    # find record_info_end_index
    record_info_end_index = file_name.find(
        record_info_index_eliminator)
    # split to record info and record connection
    record_connection = file_name[record_info_end_index:]
    file_name = file_name[:record_info_end_index-1]

    # exporting connection detals
    end_indx = record_connection.find("_")
    record_connection = record_connection[end_indx+1:]
    print("record_connection : " + record_connection)
    print("file_name : " + file_name)
    end_indx = record_connection.find("_")
    client_ip = record_connection[:end_indx].replace("-", ".")
    record_connection = record_connection[end_indx+1:]
    end_indx = record_connection.find("_")
    client_port = record_connection[:end_indx]
    record_connection = record_connection[end_indx+1:]
    end_indx = record_connection.find("_")
    server_ip = record_connection[:end_indx].replace("-", ".")
    record_connection = record_connection[end_indx+1:]
    end_indx = record_connection.find("_")
    server_port = str(443)

    client = client_ip+":"+client_port
    server = server_ip+":"+server_port

    count = 0
    interesting_packet_count = 0
    first_pkt_ordinal = 1
    last_pkt_ordinal = 2
    first_pkt_timestamp = 0
    last_pkt_timestamp = 60

    packets_for_analysis = Counter()
    # for i in range(0, MTU):
    #     packets_for_analysis.append(0)

    for (pkt_data, pkt_metadata,) in RawPcapReader("pcaps\\"+pcap_file_in):
        count += 1

        # collecting packet info

        ether_pkt = Ether(pkt_data)
        if 'type' not in ether_pkt.fields:
            # LLC frames will have 'len' instead of 'type'.
            # We disregard those
            continue

        if ether_pkt.type != 0x0800:
            # disregard non-IPv4 packets
            continue

        ip_pkt = ether_pkt[IP]

        if ip_pkt.proto != 6:
            # Ignore non-TCP packet
            continue

        tcp_pkt = ip_pkt[TCP]
        direction = PktDirection.not_defined

        # settting packet direction
        if ip_pkt.src == client_ip:
            if tcp_pkt.sport != int(client_port):
                continue
            if ip_pkt.dst != server_ip:
                continue
            if tcp_pkt.dport != int(server_port):
                continue
            direction = PktDirection.client_to_server
        elif ip_pkt.src == server_ip:
            if tcp_pkt.sport != int(server_port):
                continue
            if ip_pkt.dst != client_ip:
                continue
            if tcp_pkt.dport != int(client_port):
                continue
            direction = PktDirection.server_to_client
        else:
            continue

        # counting the packet (divided to relevant session packets and not)
        interesting_packet_count += 1
        if interesting_packet_count == 1:
            first_pkt_timestamp = (pkt_metadata.sec)
            first_pkt_ordinal = count

        # setting timestamp and packet oreder index
        last_pkt_timestamp = (pkt_metadata.sec+(pkt_metadata.usec))
        last_pkt_ordinal = count

        # Determine the TCP payload length. IP fragmentation will mess up this
        # logic, so first check that this is an unfragmented packet
        if (ip_pkt.flags == 'MF') or (ip_pkt.frag != 0):
            print('No support for fragmented IP packets')
            return False

        # tcp_payload_len = ip_pkt.len - \
        #     (ip_pkt.ihl * 4) - (tcp_pkt.dataofs * 4)

        # count packet size
        # if (tcp_payload_len >= MTU):
        #     print("\n--------------- Packet " + str(count) +
        #           " at size : " + str(tcp_payload_len) + " -----------------\n")
        # else:
        #     packets_for_analysis[tcp_payload_len] += 1
        packets_for_analysis[int(ip_pkt.len)] += 1
# ---
    print('{} contains {} packets ({} interesting)'.
          format(file_name, count, interesting_packet_count))
    print('First packet in connection: Packet #{} {}'.
          format(first_pkt_ordinal,
                 printable_timestamp(first_pkt_timestamp)))
    print('Last packet in connection: Packet #{} {}'.
          format(last_pkt_ordinal,
                 printable_timestamp(last_pkt_timestamp)))
    return packets_for_analysis
# ---


if __name__ == '__main__':
    number_of_files = 500
    pickle_file_out = "all_pcaps.pickle"
    pickle_array = []
    files_list = sorted(os.listdir("pcaps"))
    for file_name in files_list:

        record_info_index_eliminator = "TCP_"
        # find record_info_end_index
        record_info_end_index = file_name.find(
            record_info_index_eliminator)
        # split to record info and record connection
        filename = file_name
        file_name = file_name[:record_info_end_index-1].lower()

        end_indx = file_name.find("_")
        os_type = file_name[:end_indx]
        file_name = file_name[end_indx+1:]

        end_indx = file_name.find("_")
        browser_type = file_name[:end_indx]
        file_name = file_name[end_indx+1:]

        end_indx = file_name.find("_")
        browser_type = file_name[:end_indx]
        file_name = file_name[end_indx+1:]

        current_label = os_type + "_" + browser_type

        tmp = pickle_pcap(filename)
        pickle_array.append(
            {"filename": filename, "Label": current_label, "PktsHist": tmp})

        print('file number : ' + str(number_of_files))
        if (number_of_files > 0):
            number_of_files -= 1
        else:
            break
    # ---
    print('Writing pickle file {}...'.format(pickle_file_out), end='')
    with open("hist_pickles\\"+pickle_file_out, 'wb') as pickle_fd:
        pickle.dump(pickle_array, pickle_fd)
    print('done.')
