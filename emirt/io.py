# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 14:27:31 2015

@author: jingpeng
"""

import numpy as np

#%% read hdf5 volume
def imread( fname ):
    if '.hdf5' in fname or '.h5' in fname:
        import h5py
        f = h5py.File( fname )
        v = np.asarray( f['/main'] )
        f.close()
        print 'finished reading image stack :)'
        return v
    elif '.tif' in fname:
#        import skimage.io
#        vol = skimage.io.imread( fname, plugin='tifffile' )
        import tifffile
        vol = tifffile.imread(fname)
        #import scipy as sp
        #vol = sp.misc.imread(fname)
        return vol 
    else:
        print 'file name error, only suport tif and hdf5 now!!!'

def imsave( vol, fname ):    
    if '.hdf5' in fname or '.h5' in fname:
        import h5py
        f = h5py.File( fname )
        f.create_dataset('/main', data=vol)
        f.close()
        print 'hdf5 file was written :)'
    elif '.tif' in fname:
#        import skimage.io
#        skimage.io.imsave(fname, vol, plugin='tifffile')
        import tifffile
        tifffile.imsave(fname, vol)
    else:
        print 'file name error! only support tif and hdf5 now!!!'
        
def save_variable( var, vname ):
    import pickle
    f = open(vname, 'w')
    pickle.dump(var, f)
    f.close()
    
def load_variable( vname ):
    import pickle
    f = open( vname, 'rb' )
    var = pickle.load(f)
    f.close()
    return var

# load binary znn image
def znn_img_read( fname ):
    if '.image' in fname:
        fname = fname.replace('.image', "")
        ext = ".image"
    elif '.label' in fname:
        fname = fname.replace(".label", "")
        ext = ".label"
    else:
        ext = ""
    vol = np.fromfile(fname + ext, dtype='double')
    sz = np.fromfile(fname+'.size', dtype='uint32')[::-1]
    vol = vol.reshape(sz)# order='F')
    return vol

def znn_img_save(vol, fname):
#    vol = vol.astype('double')
    if ".image" in fname:
        fname = fname.replace(".image", "")
        ext = ".image"
    elif ".label" in fname:
        fname = fname.replace(".label", "")
        ext = ".label"
    else:
        ext = ""
    vol.tofile(fname+ext)
    sz = np.asarray( vol.shape, dtype='uint32' )[::-1]
    sz.tofile(fname+".size")

def write_for_znn(Dir, vol, cid):
    '''transform volume to znn format'''
    # make directory
    import emirt.os    
    emirt.os.mkdir_p(Dir )
    emirt.os.mkdir_p(Dir + 'data')
    emirt.os.mkdir_p(Dir + 'spec')
    vol.tofile(Dir + 'data/' + 'batch'+str(cid)+'.image')
    sz = np.asarray(vol.shape)
    sz.tofile(Dir + 'data/' + 'batch'+str(cid)+'.size')
    
    # printf the batch.spec
    f = open(Dir + 'spec/' + 'batch'+str(cid)+'.spec', 'w')
    f.write('[INPUT1]\n')
    f.write('path=./dataset/piriform/data/batch'+str(cid)+'\n')
    f.write('ext=image\n')
    f.write('size='+str(sz[2])+','+str(sz[1])+','+str(sz[0])+'\n')
    f.write('pptype=standard2D\n\n')
    
