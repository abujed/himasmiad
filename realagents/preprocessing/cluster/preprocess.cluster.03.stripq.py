#!/usr/bin/python

import re, sys

# put however many of these: '?', that there are that need to be gotten rid of
q = "'?','?'"

with open(sys.argv[1]) as infile, open(sys.argv[1].strip("arff")+"noq.arff", 'w') as outfile:
	for line in infile:
		if q not in line:
			outfile.write(line)
