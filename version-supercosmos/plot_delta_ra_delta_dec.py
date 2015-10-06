#===========================================================================
#
# plot_m.py
#
# Python script to query SWIRE_ES1 mysql database to plot the 
# catalog position offsets between ATLAS-Radio and Swire-IR for the
# nearest neighbour candidates.
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
import MySQLdb
import numpy
import scipy
import matplotlib.pyplot as plt
import astropysics as astro
import pylab
import sys

output_dir='D:/temp/'

# Database 
global db_host
db_host='localhost'
global db_user
db_user='atlas'
global db_passwd
db_passwd='atlas'

print "\nStarting Plot Delta RA vs Delta Dec"

# Load in the definitions and constants
execfile('constants.py')

#==================================================================

#   Connect to the local database with the atlas uid

db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)
#db=_mysql.connect(host="localhost",user="root")
#db=MySQLdb.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from matches the sum of L_i grouped by radio source

sql01="select t1.dx, t1.dy \
     from "+schema+"."+schema+"_matches as t1 "

db.query(sql01)
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=0)

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
plt.axis('equal')
plt.grid(True)
plot_title=' Catalog Position Offset'
plt.title(plot_title)
plt.ylabel('Delta Dec')
plt.xlabel('Delta RA')
#plot_fname='nvss_supercosmos_cat_posn_offset.pdf'
#fname=output_dir + plot_fname
#plt.savefig(fname)
plt.show()




