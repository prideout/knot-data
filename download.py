#!/usr/bin/python

import urllib

for f in open('indices'):
    index = int(f)
    base = "http://www.colab.sfu.ca/KnotPlot/KnotServer"
    print index

    html = "%d.html" % index
    url1 = "%s/coord/%s" % (base, html)
    urllib.urlretrieve(url1, html)

    jpg = "%d.jpg" % index
    url2 = "%s/inlines/jpg/%s" % (base, jpg)
    urllib.urlretrieve(url2, jpg)
