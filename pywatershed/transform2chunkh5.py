# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 16:53:46 2015

transform the channel data to chunked hdf5 

@author: jingpeng
"""
import h5py
import numpy as np
import time

#%% parameters
src_fname = '../../../Ignacio/aws-znn/pipeline/watershed/znn_merged.hdf5'
dst_fname = '/usr/people/jingpeng/znn_merged.hdf5'

#%% transforming
start_all = time.time() 
# read
f1 = h5py.File( src_fname, 'r')
f2 = h5py.File( dst_fname, 'w')

v1 = f1['/main']
sz = np.array(v1.shape, dtype='uint32')

f2.create_dataset('/main', shape=v1.shape, dtype='float32', chunks=(3,512,512,512), compression='gzip')
v2 = f2['/main']

for z in xrange( sz[1] ):
    print "z: {}".format(z)
    start = time.time()
#    if z < sz[1]:
    v2[:,z,:,:] = np.array(v1[:, z, :,:])
#    else:
#        v2[:,z,:,:] = np.zeros( sz[1:], dtype='float32' )
    print "layer {} takes {}s".format( z, time.time()-start )
#%%
f1.close()
f2.close()

#%% count time
print "elapsed time: {}h".format( (time.time() - start_all)/3600 )