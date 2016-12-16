#!/usr/bin/python

import argparse
import sys


if __name__ == '__main__':

	options = argparse.ArgumentParser(description='Qrels manipulations')
	required = options.add_argument_group('required arguments')
	required.add_argument('-q', '--qrels', help='Qrels file')
	options.add_argument('-r', '--rels', type=int, default=0, help='Read documents at this level or above only')
	options.add_argument('-t', '--topic', help='Give qrels for specified topic')
	options.add_argument('-c', '--count', action='store_true', help='Report number of qrels')
	args = options.parse_args()

	qrels = {}
	with open(args.qrels) as f:
		for line in f:
			topic, _, doc, rel = line.split()
			rel = int(rel)
			if rel >= args.rels:
				if topic not in qrels:
					qrels[topic] = {}
				if rel not in qrels[topic]:
					qrels[topic][rel] = []
				qrels[topic][rel].append(doc)

	if args.topic:
		count = 0
		try:
			for rel in qrels[args.topic]:
				for doc in qrels[args.topic][rel]:
					print('{} {}'.format(doc, str(rel)))
					count += 1
		except IndexError:
			print('{} is not a topic in the qrels file.'.format(args.topic))

		if args.count:
			print('Total: {}'.format(str(count)))
