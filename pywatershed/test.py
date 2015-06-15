#!/usr/bin/env python

"""
Show how to connect to keypress events
"""
import matplotlib.pylab as plt
import numpy as np

import emirt
reload(emirt)
    
import h5py
f = h5py.File('data.h5', 'r')
seg = np.asarray(f['/seg'])
affin = np.asarray(f['/affin'])
chann = np.asarray(f['/chann'])
# read original dend and dendValues
all_dendValues = np.asarray(f['/dendValues'])
all_dend = np.asarray(f['/dend'])
f.close()


seg2 = np.copy(seg)
s = np.array(seg.shape)

cv = emirt.show.compare_vol(chann, seg)
cv.vol_compare_slice()

#%%
import numpy as np
import h5py
f = h5py.File('../omnify/chunk_1_Z1-81_Y1-81_X1-81.segm.h5', 'r')
seg = np.asarray( f['/main'] )
plt.imshow(seg[5,:,:])
40 in np.unique(seg)
print "max: {}, number: {}".format(seg.max(), np.unique(seg).shape[0])

#%% test the affinity data
import numpy as np
m_aff = np.fromfile('matlab/temp/wstemp.affinity.data', dtype='single')
p_aff = np.fromfile('temp/input.affinity.data', dtype='single')

np.all(m_aff==p_aff)

#%% test the chunksizes
m_cks = np.fromfile('matlab/temp/wstemp.chunksizes', dtype='uint32')
p_cks = np.fromfile('temp/input.chunksizes', dtype='uint32')
np.all( m_cks==p_cks )

#%% test the metadata
m_mtd = np.fromfile('matlab/temp/wstemp.metadata', dtype='uint32')
p_mtd = np.fromfile('temp/input.metadata', dtype='uint32')
np.all( m_mtd==p_mtd )

#%% test the sizes
m_szs = np.fromfile('matlab/temp/wstemp.sizes', dtype='uint32')
p_szs = np.fromfile('temp/input.sizes', dtype='uint32')
np.all( m_szs==p_szs )

#%% test seg data
import numpy as np
m_seg = np.fromfile('matlab/temp/wstemp.chunks/0/0/0/.seg', dtype='uint32')
p_seg = np.fromfile('temp/input.chunks/0/0/0/.seg', dtype='uint32')

np.all(m_seg==p_seg)

#%% test dend
import numpy as np
dend_m = np.fromfile('matlab/temp/wstemp.dend_pairs', dtype='uint32')
dend_p = np.fromfile('temp/input.dend_pairs', dtype='uint32')

np.all(dend_m==dend_p)

#%% test dend values
import numpy as np
dendValues_m = np.fromfile('matlab/temp/wstemp.dend_values', dtype='uint32')
dendValues_p = np.fromfile('temp/input.dend_values', dtype='uint32')

np.all(dendValues_m==dendValues_p)

#%% compare the segment
from global_vars import *
import watershed_chop
watershed_chop.watershed1()
import watershed_merge
watershed_merge.watershed2()

import h5py
fm = h5py.File('../znn_merged_matlab.Th-900.Tl-300.Ts-400.Te-250.segm.h5', 'r')
seg_m = np.asarray( fm['/main'] )
dend_m = np.asarray( fm['/dend'] )
dendValues_m = np.asarray( fm['/dendValues'] )
fm.close()

fm = h5py.File('../znn_merged_matlab.Th-900.Tl-300.Ts-400.Te-250.segm.h5', 'r')
seg_m2 = np.asarray( fm['/main'] )
dend_m2 = np.asarray( fm['/dend'] )
dendValues_m2 = np.asarray( fm['/dendValues'] )
fm.close()

fp = h5py.File( ws_merge_h5 )
fp = h5py.File( '../relabel.h5' )
seg_p = np.asarray( fp['/main'] )
dend_p = np.asarray( fp['/dend'] )
dendValues_p = np.asarray(fp['/dendValues'])
fp.close()

print "seg:         matlab is same with python: {}".format( np.all( seg_m == seg_p ) )
print "seg:         matlab is same with matlab: {}".format( np.all( seg_m == seg_m2 ) )

print "dend:        matlab is same with python: {}".format( np.all( dend_m == dend_p ) )
print "dend:        matlab is same with matlab: {}".format( np.all( dend_m == dend_m2 ) )

print "dendValues:  matlab is same with python: {}".format( np.all( dendValues_m == dendValues_p ) )
print "dendValues:  matlab is same with matlab: {}".format( np.all( dendValues_m == dendValues_m2 ) )


#%% compare channel and affinity
import emirt.show
from global_vars import *

VS = emirt.show.VolSlider( gchann_file )
VS.show()

#
import emirt.show
from global_vars import *
import matplotlib.pylab as plt
plt.figure
VS = emirt.show.VolSlider( gaffin_file )
VS.show()

#%% compare channel and affinity data
import h5py
import matplotlib.pylab as plt
from global_vars import *
zc = 1
zs = 1

#fc = h5py.File( gchann_file, 'r' )
#fs = h5py.File( 'temp/pywsmerge.Th-900.Tl-300.Ts-400.Te-250.h5', 'r' )

fc = h5py.File( '../omnify/chunk_1_X0-255_Y0-255_Z0-255.chann.h5', 'r' )
fs = h5py.File( '../omnify/chunk_1_X0-255_Y0-255_Z0-255.segm.h5', 'r' )

img_c = np.array( fc['/main'][zc,:,:] )
img_s = np.array( fs['/main'][zs,:,:] )

plt.subplot(121)
plt.imshow( img_c, cmap='gray' )
plt.subplot(122)
plt.imshow( img_s, cmap='gray')

fc.close()
fs.close()

#%% 
import h5py
import matplotlib.pylab as plt
from global_vars import *

fc = h5py.File( gchann_file, 'r' )
fa = h5py.File( gaffin_file, 'r' )

width = 200
vlm_c = np.array( fc['/main'][:,:width,:width] )
vlm_a = np.array( fa['/main'][0,:,:width,:width] )

fc.close()
fa.close()

CV = emirt.show.CompareVol(vlm_c, vlm_a)
CV.vol_compare_slice()



