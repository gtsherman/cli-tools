import numpy


def read_data(ins, delimiter='\t', column=1):
	lines = []
	elements = []
	for line in ins:
		p = line.split(delimiter)[column-1]
		try:
			e = float(p)
			if not numpy.isnan(e):
				lines.append(line.strip())
				elements.append(e)
		except ValueError:
			print('Not a valid number: {} ({}) -- maybe specify field and delimiter?'.format(p, line.strip()))
	return (lines, elements)
