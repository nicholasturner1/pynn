# pynn
Python tools for ZNN (https://github.com/seung-lab/znn-release) data

# Dependencies
|Library|Ubuntu package name|
|:-----:|-------------------|
|tifffile|python-tifffile|
|numpy|python-numpy|
|matplotlib|python-matplotlib|
|scipy|python-scipy|

# Initial Setup

Some of the scripts within this package depend on cython optimizations. These need to be
compiled on your host machine before they can be imported properly. This can be achieved
by:

cd pynn
python setup.py build_ext --inplace
