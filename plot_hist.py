#!/usr/bin/env python

documentation = '''
Plot a histogram of the values within a znn image file'''

import argparse
import numpy as np
import matplotlib.pyplot as plt
from emirt import io

def main(input_filename, num_bins):

	vol = io.znn_img_read(input_filename)

	values = vol.flatten()

	n, bins, patches = plt.hist(values, num_bins)

	plt.xlabel('Value')
	plt.ylabel('Counts')
	plt.show()

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description = documentation)

	parser.add_argument('input_filename',
		help='Name of the input file')
	parser.add_argument('-num_bins',
		type=int, default=100, 
		help='Number of bins for histogram')

	args = parser.parse_args()

	main(args.input_filename,
		 args.num_bins)