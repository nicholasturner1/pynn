# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:37:12 2015

@author: jingpeng
"""
from global_vars import *
import h5py
import time

def write_h5_with_dend(h5filename, dend, dendValues, vol=False):
    import h5py
    f = h5py.File( h5filename, "a" )
    if np.any(vol):
        f.create_dataset('/main', data = vol )
    f.create_dataset('/dend', data=dend, dtype='uint32')
    f.create_dataset('/dendValues', data=dendValues, dtype='single')
    f.close()
	
def write_h5_chann( h5filename, vol ):
    import h5py
    f = h5py.File( h5filename, "w" )
    f.create_dataset('/main', data = vol )
    f.close()
    
def write_cmd( fname, bfrom ):   
    cmdfname = gomnify_data_file + fname + ".cmd"
    fcmd = open(cmdfname, 'w')
    fcmd.write('create:'+ gomniprojects_save_file + fname+'.omni\n')
    fcmd.write('loadHDF5chann:' + fname + '.chann.h5\n')
    fcmd.write('setChanResolution:1,{},{},{}\n'.format( gvoxel_size[2], gvoxel_size[1], gvoxel_size[0] ))
    fcmd.write('setChanAbsOffset:,1,{},{},{}\n'.format(\
        bfrom[2]*gvoxel_size[2],\
        bfrom[1]*gvoxel_size[1],\
        bfrom[0]*gvoxel_size[0]) )
    fcmd.write('loadHDF5seg:'+ fname +'.segm.h5\n')
    fcmd.write('setSegResolution:1,{},{},{}\n'.format( gvoxel_size[2], gvoxel_size[1], gvoxel_size[0] ))
    fcmd.write('setSegAbsOffset:1,{},{},{}\n'.format(\
        bfrom[2]*gvoxel_size[2],\
        bfrom[1]*gvoxel_size[1],\
        bfrom[0]*gvoxel_size[0]) )
    fcmd.write('mesh\n')
    fcmd.write('quit\n\n')
    fcmd.close()

def write_sh(shfname, fname):
    fsh = open( shfname, 'w' )
    fsh.write('#!/bin/bash\n')
    fsh.write(gomnifybin + " --headless --cmdfile='" + gomnify_data_file + fname + ".cmd'")
    fsh.close()
def write_runall_sh(blockNum):
    fsh = open( gomnify_data_file + 'runall.sh', 'w')
    fsh.write('#!/bin/bash\n')
    for idx in range(blockNum):
        fsh.write( 'sh chunk_' +str(idx+1) + '.sh\n' )
    fsh.close()

def prepare_complete_volume():
    fname = "chunk_" + str(1) + \
            "_Z" + str(0) + '-' + str(s[0]-1) + \
            "_Y" + str(0) + '-' + str(s[1]-1) + \
            "_X" + str(0) + '-' + str(s[2]-1)
    # write the segmentation h5 file
    h5fname = gomnify_data_file + fname + ".segm.h5"
    os.system("mv " + gws_merge_h5 + " " + h5fname)
    write_h5_with_dend( h5fname, dend, dendValues )
    # channel data
    # write omnify cmd file
    write_cmd( fname, np.array([0,0,0]) )
    # generate a corresponding sh file
    shfname =  gomnify_data_file + "chunk_" + str(1) + ".sh"
    write_sh(shfname, fname)
    # write a general bash file
    write_runall_sh(1)

def prepare_blocks():
    ftmp = h5py.File( gws_merge_h5, "r" )
    seg = ftmp['/main']
    print "get the blocks ..."
    # get the blocks of seg
    fchann = h5py.File( gchann_file, 'r')
    chann = fchann['/main']        
    
    faffin = h5py.File( gaffin_file, 'r' )
    affin = faffin['/main']
    s = np.array(affin.shape, dtype='uint32')[1:]
    
    blockid = 0
    for bz in xrange(0, s[0], gblocksize[0]-goverlap[0]):
        for by in xrange(0, s[1], gblocksize[1]-goverlap[1]):
            for bx in xrange(0, s[2], gblocksize[2]-goverlap[2]):
                blockid += 1            
                if bx>=512*3 or by>=512*3 or bz>=128*2: 
                    continue
                print "\nblockid: {}".format(blockid)
                
                bfrom = np.array([bz, by, bx])
                # the +1 was for rebuild MST
                bto = np.minimum(s, bfrom+gblocksize)
                
                print "bfrom: {}".format(bfrom)
                print "bto  : {}".format(bto)
                start = time.time()
                block = np.asarray( seg[bfrom[0]:bto[0], bfrom[1]:bto[1], bfrom[2]:bto[2] ] )
                print "reading segment block takes {0:.1f}s".format( time.time() - start )
                start = time.time()
                block_affin = np.asarray( affin[:, bfrom[0]:bto[0], bfrom[1]:bto[1], bfrom[2]:bto[2]] )
                print "reading affinity block takes {0:.1f}s".format( time.time() - start )
                
                # rebuild MST
                start = time.time()
                from relabel import relabel
                block, chunk_dend, chunk_dendValues = relabel(block, block_affin)
                print "relabeling takes {0:.1f}s".format( time.time() - start )
                print "relabelled block:    max: {}, number: {}".format(block.max(), np.unique(block).shape[0])
                # write the h5 file
                fname = "chunk_" + str(blockid) + \
                        "_X" + str(bfrom[2]) + '-' + str(bto[2]-1) + \
                        "_Y" + str(bfrom[1]) + '-' + str(bto[1]-1) + \
                        "_Z" + str(bfrom[0]) + '-' + str(bto[0]-1)
                # write the segmentation h5 file
                start = time.time()
                h5fname = gomnify_data_file + fname + ".segm.h5"
                write_h5_with_dend( h5fname, chunk_dend, chunk_dendValues, block )
                print "writting segment block takes {0:.1f}s".format( (time.time() - start) )                
                
                # write channel data    
                start = time.time()
                block_chann = np.asarray( chann[bfrom[0]:bto[0], bfrom[1]:bto[1], bfrom[2]:bto[2] ] )
                print "reading channel block takes {0:.1f}s".format( time.time() - start )
                start = time.time()
                write_h5_chann( gomnify_data_file + fname + '.chann.h5', block_chann )
                print "writting channel block takes {0:.1f}s".format( (time.time() - start) )
                
                # write omnify cmd file
                write_cmd( fname, bfrom )
                # generate a corresponding sh file
                shfname =  gomnify_data_file + "chunk_" + str(blockid) + ".sh"
                write_sh(shfname, fname)
    
    # write a general bash file
    write_runall_sh(blockid)
    ftmp.close()
    fchann.close()
    faffin.close()

def omnify_chop():
    ftmp = h5py.File( gws_merge_h5, "r" )
    seg = ftmp['/main']
    s = np.array(seg.shape, dtype='uint32')
    ftmp.close()
#    import os
#    os.system('rm -rf {}chunk_*'.format(gomnify_data_file) )
    if np.all( gblocksize >= s ):  
        # the complete volume
        prepare_complete_volume()
    else:
        # run block chunking
        prepare_blocks()

if __name__ == "__main__":
    start = time.time()
    omnify_chop()
    print "omnify_chop takes {0:.2f}h".format( (time.time() - start)/3600 )
