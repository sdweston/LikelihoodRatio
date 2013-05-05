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
import sys
import matplotlib.pyplot as plt

#print math.pi

print "Starting f(r) calculations and db updates"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry

db.query("select t1.cid,t2.swire_es1_index_spitzer,t1.dbmaj,t1.dbmin,t1.sint,t1.rms,t2.r_arcsec \
          from elais_s1.table4 as t1 left outer join elais_s1.matches t2 \
          on t2.elais_s1_cid=t1.cid \
          order by t1.cid;")
          
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

RADIUS=[]
F_R=[]

for row in rows:
    cid=row[0]
    index_spitzer=row[1]
    dbmaj=row[2]
    dbmin=row[3]
    sint=float(row[4])
    rms=float(row[5])
    if row[6]==None:
        continue
    r=float(row[6])
    
#    print cid, index_spitzer,dbmaj,dbmin,sint,rms,r
    sys.stdout.write('.')
    

# if dbmaj or dbmin are a string "None" then continue with next iteration

    if dbmaj==None:
        continue
    if dbmin==None:
        continue

# Need Sint & rms in same units muJy
# Sint is in mJy 10-3
# rms is in muJy 10-6

#    print "CID           : ",cid
    DBMAJ=float(dbmaj)
    DBMIN=float(dbmin)

    RMS=rms/1000
#    print "RMS           : ",RMS

# ACE - ancillary catalogue error, arcsec's

    ACE=0.1

# IRE - intrensic radio error, arcsec's

    IRE=0.6

# Work out SNR

    SNR = sint/RMS
#    print "SNR           : ",SNR

# Work out FWHM

# Calculate Sigma

    sigma_x=math.sqrt((DBMAJ/(2*SNR))**2 + ACE**2 + IRE**2)
#    print "Sigma X       : ",sigma_x

    sigma_y=math.sqrt((DBMIN/(2*SNR))**2 + ACE**2 + IRE**2)
#    print "Sigma Y       : ",sigma_y

#   sigma is the mean of sigma_x and sigma_y
    sigma=(sigma_x + sigma_y)/2
#    print "Sigma         : ",sigma

# r is the radial distance between the radio source and the aux catalogue source
# r was returned from the sql in the matches table

# Calculate f(r)

    f_r=(1/(2*math.pi*sigma**2)) * math.exp(-r**2/2*sigma**2)
    F_R.append(f_r)
    RADIUS.append(r)
#    print "cid   index_spitzer   f(r) : ",cid,index_spitzer,f_r
#    print "\n"

# Populate new table with cid,BS,SNR,f(r), or put back into matches table.
#    db.query("update elais_s1.matches set f_r=%s,snr=%s where elais_s1_cid='%s' \
#              and swire_es1_index_spitzer='%s';" % (f_r, SNR, cid, index_spitzer))

# End of do block

# Close connection to the database
db.close()

plt.plot(RADIUS, F_R,'k.')
plt.title(' ATLAS/ELAIS_S1     f(r) vs r')
plt.ylabel('f(r)')
plt.xlabel('r (arcsec)')
plt.savefig("atlas-elasis_s1_fr_vs_r.ps")
plt.show()

print "End"


