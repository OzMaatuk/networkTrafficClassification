#!/usr/bin/env python

from translateLabels import transform_to_os_labels, transform_to_browser_labels, transform_to_app_labels
import pandas as pd
import os
import copy

if __name__ == "__main__":
    # read csv
    path = "../"
    csv_file = path+'samples_25.2.16_all_features_triple.csv'
    ds = pd.read_csv(csv_file, sep='\t', header=None, skiprows=[0])

    # idk
    labels_column = len(ds.columns)-1
    ds[labels_column] = ds[labels_column].astype(int)
    # not doing anything
    ds_app = ds_browser = ds_os = ds

    # copy last column as y
    y_triple = copy.deepcopy(ds[labels_column])

    # set last column for os
    ds[labels_column] = transform_to_os_labels(y_triple)
    ds.to_csv(path+'os_dataset/all_features_os.csv',
              sep='\t', index=False)

    # set last column for browser
    ds[labels_column] = transform_to_browser_labels(y_triple)
    ds.to_csv(path+'browser_dataset/all_features_browser.csv',
              sep='\t', index=False)

    # set last column for app
    ds[labels_column] = transform_to_app_labels(y_triple)
    ds.to_csv(path+'app_dataset/all_features_app.csv',
              sep='\t', index=False)
