import os
from pcaptopkl import pickle_pcap
from anlzpkl import analyze_pickle
import time

directory = 'pcaps'

for filename in os.listdir(directory):
    if filename.endswith(".pcap"):
        print(filename)
    output_file = filename[:-4]+'pickle'
    pickle_pcap(directory + '\\'+filename, output_file)
    time.sleep(2.4)
    analyze_pickle(output_file)
