#!/usr/bin/env python
__doc__ = '''
ZNN data import from tif files

 This module imports a pair of tif files into dataset directories
 within the ZNN hierarchy. 

 The created  directories are specified by means of relative pathnames, 
 so the current directory determines their final location. While one could
 run this from any such current directory, it is intended to run from the
 ZNN installation directory for standard organization.

Inputs:

	-Image Filename
	-Label Filename
	-Desired Dataset Name (opt)
	-Whether to remove the mean from the image at this step (opt) (flag)
	 NOTE: You can also perform standard normalization 
	       through ZNN preprocessing
	-What percentage of the dataset to use as a test set (opt) (flag)
	  
	
Main Outputs:

	-A ZNN dataset directory populated with:
		-batch1.image, batch2.image - image 
		-batch1.label ()


Nicholas Turner, June 2015
'''
documentation ='''
Quick ZNN data import from tif files

SHOULD BE RUN FROM THE ZNN DIRECTORY
'''

#Standard imports
import os, math, argparse
#Not so standard imports
import tifffile
import emirt
import numpy as np

########################################
#Constants

spec_file_format_string = """[INPUT1]
path=./dataset/{0}/data/batch{1}
ext=image
size={2},{3},{4}
pptype=standard2D

[LABEL1]
path=./dataset/{0}/data/batch{1}
ext=label
size={2},{3},{4}
pptype=binary_class

[MASK1]
size={2},{3},{4}
pptype=one
ppargs=2"""
########################################

def rgb2bin(vol):
	'''Transforms a 4d numpy array to a binary 3d array'''

	res = vol.sum(3)
	res[res > 0] = 1

	return res.astype('uint8')

def zero_mean(vol):
	'''Subtracts the mean from each point in the volume'''
	return vol - np.mean(vol)

def split_data(volume, label, percent_test):

	shape = volume.shape
	num_slices = shape[0]

	if percent_test == 0:

		test_shape = list(shape)
		test_shape[0] = 0

		test_vol = np.zeros(test_shape)
		test_label = np.zeros(test_shape)

		return volume, label, test_vol, test_label

	else:

		num_test = math.ceil((percent_test / 100.) * num_slices)

		train_vol = volume[:-(num_test),:,:]
		test_vol = volume[-(num_test):,:,:]

		train_label = label[:-(num_test),:,:]
		test_label = label[-(num_test):,:,:]

		return train_vol, train_label, test_vol, test_label

def write_spec_file(dname, batch_num, size):

	spec_fname = "dataset/{0}/spec/batch{1}.spec".format(dname,
														batch_num)
	f = open( spec_fname, 'w')

	f.write(spec_file_format_string.format(
				dname, 
				batch_num, 
				size[2], 
				size[1], 
				size[0]) )
	
	f.close()

def main(vol_fname='', label_fname='', dataset_name='', percent_test=0,
	normalize_mean=False):

	print "Reading data..."
	vol = tifffile.imread(vol_fname)
	label = tifffile.imread(label_fname)

	if zero_mean:
		vol = zero_mean(vol)

	if len(label.shape) > 3 and label.shape[3] == 3:
		print "Converting label to binary..."
		label = rgb2bin(label)

	#Splitting into training and test sets
	train, label_train, test, label_test = split_data(vol, label, percent_test)

	#Transpose
	train = train.transpose(0,2,1)
	test = test.transpose(0,2,1)

	label_train = label_train.transpose(0,2,1)
	label_test = label_test.transpose(0,2,1)

	s_train = train.shape
	s_test = test.shape

	print "Saving data in znn format..."
	#Making the necessary directories
	os.makedirs('dataset/{}/data/'.format(dataset_name))
	os.makedirs('dataset/{}/spec/'.format(dataset_name))
		
	#Save as znn format
	train_outname = "dataset/{0}/data/batch{1}.image".format(dataset_name, 1)
	label_train_outname = "dataset/{0}/data/batch{1}.label".format(dataset_name, 1)

	if percent_test > 0:

		test_outname = "dataset/{0}/data/batch{1}.image".format(dataset_name, 2)
		label_test_outname = "dataset/{0}/data/batch{1}.label".format(dataset_name, 2)

	emirt.io.znn_img_save(train.astype('double'), train_outname)
	emirt.io.znn_img_save(label_train.astype('double'), label_train_outname)

	if percent_test > 0:

		emirt.io.znn_img_save(test.astype('double'), test_outname)
		emirt.io.znn_img_save(label_test.astype('double'), label_test_outname)

	#Prepare a spec file
	print "Writing spec file..."
	write_spec_file(dataset_name, 1, s_train)

	if percent_test > 0:

		write_spec_file(dataset_name, 2, s_test)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument('vol_fname', help='input volume filename')
	parser.add_argument('label_fname', help='label volume filename')
	parser.add_argument('dataset_name', 
		help='what to call the dataset within the znn hierarchy')
	parser.add_argument('-zm','-zero_mean', action='store_true')
	parser.add_argument('-p','-percent_test','--percent_test', type=int, default=0)
	
	args = parser.parse_args()

	main(vol_fname=args.vol_fname,
		 label_fname=args.label_fname,
		 dataset_name=args.dataset_name,
		 percent_test=args.percent_test,
		 normalize_mean=args.zm)