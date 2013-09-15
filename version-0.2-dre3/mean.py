# randomcats.py
# This program makes a random catalogue based on the FUSION catalogue

import sys
import math
import array
import random
import MySQLdb
import numpy
import matplotlib.pyplot as plt
import astropysics as astro

from astropysics.constants import c,G

a=[2,3,4,3,4,2]

mean=numpy.mean(a)

print "Mean :",mean
