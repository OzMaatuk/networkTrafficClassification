import sys
import pandas as pd
from numpy.random import RandomState
import numpy as np

# set target lable column from command line argument
target = str(sys.argv[1])  # 'os' , 'browser' , 'app' , 'tuple'

# set data directory path
path = "../"+target + "_dataset/"

# read csv data file
data = pd.read_csv(path+'all_features_'+target+'.csv',
                   sep='\t')

data['fSSL_session_id_len'] = pd.to_numeric(
    data['fSSL_session_id_len'], downcast='signed')
data['fSSL_num_extensions'] = pd.to_numeric(
    data['fSSL_num_extensions'], downcast='signed')
data['fSSL_num_compression_methods'] = pd.to_numeric(
    data['fSSL_num_compression_methods'], downcast='signed')
data['SYN_tcp_scale'] = pd.to_numeric(data['SYN_tcp_scale'], downcast='signed')
data['SYN_MSS'] = pd.to_numeric(data['SYN_MSS'], downcast='signed')
data['SYN_tcp_winsize'] = pd.to_numeric(
    data['SYN_tcp_winsize'], downcast='signed')
data['fcipher_suites_1'] = pd.to_numeric(
    data['fcipher_suites_1'], downcast='signed')
data['fcipher_suites_2'] = pd.to_numeric(
    data['fcipher_suites_2'], downcast='signed')
data['fcipher_suites_3'] = pd.to_numeric(
    data['fcipher_suites_3'], downcast='signed')
data['fSSLv_1'] = pd.to_numeric(data['fSSLv_1'], downcast='signed')
data['fSSLv_2'] = pd.to_numeric(data['fSSLv_2'], downcast='signed')
data['fSSLv_3'] = pd.to_numeric(data['fSSLv_3'], downcast='signed')
data['fSSLv_4'] = pd.to_numeric(data['fSSLv_4'], downcast='signed')
data['size_histogram_1'] = pd.to_numeric(
    data['size_histogram_1'], downcast='signed')
data['size_histogram_2'] = pd.to_numeric(
    data['size_histogram_2'], downcast='signed')
data['size_histogram_3'] = pd.to_numeric(
    data['size_histogram_3'], downcast='signed')
data['size_histogram_4'] = pd.to_numeric(
    data['size_histogram_4'], downcast='signed')
data['size_histogram_5'] = pd.to_numeric(
    data['size_histogram_5'], downcast='signed')
data['size_histogram_6'] = pd.to_numeric(
    data['size_histogram_6'], downcast='signed')
data['size_histogram_7'] = pd.to_numeric(
    data['size_histogram_7'], downcast='signed')
data['size_histogram_8'] = pd.to_numeric(
    data['size_histogram_8'], downcast='signed')
data['size_histogram_9'] = pd.to_numeric(
    data['size_histogram_9'], downcast='signed')
data['size_histogram_10'] = pd.to_numeric(
    data['size_histogram_10'], downcast='signed')
data['fpeak_features_2'] = pd.to_numeric(
    data['fpeak_features_2'], downcast='signed')
data['fpeak_features_3'] = pd.to_numeric(
    data['fpeak_features_3'], downcast='signed')
data['fpeak_features_5'] = pd.to_numeric(
    data['fpeak_features_5'], downcast='signed')
data['bpeak_features_2'] = pd.to_numeric(
    data['bpeak_features_2'], downcast='signed')
data['bpeak_features_3'] = pd.to_numeric(
    data['bpeak_features_3'], downcast='signed')
data['bpeak_features_5'] = pd.to_numeric(
    data['bpeak_features_5'], downcast='signed')
data['packet_count'] = pd.to_numeric(data['packet_count'], downcast='signed')
data['min_packet_size'] = pd.to_numeric(
    data['min_packet_size'], downcast='signed')
data['max_packet_size'] = pd.to_numeric(
    data['max_packet_size'], downcast='signed')
data['fpackets'] = pd.to_numeric(data['fpackets'], downcast='signed')
data['bpackets'] = pd.to_numeric(data['bpackets'], downcast='signed')
data['fbytes'] = pd.to_numeric(data['fbytes'], downcast='signed')
data['bbytes'] = pd.to_numeric(data['bbytes'], downcast='signed')
data['min_fiat'] = pd.to_numeric(data['min_fiat'], downcast='signed')
data['min_biat'] = pd.to_numeric(data['min_biat'], downcast='signed')
data['min_fpkt'] = pd.to_numeric(data['min_fpkt'], downcast='signed')
data['min_bpkt'] = pd.to_numeric(data['min_bpkt'], downcast='signed')
data['max_fpkt'] = pd.to_numeric(data['max_fpkt'], downcast='signed')
data['max_bpkt'] = pd.to_numeric(data['max_bpkt'], downcast='signed')
data['mean_fttl_1'] = pd.to_numeric(data['mean_fttl_1'], downcast='signed')
data['mean_fttl_2'] = pd.to_numeric(data['mean_fttl_2'], downcast='signed')
data['num_keep_alive'] = pd.to_numeric(
    data['num_keep_alive'], downcast='signed')

# write all data to file
data.to_csv(path+'converted_all_features_'+target+'.csv', '\t', index=False)
