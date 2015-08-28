#===============================================================================
# UpdateSuperCosmos.py
# This program takes the ra,dec by epoch and converts
# ra,dec to J2000 then updates new coord columns with
# this new epoch
#===============================================================================

import sys
import math
import array
import random
#import _mysql
import MySQLdb
import ephem
import string

#===============================================================================

execfile('astroTools.py')

#===============================================================================

db=MySQLdb.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry, find the records

#db.query("select id,ra,decl,epoch from supercosmos_gama12.supercosmos_gama12 limit 0,3000000;")
db.query("select id,ra,decl,epoch from supercosmos_gama12.supercosmos_gama12 limit 10;")

r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=0)

# Close connection to the database

db.close()

s_count=[]

for row in rows:
    print "Row : ",row
    id=row[0]
    ra=float(row[1])
    dec=float(row[2])
    epoch=row[3]
	
    #print id,ra,dec,epoch

    ra_hms=deg2HMS(ra)
    dec_dms=deg2DMS(dec)

    print ra_hms,dec_dms,epoch
    arg='01,f|H,'+ra_hms+','+dec_dms+',1.0,'+str(epoch)
    #print arg
    sc01=ephem.readdb(arg)
    sc01.compute(epoch=str(epoch))
    sc01.compute(epoch='2000')
    print('%s %s J2000' %(sc01.a_ra, sc01.a_dec))

    ra1=sc01.a_ra
    dec1=sc01.a_dec

    print ra1,dec1
    
    ra_deg=convHMS(str(ra1))
    dec_deg=convDMS(str(dec1))

    print ra_deg, dec_deg

    # OK insert the J2000 coords back into the database by id !

# OK we are done
    
