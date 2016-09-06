#!/usr/bin/python

import argparse
import numpy
import subprocess
import sys

from scipy.stats import ttest_1samp, ttest_rel


def get_data(out, comp_metric):
	data = {}
	for line in out.splitlines():
		if comp_metric == 'map':
			metric, query, value = line.split()
			if metric == 'map' and query != 'all':
				data[query] = float(value)
		elif comp_metric == 'ndcg':
			_, query, value, _ = line.split(',')
			if query != 'topic' and query != 'amean':
				data[query] = float(value)
	return [value for (key, value) in sorted(data.items())]

def main():
	options = argparse.ArgumentParser(description='Run a t-test comparing two indri runs.')
	required = options.add_argument_group('required arguments')
	required.add_argument('-q', '--qrels', help='qrels file', required=True)
	required.add_argument('-f', '--file', action='append', help='out file', required=True)
	options.add_argument('-g', '--greater', action='store_true', help='greater than test')
	options.add_argument('-m', '--metric', choices=['map', 'ndcg'], default='map', help='the metric to compare')
	args = options.parse_args()

	if len(args.file) < 2:
		print('You must specify two out files.')

	if args.metric == 'map':
		command = 'trec_eval -q {q} {f}'
	elif args.metric == 'ndcg':
		command = 'gdeval {q} {f}'

	f1 = subprocess.check_output(command.format(q=args.qrels, f=args.file[0]).split())
	f2 = subprocess.check_output(command.format(q=args.qrels, f=args.file[1]).split())

	d1 = get_data(f1, args.metric)
	d2 = get_data(f2, args.metric)

	print('\n{}: {}'.format(args.file[0], numpy.mean(d1)))
	print('{}: {}\n'.format(args.file[1], numpy.mean(d2)))

	ttest_results = ttest_rel(d1, d2)
	if (args.greater):
		res = ttest_results[1]/2
	else:
		res = ttest_results[1]
	print('p-value: {}'.format(res))

if __name__ == '__main__':
	main()
