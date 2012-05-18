#!/usr/bin/python

import re, glob

binout = open("centerlines.bin", "wb")
descout = open("knots.coffee", "w")

briggs = re.compile("^[0-9]+\.[0-9]+(\.[0-9]+)?$")
coord = re.compile("^(\-?\d+(\.\d*)?)\s(\-?\d+(\.\d*)?)\s(\-?\d+(\.\d*)?)$")
separator = re.compile("^$")

links = {}
coords = []
files = {}

for html in glob.glob("*.html"):
    infile = open(html, "r")
    components = []
    span = [len(coords),0] # [starting index, # of indices]
    for line in infile:
        m = coord.match(line)
        if m:
            x = float(m.group(1))
            y = float(m.group(2))
            z = float(m.group(3))
            coords.append((x,y,z))
        elif briggs.match(line):
            name = line.strip()
        elif separator.match(line):
            span[1] = len(coords) - span[0]
            components.append(span[:])
            span[0] = len(coords)

    span[1] = len(coords) - span[0]
    components.append(span)
    links[name] = components
    files[name] = html
    infile.close()

print "8.20 = ", links["8.20"], files["8.20"]
print "8.3.2 = ", links["8.3.2"], files["8.3.2"]

# We want 9 columns, 12 rows:

single_component_links  = """
0 1
3 1
4 1
5 2
6 3
7 7
8 21
9 36
"""

two_component_links = """
0 1
2 1
4 1
5 1
6 3
7 8
8 11
"""

three_component_links = """
0 1
6 3
7 1
8 5
"""
