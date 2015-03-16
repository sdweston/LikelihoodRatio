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
import astropysics as astro
import pylab
import sys

# Database 
global db_host
db_host='localhost'
global db_user
db_user='atlas'
global db_passwd
db_passwd='atlas'

# Location to put plot files etc
global output_dir
output_dir='d:/temp/'

# ask which field to process
answer=raw_input('Which field cdfs/elais ?')
print "\nentered : ",answer,"\n"

print "\nStarting Plot N(false) vs rel_1iability"

n_false_1=[]
rel_1=[]
n_false_2=[]
rel_2=[]
field=answer

for inc in range(1,10):
    print inc,"\n"
    reliability=str(float(inc)/10)
    print reliability,"\n"
    llim_rel_1=str(float(inc)/10 - 0.5)
    ulim_rel_1=str(float(inc)/10 + 0.5)

#    print llim_rel_1,ulim_rel_1,"\n"
    
# select from matches the sum of 1-Ri
#   Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)       
    sql1=("SELECT sum(1-reliability),"+reliability+" FROM atlas_dr3.cdfs_matches where reliability >="+reliability+";")
#    sql1=("SELECT count(rel_1iability),avg(rel_1iability) FROM atlas_dr3."+field+ \
#          "_matches where rel_1iability > "+llim_rel_1+" and rel_1iability < "+ulim_rel_1+";")
    print sql1,"\n"
    db.query(sql1)
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=1)

# rows is a tuple, convert it to a list

    for row in rows:
        if inc==1:
           n_false_1.append(float(row[0]))
           rel_1.append(0.0)
            
        n_false_1.append(float(row[0]))
        rel_1.append(float(row[1]))
        print inc," ",row[0]," ",row[1],"\n"

        if inc==9:
           n_false_1.append(float(row[0]))
           rel_1.append(1.0)

#    End of do block

# Close connection to the database
    db.close()

for inc in range(1,10):
    print inc,"\n"
    reliability=str(float(inc)/10)
    print reliability,"\n"
    llim_rel_1=str(float(inc)/10 - 0.5)
    ulim_rel_1=str(float(inc)/10 + 0.5)

#    print llim_rel_1,ulim_rel_1,"\n"
    
# select from matches the sum of 1-Ri
#   Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)       
    sql1=("SELECT sum(1-reliability),"+reliability+" FROM atlas_dr3.elais_matches where reliability >="+reliability+";")
#    sql1=("SELECT count(rel_1iability),avg(rel_1iability) FROM atlas_dr3."+field+ \
#          "_matches where rel_1iability > "+llim_rel_1+" and rel_1iability < "+ulim_rel_1+";")
    print sql1,"\n"
    db.query(sql1)
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=1)

# rows is a tuple, convert it to a list

    for row in rows:
        if inc==1:
           n_false_2.append(float(row[0]))
           rel_2.append(0.0)
            
        n_false_2.append(float(row[0]))
        rel_2.append(float(row[1]))
        print inc," ",row[0]," ",row[1],"\n"

        if inc==9:
           n_false_2.append(float(row[0]))
           rel_2.append(1.0)

#    End of do block

# Close connection to the database
    db.close()

print n_false_1,"\n"
print rel_1,"\n"

# Now plot the data

plt.plot(rel_1,n_false_1,'r^',markersize=5)
plt.plot(rel_2,n_false_2,'gv',markersize=5)
plot_title=field+'  N(false) vs reliability' 
#plt.title(plot_title)
plt.ylabel('N(false)')
plt.xlabel('reliability')
plt.xlim(0.05,0.95)
#plt.ylim(0.0,200)
#plt.legend(["Total(m)","Real(m)","n(m) - Background"])
plot_fname='atlas_n_false_vs_reliability.eps' 
fname=output_dir + plot_fname
plt.savefig(fname,format="eps")
plt.show()

# Plot as historgram
(hist,bins)=numpy.histogram(rel_1,bins=10,range=[0,1])
width=0.5*(bins[1]-bins[0])
center=(bins[:-1]+bins[1:])/2

#plt.bar(center, hist, align = 'center',width = width,linewidth=0)
plt.title(plot_title)
plt.ylabel('N(false)')
plt.xlabel('reliability')
plt.plot(rel_1,n_false_1,drawstyle='steps')
plt.xlim(0.1,0.9)
plot_fname='atlas_'+field+'_n_false_vs_reliability_historgram.eps' 
fname=output_dir + plot_fname
plt.savefig(fname,format="eps")
plt.show()
	
