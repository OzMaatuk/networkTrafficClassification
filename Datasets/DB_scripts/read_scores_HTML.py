#!/usr/bin/python3
import sys

file_name = str(sys.argv[1])
output = ""
with open(file_name+".html", "r") as f:
    for line in f.readlines():
        if "class=\"data row0 col1\"" in line:
            output = output+line
f = open(file_name+".txt", "w+")
f.write(output)
