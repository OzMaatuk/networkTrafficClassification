#!/usr/bin/python3

import sys
import pandas as pd
from numpy.random import RandomState
import numpy as np

# set target lable column
# target = 'os'  # 'os' , 'browser' , 'app' , 'tuple'

# set target lable column from command line argument
target = str(sys.argv[1])

# set data directory path
path = "../"+target + "_dataset/"

# read csv data file
data = pd.read_csv(path+'all_features_'+target+'.csv',
                   sep='\t',
                   header=None)

# delete row one which includes clm indx
data = data.iloc[1:, ]

# setting clm lables as features
data = data.rename(columns={0: 'fSSL_session_id_len',
                            1: 'fSSL_num_extensions',
                            2: 'fSSL_num_compression_methods',
                            3: 'SYN_tcp_scale',
                            4: 'SYN_MSS',
                            5: 'SYN_tcp_winsize',
                            6: 'fcipher_suites_1',
                            7: 'fcipher_suites_2',
                            8: 'fcipher_suites_3',
                            9: 'fSSLv_1',
                            10: 'fSSLv_2',
                            11: 'fSSLv_3',
                            12: 'fSSLv_4',
                            13: 'size_histogram_1',
                            14: 'size_histogram_2',
                            15: 'size_histogram_3',
                            16: 'size_histogram_4',
                            17: 'size_histogram_5',
                            18: 'size_histogram_6',
                            19: 'size_histogram_7',
                            20: 'size_histogram_8',
                            21: 'size_histogram_9',
                            22: 'size_histogram_10',
                            23: 'fpeak_features_1',
                            24: 'fpeak_features_2',
                            25: 'fpeak_features_3',
                            26: 'fpeak_features_4',
                            27: 'fpeak_features_5',
                            28: 'fpeak_features_6',
                            29: 'fpeak_features_7',
                            30: 'fpeak_features_8',
                            31: 'fpeak_features_9',
                            32: 'bpeak_features_1',
                            33: 'bpeak_features_2',
                            34: 'bpeak_features_3',
                            35: 'bpeak_features_4',
                            36: 'bpeak_features_5',
                            37: 'bpeak_features_6',
                            38: 'bpeak_features_7',
                            39: 'bpeak_features_8',
                            40: 'bpeak_features_9',
                            41: 'packet_count',
                            42: 'min_packet_size',
                            43: 'max_packet_size',
                            44: 'mean_packet_size',
                            45: 'sizevar',
                            46: 'std_fiat',
                            47: 'fpackets',
                            48: 'bpackets',
                            49: 'fbytes',
                            50: 'bbytes',
                            51: 'min_fiat',
                            52: 'min_biat',
                            53: 'max_fiat',
                            54: 'max_biat',
                            55: 'std_biat',
                            56: 'mean_fiat',
                            57: 'mean_biat',
                            58: 'min_fpkt',
                            59: 'min_bpkt',
                            60: 'max_fpkt',
                            61: 'max_bpkt',
                            62: 'std_fpkt',
                            63: 'std_bpkt',
                            64: 'mean_fpkt',
                            65: 'mean_bpkt',
                            66: 'mean_fttl_1',
                            67: 'mean_fttl_2',
                            68: 'num_keep_alive',
                            69: target})

# write all data to file
data.to_csv(path+'all_features_'+target+'.csv', '\t', index=False)
