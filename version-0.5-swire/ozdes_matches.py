#===========================================================================
#
# ozdes_matches.py
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

print "\nStarting finding nearest neighbours between OzDES and FUSION \n"

# ask which field to process
answer=raw_input('Which field cdfs/elais ?')
print "\nentered : ",answer,"\n"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

   
print "find OzDES NN to fusion.swire_elais\n"

# Use SWIRE (cdfs/elais)_swire-sdss-cat-plus-full
 
sql1=("select t1.cid,t2.ra,t2.decl,t1.swire_index_spitzer,t3.ra_spitzer,t3.dec_spitzer,t1.reliability,t1.swire_index_spitzer "
      " from atlas_dr3."+answer+"_matches as t1, atlas_dr3."+answer+"_coords as t2, fusion.swire_"+answer+" as t3 "
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

#db.close()	

lst_rows=list(rows)

for row in lst_rows:
    cid=row[0]
    ra_radio=float(row[1])
    dec_radio=float(row[2])
    sid=row[3]
    ra_ir=float(row[4])
    dec_ir=float(row[5])
    rel=float(row[6])
    sis=row[7]

    error=2.0/3600.0
    ra1=ra_ir-error
    ra2=ra_ir+error

    dec1=dec_ir-error
    dec2=dec_ir+error

    print cid,ra_radio,dec_radio,sid,ra_ir,dec_ir,rel
#    print error,ra1,ra2,dec1,dec2

#   Find NN to the IR Candidate from OzDES, using 1" radius
#   Set limits on search to within say 2" of IR source.

# "where pow((t1.ra-"+str(posn_offset_ra)+"-t2.RA_Spitzer)*cos(radians(t1.decl-"+str(posn_offset_dec)+")),2)+" 
# "pow(t1.decl-"+str(posn_offset_dec)+"-t2.Dec_Spitzer,2) <= pow("+str(sr)+"/3600,2) "

#          "where pow(("+str(ra_ir)+"-RA)*cos("+str(dec_ir)+"),2)+ "
#          "pow("+str(dec_ir)+"-DECL,2) <= pow(2/3600,2) "

    sql2=("select id,ra,decl,z, "
          "pow(("+str(ra_ir)+"-RA)*cos("+str(dec_ir)+"),2)+ pow("+str(dec_ir)+"-DECL,2) "
          "from ozdes.ozdes_grc_2016_02_25 "
          "where pow(("+str(ra_ir)+"-RA)*cos("+str(dec_ir)+"),2)+ "
          "pow("+str(dec_ir)+"-DECL,2) <= pow(1.0/3600.0,2) "
          "and   RA > "+str(ra1)+" and RA < "+str(ra2)+" "
          "and   DECL > "+str(dec1)+" and DECL < "+str(dec2)+" limit 0,3000000; ")

#    print sql2
     
    db.query(sql2)
    
    r=db.use_result()
     
    nns=r.fetch_row(maxrows=0)

    print nns

    for nn in nns:
        ozdes_id=nn[0]
        ra_ozdes=float(nn[1])
        dec_ozdes=float(nn[2])
        ozdes_z=float(nn[3])

        print ozdes_z

#   Having found a match, update the ozdes_z column on the matches table

        sql3=("update atlas_dr3."+answer+"_matches "
             "set ozdes_z="+str(ozdes_z)+",ozdes_id='"+ozdes_id+"' "
             "where cid='"+cid+"' and swire_index_spitzer='"+sis+"';")
        print sql3
        db.query(sql3)
    
# Close connection to the database

db.close()
	
print "End of OzDES matches\n"





