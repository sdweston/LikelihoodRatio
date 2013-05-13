#===========================================================================
#
# f_r_swire_es1.py
#
# Python script to query SWIRE_ES1 mysql database to determine the
# f(r) for the likelihood ratio.
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

#print math.pi

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry

db.query("select t1.cid,t1.dbmaj,t1.dbmin,t1.sint,t1.rms,t2.ra_deg,t2.dec_deg \
          FROM elais_s1.table4 t1 \
	  inner join elais_s1.coords t2 \
          on t1.cid=t2.cid  \
          where t2.ra_deg > 8.4 and t2.ra_deg < 10.4 \
          and t2.dec_deg < -43.0 and t2.dec_deg > -45.0;")

# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=2000)

# rows is a tuple, convert it to a list

#lst_rows=list(rows)

#print rows

for row in rows:
    cid=row[0]
    dbmaj=row[1]
    dbmin=row[2]
    sint=float(row[3])
    rms=float(row[4])
    print cid
    print dbmaj
    print dbmin
    print sint
    print rms

# if dbmaj or dbmin are a string "None" then continue with next iteration

    if dbmaj==None:
        continue
    if dbmin==None:
        continue

# Need Sint & rms in same units muJy
# Sint is in mJy 10-3
# rms is in muJy 10-6

    print "CID           : ",cid
    DBMAJ=float(dbmaj)
    DBMIN=float(dbmin)

    RMS=rms/1000
    print "RMS           : ",RMS

# ACE - ancillary catalogue error, arcsec's

    ACE=0.1

# IRE - intrensic radio error, arcsec's

    IRE=0.6

# Work out SNR

    SNR = sint/RMS
    print "SNR           : ",SNR

# Work out FWHM

# Calculate Sigma

    sigma_x=math.sqrt((DBMAJ/(2*SNR))**2 + ACE**2 + IRE**2)
    print "Sigma X       : ",sigma_x_radio

    sigma_y=math.sqrt((DBMIN/(2*SNR))**2 + ACE**2 + IRE**2)
    print "Sigma Y       : ",sigma_y_radio

#   sigma is the mean of sigma_x and sigma_y
    sigma=(sigma_x + sigma_y)/2
    print "Sigma         : ",sigma

# r is the radial distance between the radio source and the aux catalogue source
    r=3.0

# Calculate f(r)

    f_r=(1/(2*math.pi*sigma**2)) * math.exp(-r**2/2*sigma**2)
    print "f(r)          : ",f_r
    print "\n=====\n"
# Populate new table with cid,BS,SNR,f(r), or put back into matches table.

    db.query("update elais_s1.matches set f_r=%s where elais_s1_cid='%s';" % (f_r, cid))

# End of do block

# Close connection to the database
db.close()    


