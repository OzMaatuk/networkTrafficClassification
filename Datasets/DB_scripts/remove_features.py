import sys
import pandas as pd
from numpy.random import RandomState
import numpy as np

# set target lable column from command line argument
target = str(sys.argv[1])  # 'os' , 'browser' , 'app' , 'tuple'

# set data directory path
path = "../"+target + "_dataset/"

# read csv data file
data = pd.read_csv(path+'converted_all_features_'+target+'.csv',
                   sep='\t')

# # print colums values to become categorized and droped
# print('colums values to become categorized and droped')
# print()
# print('fSSLv_1: ' + str(data['fSSLv_1'].unique()))
# print('fSSLv_2: ' + str(data['fSSLv_2'].unique()))
# print('fSSLv_3: ' + str(data['fSSLv_3'].unique()))
# print('fSSLv_4: ' + str(data['fSSLv_4'].unique()))

# print('fcipher_suites_1: ' + str(data['fcipher_suites_1'].unique()))
# print('fcipher_suites_2: ' + str(data['fcipher_suites_2'].unique()))
# print('fcipher_suites_3: ' + str(data['fcipher_suites_3'].unique()))

# print('mean_fttl_1: ' + str(data['mean_fttl_1'].unique()))
# print('mean_fttl_2: ' + str(data['mean_fttl_2'].unique()))
# print()

# new column will group and replace old ones
new_ssl_v = []
new_fcipher_suites = []
new_mean_fttl = []

# removing column due to variance check
data = data.drop(columns=['fSSL_num_compression_methods', 'SYN_MSS'])

# removing columns due to values check
data = data.drop(columns=['min_fiat', 'min_biat'])

# filling the new columns
for i in range(0, data.shape[0]):
    if data['fSSLv_2'][i].item() == 1:
        new_ssl_v.append(2)
    elif data['fSSLv_4'][i].item() == 1:
        new_ssl_v.append(4)
    else:
        new_ssl_v.append(0)
    if data['fcipher_suites_1'][i].item() == 1:
        new_fcipher_suites.append(1)
    elif data['fcipher_suites_2'][i].item() == 1:
        new_fcipher_suites.append(2)
    elif data['fcipher_suites_3'][i].item() == 1:
        new_fcipher_suites.append(3)
    else:
        new_fcipher_suites.append(0)
    if data['mean_fttl_1'][i].item() == 1:
        new_mean_fttl.append(1)
    elif data['mean_fttl_2'][i].item() == 1:
        new_mean_fttl.append(2)
    else:
        new_mean_fttl.append(0)

# converts to np arrays
np_new_ssl_v = np.array(new_ssl_v)
np_new_fcipher_suites = np.array(new_fcipher_suites)
np_new_mean_fttl = np.array(new_mean_fttl)

# # prints new values....
# print("new values")
# print()
# print("new_ssl_v: " + str(np.unique(np_new_ssl_v)))
# print("new_fcipher_suites: " + str(np.unique(np_new_fcipher_suites)))
# print("new_mean_fttl: " + str(np.unique(np_new_mean_fttl)))
# print()

# adds new columns
data['ssl_v'] = np_new_ssl_v
data['fcipher_suites'] = np_new_fcipher_suites
data['mean_fttl'] = np_new_mean_fttl

# droing the grouped columns
data = data.drop(columns=['fSSLv_1', 'fSSLv_2',
                          'fSSLv_3', 'fSSLv_4', 'fcipher_suites_1', 'fcipher_suites_2',
                          'fcipher_suites_3', 'mean_fttl_1', 'mean_fttl_2'])

# write new CSV file
# write all data to file
data.to_csv(path+'new_all_features_'+target +
            '.csv', '\t', index=False)
