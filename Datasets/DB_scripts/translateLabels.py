import numpy as np

def translate(label):
    os = label % 10
    browser = (label % 1000) / 100
    app = (label % 10000) / 1000
    return int(os), int(browser), int(app)

#########################################


def transformer(label, os_flag, browser_flag, app_flag):
    os, browser, app = translate(label)
    new_label = (os_flag*os) + (browser_flag*100*browser) + (app_flag*1000*app)
    # print 'new label: ' + repr(new_label)
    return int(new_label)

##########################################


def transform_labels(y, os_flag=0, browser_flag=0, app_flag=0):
    return [ transformer(label, os_flag=os_flag, browser_flag=browser_flag, app_flag=app_flag) for label in y ]
    # return [ 0 for label in y ]

###########################################


def transform_to_os_labels(y):
    return transform_labels(y, os_flag=1, browser_flag=0, app_flag=0)

def transform_to_browser_labels(y):
    return transform_labels(y, os_flag=0, browser_flag=1, app_flag=0)

def transform_to_app_labels(y):
    return transform_labels(y, os_flag=0, browser_flag=0, app_flag=1)

def transform_to_os_browser_labels(y):
    return transform_labels(y, os_flag=1, browser_flag=1, app_flag=0)

def transform_to_os_app_labels(y):
    return transform_labels(y, os_flag=1, browser_flag=0, app_flag=1)

def transform_to_browser_app_labels(y):
    return transform_labels(y, os_flag=0, browser_flag=1, app_flag=1)

##########################################
