import math
import array
import _mysql
import numpy 
import scipy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pylab
import sys


print "\nStarting q0 calculation"

# ask which field to process
answer=raw_input('Which field cdfs/elais ?')
print "\nentered : ",answer,"\n"

if answer == 'elais':
   field='ELAIS'
else:
   field='CDFS'

   # Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="root",passwd="root")

# First truncate the table
sql1=("truncate table atlas_dr3."+field+"_q0 ; ")

print sql1,"\n"
db.query(sql1)

# OK now inser new radius values:

radius=0.5
for x in xrange(1,21):
    print "New value : ",radius
    sql3=("insert into atlas_dr3."+field+"_q0 (radius) values ("+str(radius)+") ;")
    print sql3,"\n"
    db.query(sql3)
    db.commit()
    radius=radius+0.5

# Close connection to the database

db.close()
