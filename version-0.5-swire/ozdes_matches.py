#===========================================================================
#
# populate_matches.py
#
# Python script to query mysql database to determine the
# nearest neigbours within search radius between catalogues
#
#===========================================================================
#
# S. Weston
# AUT University
# Sept 2014
#===========================================================================

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

print "\nStarting finding nearest neighbours between catalogues\n"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

   
print "find OzDES NN to fusion.swire_elais\n"

# Use SWIRE (cdfs/elais)_swire-sdss-cat-plus-full
 
sql1=("select t1.cid,t2.ra,t2.decl,t1.swire_index_spitzer,t3.ra_spitzer,t3.dec_spitzer,t1.reliability "
      " from atlas_dr3.elais_matches as t1, atlas_dr3.elais_coords as t2, fusion.swire_elais as t3 "
      " where t1.cid=t2.id "
      " and t1.swire_index_spitzer=t3.index_spitzer "
      " and t1.reliability > 0.8; ")

print sql1,"\n"
	
print "This SQL will take a while .... \n"
db.query(sql1)
    
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=0)

# Close connection to the database

db.close()	

lst_rows=list(rows)

for row in lst_rows:
    cid=row[0]
    ra_radio=float(row[1])
    dec_radio=float(row[2])
    sid=row[3]
    ra_ir=float(row[4])
    dec_ir=float(row[5])
    rel=float(row[6])

    print cid,ra_radio,dec_radio,sid,ra_ir,dec_ir,rel

#   Find NN to the IR Candidate from OzDES

    sql2=("
	
print "End of populate matches\n"





