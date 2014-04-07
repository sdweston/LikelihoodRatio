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

#def f_r_plot():

field="elais_s1"

print "Starting f(r) calculations and db updates"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
# table4 for atlas.elais and atlas.cdfs are not consistent. Rename column dbmaj,dbmin to be majaxis,minaxis for both tables !

sql1="select f_r,r_arcsec from "+field+".matches where f_r is not null"
db.query(sql1)

		  
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

#lst_rows=list(rows)

#print rows

r_arcsec=[]
f_r=[]

for row in rows:

        f_r.append(float(row[0]))
        r_arcsec.append(float(row[1]))
        
# End of do block

# Close connection to the database
db.close()

plt.plot(r_arcsec, f_r,'k.')
plot_title='ATLAS ' +field+ ' f(r) vs r'
plt.title(plot_title)
plt.ylabel('f(r)')
plt.xlabel('r (arcsec)')

output_dir="F:/temp/"
plot_fname='atlas_' +field+ '_fr_vs_r.ps'
fname=output_dir + plot_fname
plt.savefig(fname)
plt.show()

print "\nEnd of Plot f(r)"


