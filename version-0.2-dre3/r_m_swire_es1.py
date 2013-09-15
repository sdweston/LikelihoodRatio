#===========================================================================
#
# r_m_swire_es1.py
#
# Python script to query ELAIS_ES1 mysql database to determine the
# real(m) for the likelihood ratio.
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
import math
import numpy
import matplotlib.pyplot as plt

print "Starting real(m) calculations and db updates"

execfile('constants.py')

# Constants for the non-radio survey area
# sqdeg - square degrees
# sqasec - square arc seconds
sqdeg=nr_area
sqasec=sqdeg*3600*3600

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry

db.query("select total_m,n_m FROM swire_es1.n_m_lookup;")

# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=0)

# Close connection to the database

db.close()

#The other oddity is: Assuming these are numeric columns, why are they returned 
#as strings? Because MySQL returns all data as strings and expects you to 
#convert it yourself. This would be a real pain in the ass, but in fact, _mysql 
#can do this for you. (And MySQLdb does do this for you.) To have automatic 
#type conversion done, you need to create a type converter dictionary, and pass 
#this to connect() as the conv keyword parameter.

area=nrs * math.pi * math.pow(10.0,2)
print "Area          : %f " % area
print "Back Grd Area : %f " % sqasec

total_m=[]
n_m=[]
real_m=[]
background_m=[]
sum_real_m=0.0
print "Total(m) n(m) r(m) backgrd"
for row in rows:
    # a is total(m)
    a=float(row[0])
    # b is n(m)
    b=float(row[1])
    # r is 10"
    # c is real(m)

#   Assume a % of area lost due to contamination from forground stars
    area_pct=0.96
    
    bck_grd=(b/(sqasec * area_pct)) * nrs * math.pi * math.pow(10.0,2)
    c= a - ((b/(sqasec * area_pct)) * nrs * math.pi * math.pow(10.0,2))
    total_m.append(a)
    n_m.append(b)
    if c < 0:
       c=0
       
    sum_real_m=sum_real_m+c
    real_m.append(c)
    background_m.append(bck_grd)
    print " %14.9f %14.9f %14.9f %14.9f" % (a, b, c, bck_grd)

print "Sum real(m) : " ,sum_real_m

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
db.query("set autocommit=0;")

i=1
for item in xrange(len(total_m)):
    r_m=real_m[item]
    b_m=background_m[item]
    db.query("update swire_es1.n_m_lookup set real_m='%f', bckgrd_m='%f' \
              where i='%d';" % (r_m, b_m, i))
    db.commit()
    i=i+1

db.commit()

# Close connection to the database
db.close()

print "End"





