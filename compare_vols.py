#!/usr/bin/env python

documentation = '''
Displays two volumes in a slice viewer for comparison 
(using emirt.show)
'''

import numpy as np
from emirt import io, show
from sys import argv

def load_data(output_fname):

	vol = io.znn_img_read(output_fname)

	if len(vol.shape) > 3:
		if vol.shape[0] > 2: #multiclass output
			vol = np.argmax(vol, axis=0)
		else: #binary output
			vol = vol[1,:,:,:]

	return vol

def main(fname_list):
	'''Loads data, starts comparison'''

	vols = [load_data(fname) for fname in fname_list]

	com = show.CompareVol(vols)
	com.vol_compare_slice()

if __name__ == '__main__':

	main(argv[1:])
