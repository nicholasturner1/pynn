#!/usr/bin/env python

import argparse
import numpy as np 
from emirt import io 

def mirror_data(dataset, buffer_sizes):

	full_size = np.array(dataset.shape) + 2 * buffer_sizes

	result = np.zeros(tuple(full_size))

	# Placing original data into center of result
	zmin = buffer_sizes[0]; zmax = result.shape[0] - buffer_sizes[0]
	ymin = buffer_sizes[1]; ymax = result.shape[1] - buffer_sizes[1]
	xmin = buffer_sizes[2]; xmax = result.shape[2] - buffer_sizes[2]

	result[zmin:zmax,ymin:ymax, xmin:xmax] = dataset

	#Creating a view for the next dimension to mirror
	#MIRRORING X
	if buffer_sizes[0] > 0:
		reversed_x = result[zmin:zmax,ymin:ymax, (xmax-1):(xmin-1):-1]

		result[zmin:zmax, ymin:ymax,
			:xmin] = reversed_x[:,:, -(xmin):]
		result[zmin:zmax, ymin:ymax,
			xmax:] = reversed_x[:,:,  :xmin  ]

	#MIRRORING Y
	if buffer_sizes[1] > 0:
		reversed_y = result[zmin:zmax, (ymax-1):(ymin)-1:-1, :]

		result[zmin:zmax, 0:ymin, :] = reversed_y[:, -(ymin):, :]
		result[zmin:zmax, ymax:,  :] = reversed_y[:, :(ymin) , :]

	#MIRRORING Z
	if buffer_sizes[0] > 0:
		reversed_z = result[(zmax-1):(zmin-1):-1,:,:]

		result[:zmin, :,:] = reversed_z[-(zmin), :,:]
		result[zmax:, :,:] = reversed_z[:(zmin), :,:]

	return result

def main(filename, fov_x, fov_y, fov_z, outname):

	print "Reading data..."
	original_data = io.znn_img_read(filename)
	assert len(original_data.shape) == 3

	buffer_sizes = np.array((fov_z, fov_y, fov_x)) / 2

	print "Buffering..."
	result = mirror_data(original_data, buffer_sizes)

	print "Saving..."
	io.znn_img_save(result, outname)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument('filename')
	parser.add_argument('fov_x', type=int)
	parser.add_argument('fov_y', type=int)
	parser.add_argument('fov_z', type=int)
	parser.add_argument('outname')

	args = parser.parse_args()

	main(args.filename,
		 args.fov_x,
		 args.fov_y,
		 args.fov_z,
		 args.outname)