#!/usr/bin/env python
__doc__ = '''
Multiclass Classification Error Between ZNN Volumes

 This module computes the multiclass classification error between
two ZNN volumes. The error values counts 1 for each different 
classification within the entire volume, and saves a binary volume which 
indicates the spatial location of the differences.

If the volumes are of different sizes, then the comparison volume
is cropped to match the dimensions of the network output. Thus, if
comparing two different network output files, the comparison file
should be the larger volume. Cropping takes evenly from both sides,
in line with the loss of resolution common with convolutional nets.


Inputs:

	-Network Output Filename
	-Comparison Filename
	-Desired Output Name (opt)
	-Whether the comparison file is a label file (opt) (flag)
	-Whether to normalize the comparison volume (opt) (flag)
	  (this can be useful for direct comparison to images)

Main Outputs:

	-New ZNN dataset containing the classification
	 differences between the network output and the
	 comparison volume.


Nicholas Turner, June 2015
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

	#Taking the maximum prediction of the input volume
	net_out = np.argmax(net_out, axis=0)

	#Binarizing if a label file
	if not comp_is_label:
		#Same treatment as above
		comp = np.argmax(comp, axis=0)

	#Normalizes values between 0 and 1
	if normalize:
		comp = norm(comp)

	print "Cropping labels..."
	comp_cropped = crop( comp, net_out.shape )

	print "Deriving Error..."
	err = (( net_out - comp_cropped ) != 0).astype(np.float64)

	print "Multiclass Error: %f" % (err.sum())

	io.znn_img_save(err, outname)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)

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
