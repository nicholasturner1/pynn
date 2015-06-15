# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:24:42 2015

@author: jingpeng
"""
import numpy as np


#%% basic

#gchann_file = '../../../Ignacio/w0-4/omnify/channel.hdf5'
gchann_file = '/data/jingpeng/channel3.hdf5'
#gchann_file = '../../05_get_train_data/11_vol_data/7nm-2500Pix.chann.h5'
#affin_file = '../znn_merged.hdf5'
gaffin_file = '/data/jingpeng/znn_merged.hdf5'
gtemp_file = '/data/jingpeng/temp/'

# the path of omnify binary
gomnifybin = 'bash /data/jingpeng/omnify/omnify.sh'

#%% watershed chop
# step 
gwidth = np.array([650, 647, 647], dtype='uint32')
# watershed parameters
gws_high = 0.91
gws_low = 0.3
gws_dust = 400
gws_dust_low = 0.25
gws_threads_num = 1
gws_bin_file = 'src/quta/zi/watershed/main/bin/xxlws'

#%% watershed merge
gws_merge_h5 = gtemp_file + "pywsmerge.Th-{}.Tl-{}.Ts-{}.Te-{}.h5".format(int(gws_high*1000), int(gws_low*1000), int(gws_dust), int(gws_dust_low*1000))

#%% omnify chop
# the block size and overlap size, z,y,x
gblocksize = np.array([128, 512, 512], dtype='uint32')
goverlap = np.array([20,32,32], dtype='uint32')
# voxel size
gvoxel_size = np.array([40,7,7])

# prepare the omnify data for omnifying
gomnify_data_file = '/data/jingpeng/omnify/'

# the save path of omni projects, should be local. Remote path may make the segmentation empty.
gomniprojects_save_file = '/data/jingpeng/omni_projects/'
