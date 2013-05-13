# randomcats.py
# This program makes a random catalogue based on the FUSION catalogue

import sys
import math
import array
import random
#import _mysql
import MySQLdb
import numpy
import matplotlib.pyplot as plt
import astropysics as astro
import re

from astropysics.constants import c,G


#===================================================================================================
#

db=MySQLdb.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry, find the number of records

db.query("select t1.cid,t1.RA_Deg ,t1.Dec_Deg from elais_s1.coords as t1 limit 0,100;")

r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=0)

# Close connection to the database

db.close()

# open a new catalogue file

#db.query("insert into ecdfs.cdfs_randomcat(id,ra,declination) values ('%s','%f','%f');" % (id_str,fake_ra,fake_dec))

s_count=[]
icount=0
db=MySQLdb.connect(host="localhost",user="atlas",passwd="atlas")
cur=db.cursor()

for row in rows:
    if icount==10:
        sys.stdout.write('.')
        icount=0
    else:
        icount +=1

#    print "Row : ",row
    id=row[0]
    ra=float(row[1])
    dec=float(row[2])
    cur.execute("select count(index_spitzer) from swire_es1.es1 as t2 where pow((%f-t2.RA_SPITZER)*cos(%f),2)+ pow(%f-t2.DEC_SPITZER,2) <= pow(100/3600,2);" % (ra,dec,dec))
    result=cur.fetchone()
#    print "Result: %s" % result
    s_count.append(int(result[0]))
#    db.close()
	  

# where pow((t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg),2)+
#      pow(t1.Dec_Deg-t2.DEC_SPITZER,2) <= pow(2/3600,2)
 
# Close connection to the database
db.close()

s_count_mean=numpy.mean(s_count)
print "Mean Source Count with in radius: ",s_count_mean


         

