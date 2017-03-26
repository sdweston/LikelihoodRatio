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

db.query("select t1.cid,t1.RA_Deg ,t1.Dec_Deg from elais_s1.coords as t1 limit 0,5;")

r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=0)

# Close connection to the database

db.close()

# open a new catalogue file

#db.query("insert into ecdfs.cdfs_randomcat(id,ra,declination) values ('%s','%f','%f');" % (id_str,fake_ra,fake_dec))

s_count=[]

for row in rows:
    print "Row : ",row
    id=row[0]
    ra=float(row[1])
    dec=float(row[2])
    db=MySQLdb.connect(host="localhost",user="atlas",passwd="atlas")
    db.query("select count(index_spitzer) from swire_es1.es1 as t2 where pow((%f-t2.RA_SPITZER)*cos(radians(%f)),2)+ pow(%f-t2.DEC_SPITZER,2) <= pow(30/3600,2);" % (ra,dec,dec))
    result=db.use_result()
    count=result.fetch_row(maxrows=1)
    print "Result: ",count[1]
#    sc=re.findall(r'[0-9]+',count[0])
    s_count.append(count)
    db.close()
	  

# where pow((t1.RA_Deg-t2.RA_SPITZER)*cos(radians(t1.Dec_Deg)),2)+
#      pow(t1.Dec_Deg-t2.DEC_SPITZER,2) <= pow(2/3600,2)
 
# Close connection to the database

#s_count_mean=numpy.mean(s_count)
print "Mean Source Count with in radius: ",s_count

db.close()
         

