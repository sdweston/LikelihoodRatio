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

# ask which field to process
answer=raw_input('Which field cdfs/elais ?')
print "\nentered : ",answer,"\n"

if answer == 'cdfs':
   schema='atlas_dr3' 
   field='cdfs'
   swire_schema='swire_cdfs'
else:
   schema='atlas_dr3' 
   field='elais'
   swire_schema='swire_es1'
   
print "Field : ",field," ; swire_schema : ",swire_schema

# now the field string is the same as the database schema name.

# notify use of nearest neigbour search radius

answer=raw_input('Nearest neighbour search radius (%s arcsec) :' % (sr))

if answer !='':
    sr=answer
    print "New nearest neighbour search radius : ",answer,"\n"

execfile('area_none_radio_survey.py')
execfile('radio_pairs.py')
execfile('populate_matches.py')
execfile('f_r.py')
execfile('n_m.py')
execfile('q_0.py')
execfile('total_m.py')
execfile('real_m.py')
execfile('q_m.py')
execfile('plot_m.py')
execfile('likelihoodratio.py')
execfile('reliability.py')
execfile('plot_lr_vs_rel.py')

auks()
print_header()	

# First truncate all the working tables in the database

# Calculate the spherical area of the none-radio survey being used
# for cross matching to get an accurate measure of the area for determining
# the background source density per unit area.

area_nr=area_none_radio_survey()
print "Area's returned  : %f %f" % (area_nr[0],area_nr[1])

global atlas_sqasec
atlas_sqasec=area_nr[0]

global swire_sqsec
swire_sqsec=area_nr[1]

# First pass for possible radio pairs, so that matches runs against new 
# generated source for radio pair.

answer=raw_input('Run radio pair search (y/n)       : ')

if (answer =='Y' or answer=='y'):
    print "Run radio pair search        : ",answer,"\n"
    rp()

# Fine the nearest neighbour matches within search radius

answer=raw_input('Run nearest neighbour match (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Run nearest neighbour match  : ",answer,"\n"
    pm()

# Determine f(r) and update the database.

answer=raw_input('Run f(r) calculations       (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing f(r) calculations                 : ",answer,"\n"
    f_r()

# Determine n(m) and update data base

answer=raw_input('Run n(m) calculations       (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing n(m) calculations                 : ",answer,"\n"
    n_m()

# Determine the Q0 at this point as we have n_m
#q_0()

print "You need Q0 for q(m) & Rel calculations latter"
answer=raw_input('Run q0 calculations         (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing q0 ) calculations                 : ",answer,"\n"
    q_0()

# Determine total(m) and update data base

answer=raw_input('Run total(m) calculations   (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing total(m) calculations             : ",answer,"\n"
    total_m()


# Determine r(m) and update database

answer=raw_input('Run real(m) calculations    (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing real(m) calculations              : ",answer,"\n"
    real_m()
#real_m()

# Determine q(m) and update database

answer=raw_input('Run q(m) calculations       (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing q(m) calculations                 : ",answer,"\n"
    q_m()

#q_m()

# Plot n(m), q(m) and total(m)
plot_m()

# Calculate LR

answer=raw_input('Run LR  calculations       (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing LR calculations                  : ",answer,"\n"
    lr()


# Calculate Reliability

answer=raw_input('Run Rel  calculations       (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing Rel calculations                  : ",answer,"\n"
    rel()

# Plot LR vs Reliability

plot_lr_rel()

print_end()
