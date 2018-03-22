#!/usr/bin/python

import sys
from ttest import print_ttest as ttest


def read(f):
	d = {}
	for line in f:
		line = line.split()
		query, score = line[0], float(line[1])
		if query != 'all':
			d[query] = score
	return [value for (key, value) in sorted(d.items())]

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Supply two data files')
		exit()

	d1_file = sys.argv[1]
	d2_file = sys.argv[2]

	with open(d1_file) as f:
		d1 = read(f)

	with open(d2_file) as f:
		d2 = read(f)

	ttest(d1, d2, False)
