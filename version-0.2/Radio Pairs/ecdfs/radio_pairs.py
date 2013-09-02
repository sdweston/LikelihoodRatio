#===========================================================================
#
# radio_pairs.py
#
# Python script to query SWIRE_ES1 mysql database to try and match radio
# pairs.
#
#===========================================================================
#
# S. Weston
# AUT University
# May 2013
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

# Definitions and Global Variables
# Database 
global db_host
db_host='localhost'
global db_user
db_user='atlas'
global db_passwd
db_passwd='atlas'

#

print "\nStarting Radio Pair Search"

# Connect to the local database with the atlas uid

db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from coords a list of all the radio sources with ra & dec

db.query("select t1.cid, t1.ra_deg, t1.dec_deg, t2.sint \
          from elais_s1.coords as t1, elais_s1.table4 as t2 \
          where t2.cid=t1.cid;")
		      
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=5000)

for row in rows:

    cid=row[0]
    ra_deg=row[1]
    dec_deg=row[2]
    sint1=row[3]
	
#   Now for each radio source find those within sq 100" 
#   We need flux of each also angular seperation

    db.query("select t1.cid, \
              sqrt(pow((%s-t1.ra_deg)*cos(%s),2)+pow(%s-t1.dec_deg,2))*3600 \
              from elais_s1.coords as t1 \
              where pow((%s-t1.dec_deg)*cos(%s),2)+ \
                    pow(%s-t1.dec_deg,2) <= pow(300/3600,2) \
              and t1.cid != '%s';" % (ra_deg,dec_deg,dec_deg, ra_deg,dec_deg,dec_deg,cid)) 
			  
    r2=db.use_result()
    rows2=r2.fetch_row(maxrows=100)

    for row2 in rows2:
        print row2
