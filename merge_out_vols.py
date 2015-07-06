#!/usr/bin/env python 

from sys import argv
import numpy as np 
from emirt import io

print "Loading Data..."
vols = [io.znn_img_read(filename) for filename in argv[1:]]

final_shape = np.concatenate(([len(vols)], vols[0].shape))

merged = np.empty((final_shape))

print "Arranging Data..."
for t in range(merged.shape[0]):
	merged[t,:,:,:] = vols[t]

outname = argv[1].split('.')[0]

print "Saving Data..."
io.znn_img_save(merged, outname)