import math
import array
import _mysql
import numpy
import scipy
import matplotlib.pyplot as plt
import astropysics as astro
import pylab
import sys

from astropysics.constants import c,G

# Load in the definitions and constants
execfile('constants.py')
    
def auks():
    global pie
    global e
    global eradian
    pie=math.pi
    e=math.e
    eradian=180.0/math.pi

def print_header():
	print "Likelihood Ratio"
	
def print_end():
    print "End"

#===================================================================================================

execfile('area_none_radio_survey.py')
execfile('f_r.py')
execfile('n_m.py')

auks()
print_header()	
print "Pi      :",pie
print "e       :",e
print "eradian :",eradian

#Print physical constants
print "c       :",c
print "G       :",G

# First truncate all the working tables in the database

# Calculate the spherical area of the none-radio survey being used
# for cross matching to get an accurate measure of the area for determing
# the bacground source density per unit area.

area=area_none_radio_survey()
print "Area returned  : %f" % area

# Determine f(r) and update the database.
#f_r()

# Determine n(m) and update data base
n_m()

print_end()
