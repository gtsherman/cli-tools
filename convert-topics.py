#!/usr/bin/python

from collections import Counter
import xml.etree.ElementTree as ET
import argparse, json, sys


def output(query_data, output_format):
	if output_format == 'json':
		print(json.dumps(query_data, sort_keys=True, indent=4, separators=(',', ': ')))
	elif output_format == 'indri':
		print('<parameters>')
		for query in query_data['queries']:
			print_indri_query(query)
		print('</parameters>')
	else:
		for query in query_data['queries']:
			print('\t'.join([query['title'], query['text']]))

def parse_indri(in_file):
	with open(in_file) as f:
		queries = ET.parse(f).getroot()
		try:
			query_data = {'queries': []}
			for query in queries.findall('query'):
				num = query.find('number').text.strip()
				text = query.find('text').text.strip()
				counts = Counter(text.split())

				q = construct_query_dict(num, text, counts)
				query_data['queries'].append(q)
				
			return query_data
		except:
			sys.stderr.write('Error reading file. Are you sure this is an XML file?\n')
	
def parse_json(in_file):
	try:
		with open(in_file) as f:
			return json.load(f)
	except:
		sys.stderr.write('Error reading file. Are you sure this is a JSON file?\n')

def parse_tsv(in_file):
	query_data = {'queries': []}
	try:
		with open(in_file) as f:
			for line in f:
				num, text = line.strip().split('\t')
				counts = Counter(text.split())

				q = construct_query_dict(num, text, counts)
				query_data['queries'].append(q)

			return query_data
	except:
		sys.stderr.write('Error reading file. Are you sure this is a TSV file?\n')

def construct_query_dict(num, text, counts):
	q = {}
	q['title'] = num
	q['text'] = text
	q['model'] = []
	for term in counts:
		t = {}
		t['weight'] = counts[term]
		t['feature'] = term
		q['model'].append(t)
	return q

def print_indri_query(query):
	print('<query>')
	print('<number>{}</number>'.format(query['title']))
	print('<text>')
	print(query['text'])
	print('</text>')
	print('</query>')

def main():
	options = argparse.ArgumentParser(description='Convert topics format.')
	required = options.add_argument_group('required arguments')
	required.add_argument('-f', '--file', help='the original topics file', required=True)
	required.add_argument('-i', '--input-format', choices=['indri', 'json', 'tsv'], help='specify the original file format', required=True)
	required.add_argument('-o', '--output-format', choices=['indri', 'json', 'tsv'], help='specify the output file format', required=True)
	args = options.parse_args()

	if args.input_format == 'indri':
		query_data = parse_indri(args.file)
	elif args.input_format == 'json':
		query_data = parse_json(args.file)
	else:
		query_data = parse_tsv(args.file)

	output(query_data, args.output_format)

if __name__ == '__main__':
	main()
