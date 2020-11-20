#!/usr/bin/python3
import sys

file_name = str(sys.argv[1])
output = "original number of errors: "
with open(file_name+".html", "r") as f:
    for line in f.readlines():
        if "<pre>current column is :" in line:
            output = output+line[25:len(line)-1]+","
        if "<pre>Number of error:" in line:
            output = output+" : "+line[22:26]+"\n"
f = open(file_name+"_scores.txt", "w+")
f.write(output)
