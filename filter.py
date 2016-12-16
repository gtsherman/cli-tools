#!/usr/bin/python

import argparse, fileinput


if __name__ == '__main__':
	options = argparse.ArgumentParser(description='Filter.')
	required = options.add_argument_group('required arguments')
	required.add_argument('-f', '--field', type=int, help='which field to filter on')
	options.add_argument('-g', '--greater', type=float, default=0, help='keep rows greater than specified number')
	options.add_argument('-l', '--less', type=float, default=float('inf'), help='keep rows less than specified number')
	options.add_argument('-d', '--delimiter', type=str, default='\t', help='value delimiter')
	args = options.parse_args()

	for line in fileinput.input(('-', )):
		elements = line.strip().split(args.delimiter)
		if (args.greater and float(elements[args.field-1]) > args.greater) or (args.less and float(elements[args.field-1]) < args.less):
			print(line.strip())
