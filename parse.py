#!/usr/bin/python

import re, glob, shutil

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
    name = ""
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
    if name == "":
        print "No name in ", html
        continue
    links[name] = components
    files[name] = html
    infile.close()

# We want 9 columns, 12 rows:

tableDesc = """
0 1
3 1
4 1
5 2
6 3
7 7
8 21
9 36
--
0 1
2 1
4 1
5 1
6 3
7 8
8 11
--
0 1
6 3
7 1
8 5
"""
table = tableDesc.split('--')

descout = open("knots.coffee", "w")
descout.write("root = exports ? this\n\n")
descout.write("root.links = [\n")
vertCount, linkCount = 0, 0
for numComponents in xrange(1, 4):
    for link in table[numComponents-1].strip().split('\n'):
        crossings, count = map(int, link.split())
        for index in xrange(1,count+1):
            if numComponents > 1:
                key = "%d.%d.%d" % (crossings, numComponents, index)
            else:
                key = "%d.%d" % (crossings, index)
            if not key in links:
                print key, "missing"
                descout.write('  ["%s"]\n' % key)
                continue
            linkData = ', '.join(str(x) for x in links[key])
            descout.write('  ["%s", %s]\n' % (key, linkData))
            linkCount = linkCount + 1

descout.write("]\n")
print linkCount, "links dumped to knots.coffee"

binout = open("centerlines.bin", "wb")
import ctypes, struct
s = struct.Struct('fff')
vertCount = len(coords)
b = ctypes.create_string_buffer(s.size * vertCount)
offset = 0
for c in coords:
    s.pack_into(b, offset, *c)
    offset = offset + 12
binout.write(b)
print vertCount, "verts dumped to centerlines.bin"
