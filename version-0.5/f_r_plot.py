#===========================================================================
#
# f_r.py
#
# Python script to query SWIRE_ES1 mysql database to plot the
# f(r) vs r for the likelihood ratio.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

import math
import array
import _mysql
import numpy
import scipy
import matplotlib.pyplot as plt
import astropysics as astro
import pylab
import sys

pie=math.pi

#def f_r_plot():

# ask which field to process
answer=raw_input('Which field cdfs/elais ?')
print "\nentered : ",answer,"\n"

print "Plotting f(r) calculations vs radius"

if answer == 'cdfs':
   schema='atlas_dr3' 
   field='cdfs'
   swire_schema='swire_cdfs'
   beam_maj=16.8
   beam_min=6.9
   beam_posn_ang=1.0
   posn_offset_ra=0.0
#   snr = 5.0 #cdfs snr_min
   snr=60.20 # cdfs snr_avg
#   snr=23135.61 # cdfs snr_max
else:
   schema='atlas_dr3' 
   field='elais'
   swire_schema='swire_es1'
   beam_maj=12.2
   beam_min=7.6
   beam_posn_ang=-11.0
#   snr=5.0 #elais snr_min
   snr = 47.94 # elais snr_avg
#   snr=8125 # elais snr_max
#  See Middelberg et al 2007
   posn_offset_ra=0.06
   posn_offset_dec=0.08

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
# table4 for atlas.elais and atlas.cdfs are not consistent. Rename column dbmaj,dbmin to be majaxis,minaxis for both tables !

sql1="select f_r,r_arcsec from atlas_dr3."+field+"_matches where f_r is not null"
db.query(sql1)

		  
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=6000)

# rows is a tuple, convert it to a list

#lst_rows=list(rows)

#print rows

r_arcsec=[]
f_r=[]
irows=0

for row in rows:

        f_r.append(float(row[0]))
        r_arcsec.append(float(row[1]))
        irows=irows+1

print "Rows : ",irows
        
# End of do block

# Close connection to the database
db.close()

# Calculate the f(r) function using avg(snr) and beam_maj, beam_min

# ACE - ancillary catalogue error, arcsec's

ACE=0.1

# IRE - intrensic radio error, arcsec's

IRE=0.6

#    print "SNR           : ",SNR

# Work out FWHM

# Calculate Sigma

# 0.655 see Smith et al 2011, Page 7
#sigma_x=math.sqrt((0.6*(beam_min/snr))**2 + ACE**2 + IRE**2)
sigma_x=((0.655*(beam_min/snr))**2 )
#    print "Sigma X       : ",sigma_x

#sigma_y=math.sqrt((0.6*(beam_maj/snr))**2 + ACE**2 + IRE**2)
sigma_y=((0.655*(beam_maj/snr))**2 )
#    print "Sigma Y       : ",sigma_y

#   sigma is the mean of sigma_x and sigma_y
#   sum in quadrature ?
#sigma=(sigma_x + sigma_y)/2
sigma=(sigma_x + sigma_y + ACE**2 + IRE**2)
#    print "Sigma         : ",sigma

x = numpy.linspace(0,10,1000) # 1000 linearly spaced numbers
y = numpy.exp(-x**2/(2*sigma))*(1/(2*pie*sigma))

#

plt.plot(r_arcsec, f_r,'k.')
plt.plot(x,y)
plot_title='ATLAS ' +field+ ' f(r) vs r'
plt.title(plot_title)
plt.ylabel('f(r)')
plt.xlabel('r (arcsec)')

plt.xlim(0.0,10.0)
#plt.yscale('log')
plt.ylim(0.0,0.5)

output_dir="D:/temp/"
plot_fname='atlas_' +field+ '_fr_vs_r.eps'
fname=output_dir + plot_fname
plt.savefig(fname,format="eps")
plt.show()

print "\nEnd of Plot f(r)"


