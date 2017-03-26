#===========================================================================
#
# plot_radio_pairs.py
#
# Python script to query SWIRE_ES1 mysql database to 
# select from matches the IR Flux, Radio Flux, Redshift etc so we can do some science
# Plot the colour colour 
# Plot the colour magnitude
#
#===========================================================================
#
# S. Weston
# AUT University
# Nov 2013
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

# Database 
global db_host
db_host='localhost'
global db_user
db_user='atlas'
global db_passwd
db_passwd='atlas'

print "\nStarting Plot Science"

#   Connect to the local database with the atlas uid

db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from matches the IR Flux, Radio Flux, Redshift etc so we can do some science

db.query("select flux1/flux2,ang_sep_arcsec/log10(flux1+flux2) from v_0_3.radio_pairs where flux1/flux2 > 1.0 limit 0,10000;")
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

flux_ratio=[]
ang_sep_flux=[]

for row in rows:
    print row[0], row[1]
    flux_ratio.append(float(row[0]))
    ang_sep_flux.append(float(row[1]))
	
	        	
#    End of do block

# Close connection to the database
db.close()

# Now plot the data

plt.yscale('log')
plt.xscale('log')
plt.plot( ang_sep_flux,flux_ratio,'k.')
plt.title(' Radio Pairs')
plt.ylabel('flux1/flux2')
plt.xlabel('ang_sep/log10(flux1-flux2)')
plt.grid(True)
plt.show()

print "End Plotting\n"


