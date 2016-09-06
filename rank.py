#!/usr/bin/python

import argparse, fileinput, numpy
from support.data import read_data


if __name__ == '__main__':
	options = argparse.ArgumentParser(description='Rank lines by specified column.')
	options.add_argument('-f', '--field', type=int, default=1, help='which column to rank on')
	options.add_argument('-d', '--delimiter', type=str, default='\t', help='column delimiter')
	options.add_argument('-n', '--num-returned', type=int, default=float('inf'), help='limit number of returned lines')
	options.add_argument('-o', '--order', choices=['asc', 'desc'], default='desc', help='ascending or descending order')
	options.add_argument('files', nargs='*', help='files to read; if empty, use stdin')
	args = options.parse_args()

	ins = fileinput.input(files=args.files if len(args.files) > 0 else ('-', ))
	lines, elements = read_data(ins, args.delimiter, args.field)

	ranks = numpy.array(elements).argsort()
	if args.order == 'desc':
		ranks = ranks[::-1]
	for i in range(min(len(ranks), args.num_returned)):
		print(lines[ranks[i]])
