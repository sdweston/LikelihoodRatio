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

# Database 
global db_host
db_host='localhost'
global db_user
db_user='atlas'
global db_passwd
db_passwd='atlas'

print "\nStarting Plot Delta RA vs Delta Dec"

#   Connect to the local database with the atlas uid

db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from matches the sum of L_i grouped by radio source

sql01="select t2.ra-t3.ra_spitzer, t2.declination-t3.dec_spitzer \
     from atlas.elais_matches t1, atlas.dr3_elais_cmpcat t2, \
     swire_es1.es1 t3 \
     where t1.cid=t2.id \
     and t1.swire_index_spitzer=t3.index_spitzer"

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
        delta_ra.append(float(row[0]))
        delta_dec.append(float(row[1]))
        
	
#    End of do block

# Close connection to the database
db.close()

# Now plot the data

plt.plot(delta_ra,delta_dec,'k.')
plot_title=' Catalog Offset'
plt.title(plot_title)
plt.ylabel('Delta Dec')
plt.xlabel('Delta RA')
#    plot_fname='atlas_'+field+'_magnitude_dependance.ps'
#    fname=output_dir + plot_fname
#    plt.savefig(fname)
plt.show()
    
print "End Plotting\n"


