#===========================================================================
#
# plot_n_false_1.py
#
# Python script to query SWIRE_ES1 mysql database to plot the false_id's
# vs R
# See Smith et al 2011, Eq 12
#     Flueren at al 2012, Eq 14
#
#===========================================================================
#
# S. Weston
# AUT University
# Oct 2014
#===========================================================================
import math
import array
import _mysql
import numpy
import scipy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#import astropysics as astro
import pylab
import sys

# Database 
global db_host
db_host='localhost'
global db_user
db_user='root'
global db_passwd
db_passwd='root'

# Location to put plot files etc
global output_dir
output_dir='d:/temp/'

# ask which field to process
#answer=raw_input('Which field cdfs/elais ?')
#print "\nentered : ",answer,"\n"

print "\nStarting Plot N(false) vs rel_1iability"

completeness_1=[]
rel_1=[]
completeness_2=[]
rel_2=[]

#field=answer

def my_range(start,end,step):
    while start<=end:
        yield start
        start += step
        
for inc in my_range(0.01,10,0.01):
#    print inc,"\n"
    reliability=str(float(inc)/10)
    
# select from matches the sum of 1-Ri
#   Connect to the local database with the atlas uid
# Take the count from matches !

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)       
#    sql1=("SELECT (count(reliability)/4725),"+reliability+" FROM atlas_dr3.cdfs_matches where reliability >="+reliability+";")
    sql1=("select count(rel)/3078,"+reliability+" from (select max(reliability) as rel from atlas_dr3.cdfs_matches "
          "where reliability >= "+reliability+"group by cid limit 10000 ) as subquery; ")

    db.query(sql1)
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=1)

# rows is a tuple, convert it to a list

    for row in rows:
#        if inc==1:
#           n_false_1.append(float(row[0]))
#           rel_1.append(0.0)
            
        completeness_1.append(float(row[0]))
        rel_1.append(float(row[1]))

#    End of do block

# Close connection to the database
    db.close()

#print completeness_1,"\n"
#print rel_1,"\n"

for inc in my_range(0.01,10,0.01):
#    print inc,"\n"
    reliability=str(float(inc)/10)
    
# select from matches the sum of 1-Ri
#   Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)       
    sql1=("select count(rel)/2113,"+reliability+" from (select max(reliability) as rel from atlas_dr3.elais_matches "
          "where reliability >= "+reliability+"group by cid limit 10000 ) as subquery; ")

    db.query(sql1)
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=1)

# rows is a tuple, convert it to a list

    for row in rows:
           
        completeness_2.append(float(row[0]))
        rel_2.append(float(row[1]))

#    End of do block

# Close connection to the database
    db.close()


# Now plot the data

# Or dump the data out to use a different plotting tool !

plt.plot(rel_1,completeness_1)
plt.plot(rel_2,completeness_2)
plot_title='  Completeness vs Reliability' 
#plt.title(plot_title)
plt.ylabel('Completeness %')
plt.xlabel('Reliability')
plt.xlim(0.00,1.0)
#plt.yscale('log')
plt.ylim(0.0,1.0)
plt.legend(["CDFS","ELAIS"])
plot_fname='atlas_n_completeness_vs_reliability.eps' 
fname=output_dir + plot_fname
plt.savefig(fname,format="eps")
plt.show()


	
