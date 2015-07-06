#!/usr/bin/env python

from emirt import io
from sys import argv

d = io.znn_img_read(argv[1])

print d.shape[::-1]