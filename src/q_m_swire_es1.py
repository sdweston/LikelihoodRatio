#===========================================================================
#
# q_m_swire_es1.py
#
# Python script to query ELAIS_ES1 mysql database to determine the
# q(m) for the likelihood ratio.
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

print "Starting q(m) calculations and db updates"

# Constants
execfile('constants.py')

sum_real_m=810.785563462

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry

db.query("select real_m FROM swire_es1.n_m_lookup;")

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

#print rows

#The other oddity is: Assuming these are numeric columns, why are they returned 
#as strings? Because MySQL returns all data as strings and expects you to 
#convert it yourself. This would be a real pain in the ass, but in fact, _mysql 
#can do this for you. (And MySQLdb does do this for you.) To have automatic 
#type conversion done, you need to create a type converter dictionary, and pass 
#this to connect() as the conv keyword parameter.

q_m=[]
for row in rows:
    a=float(row[0])
    b=(a / sum_real_m ) * Q
    print "q(m) ",b
    q_m.append(b)

# insert q(m) into the lookup table

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
db.query("set autocommit=0;")

i=1
for item in xrange(len(q_m)):
    print item
    db.query("update swire_es1.n_m_lookup set q_m='%f' \
              where i='%d';" % (q_m[item], i))
    db.commit()
    i=i+1

db.commit()

# Close connection to the database
db.close()

print "End"





