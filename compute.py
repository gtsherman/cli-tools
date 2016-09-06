#!/usr/bin/python

import argparse, fileinput, numpy
from support.data import read_data


if __name__ == '__main__':
	# Computable
	MEAN = 'mean'
	MEDIAN = 'median'
	MAX = 'max'
	MIN = 'min'
	SUM = 'sum'

	# Parse arguments
	options = argparse.ArgumentParser(description='Compute simple metrics.')
	required = options.add_argument_group('required arguments')
	required.add_argument('-m', '--measure', choices=[MEAN, MEDIAN, MAX, MIN, SUM], help='the measure to use', required=True)
	options.add_argument('-f', '--field', type=int, default=1, help='which field to use for computing')
	options.add_argument('-d', '--delimiter', type=str, default='\t', help='value delimiter')
	options.add_argument('-w', '--which', action='store_true', help='return which line matches the computation')
	options.add_argument('files', nargs='*', help='files to read; if empty, use stdin')
	args = options.parse_args()

	# Compute options
	switcher = {
		MEAN: numpy.mean,
		MEDIAN: numpy.median,
		MAX: max,
		MIN: min,
		SUM: sum
	}

	# Collect the data
	ins = fileinput.input(files=args.files if len(args.files) > 0 else ('-', ))
	lines, elements = read_data(ins, args.delimiter, args.field)

	if len(elements) > 0:
		result = switcher.get(args.measure)(elements)
		if args.which and not args.measure == MEAN:
			for line in numpy.where(numpy.array(elements) == result):
				for l in line:
					print(lines[l])
		else:
			print(result)
	else:
		print('No data successfully read.')
