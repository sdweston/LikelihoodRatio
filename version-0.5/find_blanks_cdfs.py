# randomcats.py
# This program makes a random catalogue based on the FUSION catalogue

import sys
import math
import array
import random
import _mysql
import numpy
import matplotlib.pyplot as plt
import astropysics as astro
import pylab as p

from astropysics.constants import c,G

schema="atlas_dr3"
field="elais"
swire_schema='swire_es1'
sr=15.0

#===================================================================================================
#

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

db.query("select count(*),max(ra),min(ra),max(declination),min(declination) from atlas_dr3.elais_randomcat;")

r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=1)

for row in rows:
 
    ra_max=float(row[1])
    ra_min=float(row[2])
    dec_min=float(row[3])
    dec_max=float(row[4])

print "RA Max, RA Min    : %f %f" % (ra_max,ra_min)
print "Dec Max, Dec Min  : %f %f" % (dec_max,dec_min)

# Close connection to the database
db.close()

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry, find the number of records

db.query("select ra,declination from atlas_dr3.elais_randomcat;")

r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=0)

n_blanks=0

# Close connection to the database
db.close()
db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

f_radius=[]

for row in rows:
    ra=float(row[0])
    dec=float(row[1])

    ra_min=float(ra)-float(sr/3600)
    ra_max=float(ra)+float(sr/3600)
    dec_min=float(dec)-float(sr/3600)
    dec_max=float(dec)+float(sr/3600)
    
# print the paramaters

#    print "Ra Dec  : %f %f" % (ra,dec)

    sql=("select "
         "t2.Index_Spitzer, "
         "sqrt(pow(("+str(ra)+"-t2.RA_SPITZER)*cos("+str(dec)+"),2)+"
         "     pow("+str(dec)+"-t2.DEC_SPITZER,2))*3600 as radius "
	 "from "+swire_schema+".swire as t2 "
         "where pow(("+str(ra)+"-t2.RA_SPITZER)*cos("+str(dec)+"),2)+" 
         "      pow("+str(dec)+"-t2.DEC_SPITZER,2) <= pow("+str(sr)+"/3600,2) "
         " and   t2.ra_spitzer > "+str(ra_min)+" and t2.ra_spitzer < "+str(ra_max)+" "
         " and   t2.dec_spitzer > "+str(dec_min)+" and t2.dec_spitzer < "+str(dec_max)+
         " order by radius asc limit 0,3000000; ")

#    print sql
    db.query(sql)
    r=db.use_result()
    count=r.fetch_row(maxrows=0)

    nm=0
    for c in count:
        nm=nm+1
        radius=float(c[1])
        f_radius.append(radius)
        sys.stdout.write('.')
#        print c
        if nm==1: break
        

#    print nm

    if nm==0:
        n_blanks=n_blanks+1

# Close connection to the database

db.close()
        
print "number of blanks :",n_blanks

(hist,bins)=numpy.histogram(f_radius,bins=15,range=[0.0,15.0])
width = 0.7*(bins[1]-bins[0])
center = (bins[:-1]+bins[1:])/2

f=open('Blanks_'+field+'.csv','w')
for x in xrange(1,15):
    out_str="hist[%d] : %d \n" % (x,hist[x])
    f.write(out_str)
    
# Need a cumulative histogram

for x in xrange(2,15):
    hist[x]=hist[x]+hist[x-1]

plt.bar(center, hist, align = 'center',width = width,linewidth=0)
#plt.hist(hist, bins=15, cumulative=True)
plot_title=' Finding Blanks m(>r)'
plt.title(plot_title)
plt.ylabel('m(>r)')
plt.xlabel('radius (arcsec)')
plot_fname='atlas_'+field+'_blanks_n_r.ps'
output_dir='D:/temp/'
fname=output_dir + plot_fname
plt.savefig(fname)
plt.show()

# Print out the histogram values
# 

#f=open('random_cats_cdfs.csv','w')
f.write('====Cumulative Histogram====\n')
for x in xrange(1,15):
    out_str="hist[%d] : %d \n" % (x,hist[x])
    f.write(out_str)
f.close()



         

