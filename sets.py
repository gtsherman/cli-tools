#!/usr/bin/python3

import argparse
import logging


def main():
    options = argparse.ArgumentParser(description='Tools for working with sets.')
    options.add_argument('-d', '--delimiter', default=',', help='The delimiter to use for splitting fields.')
    options.add_argument('-f', '--fields', default=None, type=int, action='append', help='The field positions to use '
                                                                                         'for comparison. Uses all '
                                                                                         'fields by default.')
    options.add_argument('-c', '--comparison', choices=['p', 'positional', 'j', 'joint'], default='j',
                         help='The comparison method used. "(p)ositional" compares each field with the corresponding '
                              'position in the other file. "(j)oint" treats the files as a composite unit to be '
                              'compared')
    options.add_argument('-s', '--size', action='store_true', help='Report the size of each set.')
    options.add_argument('-i', '--intersection', action='store_true', help='List the intersection of the sets.')
    options.add_argument('-is', '--intersection-size', action='store_true', help='Report the size of the intersection '
                                                                                 'the sets.')
    options.add_argument('-u', '--union', action='store_true', help='List the union of the sets.')
    options.add_argument('-us', '--union-size', action='store_true', help='Report the size of the union of the sets.')
    options.add_argument('-m', '--difference', action='store_true', help='List the items of the first set that are '
                                                                         'not part of the later sets')
    options.add_argument('-ms', '--difference-size', action='store_true', help='Report the size of the difference of '
                                                                               'the later sets from the first set.')
    options.add_argument('files', nargs=2, help='The files containing the sets')
    args = options.parse_args()

    sets = []
    for file in args.files:
        file_items = FlexibleSet(num_fields=len(args.fields))
        with open(file) as f:
            for line in f:
                line_values = line.strip().split(args.delimiter)
                line_items = []
                for field in args.fields:
                    line_items.append(line_values[field-1])
                file_items.add(*line_items)
        sets.append(file_items)

    if args.comparison.startswith('j'):
        joint_sets = [s.get_joint_set() for s in sets]  # ( set((field11, field12), (field21, field22)), set(...) )
        compare(args, *joint_sets)
    else:
        positional_sets = [s.get_individual_sets() for s in sets]  # ((set(field11), set(field12)), (set(field21), ...))
        for i in range(len(args.fields)):
            print('Field ', args.fields[i], ':', sep='')
            sets = [s[i] for s in positional_sets]
            compare(args, *sets)
            if i < len(args.fields) - 1:
                print()


def compare(args, *sets):
    # Lists
    if args.intersection:
        print('Intersection:')
        for item in set.intersection(*sets):
            print('\t', args.delimiter.join(item), sep='')
    if args.union:
        print('Union:')
        for item in set.union(*sets):
            print('\t', args.delimiter.join(item), sep='')
    if args.difference:
        print('Difference:')
        for item in sets[0].difference(*sets[1:]):
            print('\t', args.delimiter.join(item), sep='')

    # Sizes
    if args.size:
        print('Sizes:')
        for i in range(len(sets)):
            print('\t', len(sets[i]), sep='')
    if args.intersection_size:
        print('Intersection size:')
        print('\t', len(set.intersection(*sets)), sep='')
    if args.union_size:
        print('Union size:')
        print('\t', len(set.union(*sets)), sep='')
    if args.difference_size:
        print('Difference size:')
        print('\t', len(sets[0].difference(*sets[1:])))


class FlexibleSet(object):
    def __init__(self, num_fields=1):
        self._item_lists = [[] for _ in range(num_fields)]

    def add(self, *items):
        if len(items) > len(self._item_lists):
            logging.warning('Trying to add more items than FlexibleSet has fields. Items will be truncated.')

        if len(items) < len(self._item_lists):
            logging.warning('Trying to add fewer items than FlexibleSet has fields. Items will be ignored.')

        for i, item in enumerate(items):
            if i < len(self._item_lists):
                self._item_lists[i].append(item)

    def get_individual_sets(self):
        return [set(items_list) for items_list in self._item_lists]

    def get_joint_set(self):
        return set(zip(*self._item_lists))


if __name__ == '__main__':
    main()
