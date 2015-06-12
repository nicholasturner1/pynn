#!/usr/bin/env python

documentation = '''
Squared Error Calculation
'''

import argparse
import numpy as np 
from emirt import io 
from vol_utils import crop, norm

def main(net_out_fname, comp_fname, outname='mult_err',
	comp_is_label=True, normalize=False):

	print "Loading data..."
	net_out = io.znn_img_read( net_out_fname )
	comp = io.znn_img_read( comp_fname )

	net_out = np.argmax(net_out, axis=0)

	#Binarizing if a label file
	if not comp_is_label:
		comp = np.argmax(comp, axis=0)

	if normalize:
		comp = norm(comp)

	print "Cropping labels..."
	comp_cropped = crop( comp, net_out.shape )

	print "Deriving Error..."
	err = (( net_out - comp_cropped ) != 0).astype(np.float64)

	print "Multiclass Error: %f" % (err.sum())

	io.znn_img_save(err, outname)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description=documentation)

	parser.add_argument('net_output_filename',
		help= "Network output file for which you'd like the error")
	parser.add_argument('comparison_filename',
		help= "Comparison (larger) file for the network output (likely a label file)")
	parser.add_argument('output_filename',
		default='mult_err',nargs='?',
		help= 'Result filename')
	#The actual variable stores whether the comp file IS a label
	parser.add_argument('-not_label', action="store_false",
		help='Flag indicating whether or not the comparison volume is a label file',
		default=True)
	parser.add_argument('-normalize', action="store_true",
		help="Whether to normalize the comparison volume",
		default=False)

	args = parser.parse_args()

	main(args.net_output_filename,
		 args.comparison_filename,
		 args.output_filename,
		 args.not_label,
		 args.normalize)
