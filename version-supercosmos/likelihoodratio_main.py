import math
import array
import _mysql
import numpy 
import scipy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import astropysics as astro
import pylab
import sys
import random

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
    global dradian
    dradian=math.pi/180

# NOTE: all trig funcations use radian's !
# so multiply degrees by "dradian"
# In the database tables we have decimal degrees
# for sql use the radians functions, ie cos(radians(deg))

def print_header():
	print "Likelihood Ratio"
	
def print_end():
    print "End"

#===================================================================================================


beam_maj=12.2
beam_min=7.6
beam_posn_ang=-11.0

   

# notify use of nearest neigbour search radius

# From Nick: The NVSS FWHM is 45” so perhaps we should use a 20” search radius

answer=raw_input('Nearest neighbour search radius (20 arcsec) :')

if answer !='':
    sr=float(answer)
    print "New nearest neighbour search radius : ",sr,"\n"
else:
    sr=20.0

# Magnitude Distribution of Background Sources - Method

print "Magnitude Distribution of Background Sources Method\n"
print " 1 - search radii \n"
print " 2 - whole background catalogue \n"
mdbs=raw_input('Which method 1 or 2 (default 2) :')

if mdbs !='1' and mdbs!='2':
   mdbs='2'

print "\nMethod : ",mdbs,"\n"

execfile('random_foreground_catalogue.py')
execfile('find_blanks_random.py')
execfile('find_blanks_real.py')
	
execfile('area_background_survey.py')
#execfile('radio_pairs.py')
execfile('populate_matches.py')
execfile('f_r.py')
execfile('n_m.py')
#execfile('q_0.py')
execfile('total_m.py')
execfile('real_m.py')
#execfile('q_m.py')
#execfile('plot_m.py')
#execfile('likelihoodratio.py')
#execfile('reliability.py')
#execfile('plot_lr_vs_rel.py')

auks()
print_header()	

# First truncate all the working tables in the database

# Prepare base data, random catalogue etc

print "This next step only need to be done once at the begining !"

answer=raw_input('Run create a new random foreground catalogue (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Create a new random foreground catalogue : ",answer,"\n"
    random_foreground_catalogue()
    find_blanks_random()
    find_blanks_real()

# Calculate the spherical area of the none-radio survey being used
# for cross matching to get an accurate measure of the area for determining
# the background source density per unit area.

area_nr=area_background_survey()
print "Area's returned  : %f %f" % (area_nr[0],area_nr[1])

global nvss_sqasec
nvss_sqasec=area_nr[0]

global supercosmos_sqsec
supercosmos_sqsec=area_nr[1]


# Fine the nearest neighbour matches within search radius

answer=raw_input('Run nearest neighbour match (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Run nearest neighbour match  : ",answer,"\n"
    pm()


# Determine f(r) and update the database.

print "You need sigma from f(r) for Q_0 calculations latter"
answer=raw_input('Run f(r) calculations       (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing f(r) calculations                 : ",answer,"\n"
    f_r()

# Determine n(m) and update data base

answer=raw_input('Run n(m) calculations       (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing n(m) calculations                 : ",answer,"\n"
    n_m()

"""
# Determine the Q0 at this point as we have n_m
#q_0()

print "You need Q0 for q(m) & Rel calculations latter"
answer=raw_input('Run q0 calculations         (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing q0 ) calculations                 : ",answer,"\n"
    q_0()

# Determine total(m) and update data base
"""

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

"""
# Determine q(m) and update database

answer=raw_input('Run q(m) calculations       (y/n) : ')

if (answer =='Y' or answer=='y'):
    print "Runing q(m) calculations                 : ",answer,"\n"
    q_m()

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
"""
