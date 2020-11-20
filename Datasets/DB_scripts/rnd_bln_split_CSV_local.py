#!/usr/bin/python3

import sys
import pandas as pd
from numpy.random import RandomState
import numpy as np

# set target lable column from command line argument
# target = str(sys.argv[1])  # 'os' , 'browser' , 'app' , 'tuple'
# file_name = 'new_all_features_'


def split_CSV_randomly_balanced(in_target, in_file_name):
    # set input parameters
    target = in_target
    file_name = in_file_name

    # set data directory path
    path = "../"+target + "_dataset/"

    # read csv data file
    data = pd.read_csv(path+file_name+target+'.csv',
                       sep='\t')

    # write all data to file
    data.to_csv(path+file_name+target+'.csv', '\t', index=False)

    # ----------------------------------------------------------------
    # making the splits balanced
    # ----------------------------------------------------------------

    # get column values
    values = data[target].unique()

    # initilize map of dataframes for any value of the target
    data_map = {}
    for i in values:
        data_map[int(i)] = data.loc[data[target] == int(i)]

    # ----------------------------------------------------------------
    # randomly spliting
    # ----------------------------------------------------------------

    train_const = 0.7

    train_data = pd.DataFrame()
    test_data = pd.DataFrame()
    for i in values:
        rng = RandomState()
        tmp_train = data_map[int(i)].sample(frac=train_const, random_state=rng)
        tmp_test = data_map[int(i)].loc[~data_map[int(i)
                                                  ].index.isin(tmp_train.index)]
        train_data = train_data.append(tmp_train)
        test_data = test_data.append(tmp_test)

    # make randomly new data any time
    # rng = RandomState()
    # train = data.sample(frac=0.7, random_state=rng)
    # test_data = data.loc[~data.index.isin(train.index)]

    # ----------------------------------------------------------------
    # varification...
    # ----------------------------------------------------------------

    # # create map for original data values
    # count_map = {}
    # for i in values:
    #     count_map[i] = int(0)

    # # count values on the map
    # for i in data[target]:
    #     count_map[i] = count_map[i] + 1

    # # create map for train values
    # count_train_map = {}
    # for i in values:
    #     count_train_map[i] = int(0)

    # # count values in train
    # for i in train_data[target]:
    #     count_train_map[i] = count_train_map[i] + 1

    # # create map for test data values
    # count_test_map = {}
    # for i in values:
    #     count_test_map[i] = int(0)

    # # count values in test
    # for i in test_data[target]:
    #     count_test_map[i] = count_test_map[i] + 1

    # # print varification
    # for i in values:
    #     print("values of " + str(i) + " : in original : " +
    #           str(count_map[i]) + " in train : " + str(count_train_map[i]) + " in test : " +
    #           str(count_test_map[i]) + " " + str(count_train_map[i]) + " + " + str(count_test_map[i]) + " = " +
    #           str(count_train_map[i]+count_test_map[i]))

    # write a train set file
    train_data.to_csv(path+file_name+target+'_train.csv', '\t', index=False)

    # write the test set answers by row index
    # test_data['org_ind'] = np.arange(len(test_data))
    # answers = test_data[['org_ind', target]].copy()
    # answers.to_csv(path+'all_features_'+target+'_answers.csv', '\t', index=False)

    # write a test set file
    # test_data = test_data.drop(columns=[target])
    test_data.to_csv(
        path+file_name+target+'_test.csv', '\t', index=False)


if __name__ == "__main__":
    pass  # split_CSV_randomly_balanced('tuple', 'new_all_features_')
