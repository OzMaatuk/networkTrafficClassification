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


def printable_timestamp(ts, resol=1):
    ts_sec = ts // resol
    ts_subsec = ts % resol
    ts_sec_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts_sec))
    return '{}.{}'.format(ts_sec_str, ts_subsec)


def pickle_pcap(pcap_file_in, pickle_file_out):
    print("\n\n\n")
    print('Processing {}...'.format(pcap_file_in))

    file_name = pcap_file_in[0]
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

    print("file_name : " + file_name)
    print("client_ip : " + client_ip)
    print("client_port : " + client_port)
    print("server_ip : " + server_ip)

    client = client_ip+":"+client_port
    server = server_ip+":"+server_port

    count = 0
    interesting_packet_count = 0
    first_pkt_ordinal = 1
    last_pkt_ordinal = 2
    first_pkt_timestamp = 0
    last_pkt_timestamp = 60
    # server_sequence_offset = None
    # client_sequence_offset = None

    # List of interesting packets, will finally be pickled.
    # Each element of the list is a dictionary that contains fields of interest
    # from the packet.
    packets_for_analysis = []

    for cur_pcap in pcap_file_in:
        print("current pcap file : " + cur_pcap)
        for (pkt_data, pkt_metadata,) in RawPcapReader("pcaps\\"+cur_pcap):
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

            # if direction == PktDirection.client_to_server:
            #     if client_sequence_offset is None:
            #         client_sequence_offset = tcp_pkt.seq
            #     relative_offset_seq = tcp_pkt.seq - client_sequence_offset
            # else:
            #     assert direction == PktDirection.server_to_client
            #     if server_sequence_offset is None:
            #         server_sequence_offset = tcp_pkt.seq
            #     relative_offset_seq = tcp_pkt.seq - server_sequence_offset

            # If this TCP packet has the Ack bit set, then it must carry an ack
            # number.
            # if 'A' not in str(tcp_pkt.flags):
            #     relative_offset_ack = 0
            # else:
            #     if direction == PktDirection.client_to_server:
            #         if server_sequence_offset is None:
            #             server_sequence_offset = tcp_pkt.seq
            #         relative_offset_ack = tcp_pkt.ack - server_sequence_offset
            #     else:
            #         if client_sequence_offset is None:
            #             client_sequence_offset = tcp_pkt.seq
            #         relative_offset_ack = tcp_pkt.ack - client_sequence_offset

            # Determine the TCP payload length. IP fragmentation will mess up this
            # logic, so first check that this is an unfragmented packet
            if (ip_pkt.flags == 'MF') or (ip_pkt.frag != 0):
                print('No support for fragmented IP packets')
                return False

            tcp_payload_len = ip_pkt.len - \
                (ip_pkt.ihl * 4) - (tcp_pkt.dataofs * 4)

            # Look for the 'Window Scale' TCP option if this is a SYN or SYN-ACK
            # packet.
            # if 'S' in str(tcp_pkt.flags):
            #     for (opt_name, opt_value,) in tcp_pkt.options:
            #         if opt_name == 'WScale':
            #             if direction == PktDirection.client_to_server:
            #                 client_recv_window_scale = opt_value
            #             else:
            #                 server_recv_window_scale = opt_value
            #             break

            # Create a dictionary and populate it with data that we'll need in the
            # analysis phase.

            pkt_data = {}
            pkt_data['direction'] = direction
            pkt_data['ordinal'] = last_pkt_ordinal
            pkt_data['relative_timestamp'] = pkt_metadata.sec - \
                first_pkt_timestamp
            pkt_data['tcp_flags'] = str(tcp_pkt.flags)
            # pkt_data['seqno'] = relative_offset_seq
            # pkt_data['ackno'] = relative_offset_ack
            pkt_data['tcp_payload_len'] = tcp_payload_len
            # if direction == PktDirection.client_to_server:
            #     pkt_data['window'] = tcp_pkt.window << client_recv_window_scale
            # else:
            #     pkt_data['window'] = tcp_pkt.window << server_recv_window_scale
            # pkt_data['window'] = pkt_metadata.caplen
            # print("tcp_payload_len : " + str(tcp_payload_len))
            # print("ordinal : " + str(last_pkt_ordinal))
            packets_for_analysis.append(pkt_data)
    # ---
    print('{} contains {} packets ({} interesting)'.
          format(file_name, count, interesting_packet_count))

    print('First packet in connection: Packet #{} {}'.
          format(first_pkt_ordinal,
                 printable_timestamp(first_pkt_timestamp)))
    print('Last packet in connection: Packet #{} {}'.
          format(last_pkt_ordinal,
                 printable_timestamp(last_pkt_timestamp)))

    print('Writing pickle file {}...'.format(pickle_file_out), end='')
    with open("pickles\\"+pickle_file_out, 'wb') as pickle_fd:
        pickle.dump(client, pickle_fd)
        pickle.dump(server, pickle_fd)
        pickle.dump(packets_for_analysis, pickle_fd)
    print('done.')

# ---


if __name__ == '__main__':
    files_list = sorted(os.listdir("pcaps"))
    for filename in files_list:
        pickle_pcap([filename], filename)
