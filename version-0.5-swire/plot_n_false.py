#===========================================================================
#
# plot_n_false.py
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

print "\nStarting Plot N(false) vs Reliability"

n_false=[]
rel=[]
avg_rel=[]
field=answer

for inc in range(1,100):
    print inc,"\n"
    reliability=str(float(inc)/100)
    print reliability,"\n"
    llim_rel=str(float(inc)/100 - 0.005)
    ulim_rel=str(float(inc)/100 + 0.005)

    print llim_rel,ulim_rel,"\n"
    
# select from matches the sum of 1-Ri
#   Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)       
#    sql1=("SELECT sum(1-reliability),avg(reliability) FROM atlas_dr3."+field+"_matches where reliability >="+reliability+";")
    sql1=("SELECT count(reliability),avg(reliability) FROM atlas_dr3."+field+"_matches where reliability > "+llim_rel+" and reliability < "+ulim_rel+";")
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
        
        n_false.append(float(row[0]))
#        avg_rel.append(float(row[1]))
        rel.append(float(reliability))
        print reliability," ",row[0]," ",row[1],"\n"
	
#    End of do block

# Close connection to the database
    db.close()

# Now plot the data


plt.plot(rel,n_false,'k.')
plot_title=field+'  N(false) vs Reliability' 
plt.title(plot_title)
plt.ylabel('N(false)')
plt.xlabel('Reliability')
plt.xlim(0.0,1.0)
#plt.ylim(0.0,200)
#plt.legend(["Total(m)","Real(m)","n(m) - Background"])
plot_fname='atlas_'+field+'_n_false_vs_reliability.eps' 
fname=output_dir + plot_fname
plt.savefig(fname,format="eps")
plt.show()

plt.plot(rel,avg_rel,'k.')
plot_title=field+'  Avg(Rel) vs Reliability' 
plt.title(plot_title)
plt.ylabel('Avg(Rel)')
plt.xlabel('Reliability')
plt.xlim(0.0,1.0)
#plt.ylim(0.9,1.0)
#plt.minorticks_on()
plt.grid(b=True,which='major',color='b',linestyle=':')
#plt.grid(b=True,which='minor',color='r',linestyle='--')
#plt.legend(["Total(m)","Real(m)","n(m) - Background"])
plot_fname='atlas_'+field+'_avg_rel_vs_rel.eps' 
fname=output_dir + plot_fname
plt.savefig(fname,format="eps")
plt.show()
	
