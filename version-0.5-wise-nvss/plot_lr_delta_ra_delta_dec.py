#===========================================================================
#
# plot_m.py
#
# Python script to query SWIRE_ES1 mysql database to determine the
# LR the likelihood ratio.
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

from matplotlib.ticker import MaxNLocator

output_dir='D:/temp/'

# Define reliability limit

rel_lim='0.99'

# Database 
global db_host
db_host='localhost'
global db_user
db_user='atlas'
global db_passwd
db_passwd='atlas'

print "\nStarting Plot Delta RA vs Delta Dec"
print "Field ELAIS\n"

#   Connect to the local database with the atlas uid

db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from matches the sum of L_i grouped by radio source

sql01="SELECT dx,dy FROM atlas_dr3.elais_matches \
      where reliability > "+rel_lim+";"
	  
db.query(sql01)
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

delta_ra=[]
delta_dec=[]
    
for row in rows:
#        print row
        delta_ra.append(float(row[0])*3600)
        delta_dec.append(float(row[1])*3600)
        
	
#    End of do block

# Close connection to the database
db.close()

# Now plot the data
#fig,ax=plt.subplots()
#ax.autoscale(enable=False)
plt.plot(delta_ra,delta_dec,'k.')
plt.axis([-10.0,10.0,-10.0,10.0])
plt.axis('equal')
#ax.xaxis.set_major_locator(MaxNLocator(5))
#ax.yaxis.set_major_locator(MaxNLocator(5))
plt.grid(True)
plot_title=' Catalog Position Offsets - ELAIS'
plt.title(plot_title)
plt.ylabel('Delta Dec arc seconds')
plt.xlabel('Delta RA arc seconds')
plot_fname='lr_rel_gt_0p8_atlas_dr3_elais_cat_posn_offset.pdf'
fname=output_dir + plot_fname
plt.savefig(fname)
plt.show()

# Now bin the data by "r" for delta_x and delta_y and plot bins.

(hist,bins)=numpy.histogram(delta_ra,bins=40,range=[-5.0,5.0])
width = 0.7*(bins[1]-bins[0])
center = (bins[:-1]+bins[1:])/2

plt.bar(center, hist, align = 'center',width = width,linewidth=0)
plot_title='Delta RA'
plt.title(plot_title)
plt.grid(True)
plt.ylabel('n(delta_ra)')
plt.xlabel('Delta RA (arcsec)')
plot_fname='atlas_elais_delta_ra.ps'
output_dir='D:/temp/'
fname=output_dir + plot_fname
plt.savefig(fname)
plt.show()

(hist,bins)=numpy.histogram(delta_dec,bins=40,range=[-5.0,5.0])
width = 0.7*(bins[1]-bins[0])
center = (bins[:-1]+bins[1:])/2

plt.bar(center, hist, align = 'center',width = width,linewidth=0)
plot_title='Delta DEC'
plt.title(plot_title)
plt.grid(True)
plt.ylabel('n(delta_dec)')
plt.xlabel('Delta DEC (arcsec)')
plot_fname='atlas_elais_delta_dec.ps'
output_dir='D:/temp/'
fname=output_dir + plot_fname
plt.savefig(fname)
plt.show()

# Fit a Gaussian and determine FWHM.

# Take FWHM for Simga_x and Sigma_y

#==================================================================

print "Field ECDFS\n"
db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from matches the sum of L_i grouped by radio source

sql02="SELECT dx,dy FROM atlas_dr3.cdfs_matches \
      where reliability > "+rel_lim+";"

db.query(sql02)
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

delta_ra=[]
delta_dec=[]
    
for row in rows:
#        print row
        delta_ra.append(float(row[0])*3600)
        delta_dec.append(float(row[1])*3600)
        
	
#    End of do block

# Close connection to the database
db.close()

# Now plot the data

plt.plot(delta_ra,delta_dec,'k.')
plt.axis([-10.0,10.0,-10.0,10.0])
plt.axis('equal')
plt.grid(True)
plot_title=' Catalog Position Offsets - ECDFS'
plt.title(plot_title)
plt.ylabel('Delta Dec arc seconds')
plt.xlabel('Delta RA arc seconds')
plot_fname='lr_rel_gt_0p8_atlas_dr3_ecdfs_cat_posn_offset.pdf'
fname=output_dir + plot_fname
plt.savefig(fname)
plt.show()

print "End Plotting\n"

# Now bin the data by "r" for delta_x and delta_y and plot bins.

(hist,bins)=numpy.histogram(delta_ra,bins=40,range=[-5.0,5.0])
width = 0.7*(bins[1]-bins[0])
center = (bins[:-1]+bins[1:])/2

plt.bar(center, hist, align = 'center',width = width,linewidth=0)
plot_title='Delta RA'
plt.title(plot_title)
plt.grid(True)
plt.ylabel('n(delta_ra)')
plt.xlabel('Delta RA (arcsec)')
plot_fname='atlas_cdfs_delta_ra.ps'
output_dir='D:/temp/'
fname=output_dir + plot_fname
plt.savefig(fname)
plt.show()

(hist,bins)=numpy.histogram(delta_dec,bins=40,range=[-5.0,5.0])
width = 0.7*(bins[1]-bins[0])
center = (bins[:-1]+bins[1:])/2

plt.bar(center, hist, align = 'center',width = width,linewidth=0)
plot_title='Delta DEC'
plt.title(plot_title)
plt.grid(True)
plt.ylabel('n(delta_dec)')
plt.xlabel('Delta DEC (arcsec)')
plot_fname='atlas_cdfs_delta_dec.ps'
output_dir='D:/temp/'
fname=output_dir + plot_fname
plt.savefig(fname)
plt.show()

# Fit a Gaussian and determine FWHM.

# Take FWHM for Simga_x and Sigma_y
