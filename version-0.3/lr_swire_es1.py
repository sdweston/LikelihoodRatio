#===========================================================================
#
# lr_swire_es1.py
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

import array
import pylab
import _mysql
import numpy
import math
import sys
import matplotlib.pyplot as plt

print "Starting LR calculations and db updates"


execfile('constants.py')

# Constants for the non-radio survey area
# sqdeg - square degrees
# sqasec - square arc seconds
sqdeg=nr_area
sqasec=sqdeg*3600*3600

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry

db.query("select elais_s1_cid,swire_es1_index_spitzer,f_r,flux from elais_s1.matches \
          where f_r is not null and flux > -9.0;")
          
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

for row in rows:
    cid=row[0]
    index_spitzer=row[1]
    f_r=float(row[2])
    flux=float(row[3])
#    print "Flux %f" %flux
    sys.stdout.write('.')

#   check lookup table for values of q(m) and n(m)
	
    log10_f=math.log10(flux)
	
    db.query("select log10_f,n_m,q_m from swire_es1.n_m_lookup \
              where %s > log10_f - 0.05 \
              and %s < log10_f + 0.05;" % (log10_f, log10_f))
	
    r2=db.store_result()
    strings=r2.fetch_row(maxrows=1)

#    print log10_f,strings

    for string in strings:
        n_m=float(string[1])
        q_m=float(string[2])         

#    print "n(m) %20.9f q(m) %20.9f " % (n_m, q_m)
              
    lr = (q_m * f_r) / (n_m / sqasec)
        
#   print "Likelihood Ratio : %f " % lr
    
#   update table with likelihood ratio.

    db.query("update elais_s1.matches set lr=%s where elais_s1_cid='%s' \
              and swire_es1_index_spitzer='%s';" % (lr, cid, index_spitzer))

# End of do block

# Close connection to the database
db.close()

print "End"


