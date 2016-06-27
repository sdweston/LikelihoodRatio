# randomcats.py
# This program makes a random catalogue based on the FUSION catalogue
# Based on method Bonzini et al 2012

import sys
import math
import array
import random
import _mysql
import numpy
import matplotlib.pyplot as plt
import pylab as p

schema="atlas_dr3"
field="cdfs"
swire_schema='cdfs'
sr=10.0
#n_radio=3078
n_radio=2983

global dradian
dradian=math.pi/180

#===================================================================================================
#

print sys.argv[0],"\n"

db=_mysql.connect(host="localhost",user="root",passwd="root")

db.query("select count(*),max(ra),min(ra),max(decl),min(decl) from atlas_dr3.cdfs_coords;")

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

db=_mysql.connect(host="localhost",user="root",passwd="root")

# Lets run a querry, find the number of records

db.query("select ra,decl from atlas_dr3.cdfs_coords ;")

r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=0)

n_blanks=0

# Close connection to the database
db.close()
db=_mysql.connect(host="localhost",user="root",passwd="root")

f_radius=[]
c_radius=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

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
         "sqrt(pow(("+str(ra)+"-t2.RA_SPITZER)*cos(radians("+str(dec)+")),2)+"
         "     pow("+str(dec)+"-t2.DEC_SPITZER,2))*3600 as radius "
	 	 "from fusion.swire_"+swire_schema+" as t2 "
         "where pow(("+str(ra)+"-t2.RA_SPITZER)*cos(radians("+str(dec)+")),2)+" 
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

# Not very elegent but need to count number
# Need to count number of values in array between certain values

        if radius < 0.5:
            c_radius[1]=c_radius[1]+1
        elif radius > 0.5 and radius < 1.0:
            c_radius[2]=c_radius[2]+1
        elif radius > 1.0 and radius < 1.5:
            c_radius[3]=c_radius[3]+1
        elif radius > 1.5 and radius < 2.0:
            c_radius[4]=c_radius[4]+1
        elif radius > 2.0 and radius < 2.5:
            c_radius[5]=c_radius[5]+1
        elif radius > 2.5 and radius < 3.0:
            c_radius[6]=c_radius[6]+1
        elif radius > 3.0 and radius < 3.5:
            c_radius[7]=c_radius[7]+1
        elif radius > 3.5 and radius < 4.0:
            c_radius[8]=c_radius[8]+1
        elif radius > 4.0 and radius < 4.5:
            c_radius[9]=c_radius[9]+1
        elif radius > 4.5 and radius < 5.0:
            c_radius[10]=c_radius[10]+1
        elif radius > 5.0 and radius < 5.5:
            c_radius[11]=c_radius[11]+1
        elif radius > 5.5 and radius < 6.0:
            c_radius[12]=c_radius[12]+1
        elif radius > 6.0 and radius < 6.5:
            c_radius[13]=c_radius[13]+1
        elif radius > 6.5 and radius < 7.0:
            c_radius[14]=c_radius[14]+1
        elif radius > 7.0 and radius < 7.5:
            c_radius[15]=c_radius[15]+1
        elif radius > 7.5 and radius < 8.0:
            c_radius[16]=c_radius[16]+1
        elif radius > 8.0 and radius < 8.5:
            c_radius[17]=c_radius[17]+1
        elif radius > 8.5 and radius < 9.0:
            c_radius[18]=c_radius[18]+1
        elif radius > 9.0 and radius < 9.5:
            c_radius[19]=c_radius[19]+1
        elif radius > 9.5 and radius < 10.0:
            c_radius[20]=c_radius[20]+1

            
        sys.stdout.write('.')
#        print c
        if nm==1: break
        

#    print nm

    if nm==0:
        n_blanks=n_blanks+1

print "number of blanks :",n_blanks

print "c_radius : ",c_radius

# We want double the number of bins
# sr=10.0 but we want 20 bins not 10, we are using integers ...
#(hist,bins)=numpy.histogram(f_radius,bins=int(2*sr),range=[0.0,sr])
#width = 0.8*(bins[1]-bins[0])
#center = (bins[:-1]+bins[1:])/2

for x in xrange(1,21):
    c_radius[x]=c_radius[x]+c_radius[x-1]

print "c_radius : ",c_radius

n_real=[]
n_blank=[]

f=open('Blanks_'+field+'_real.csv','w')
for x in xrange(1,21):
    sql3=("update atlas_dr3.cdfs_q0 set nb_real="+str(n_radio-c_radius[x])+" where radius="+str(float(x)/2)+";")
    print sql3,"\n"
    db.query(sql3)
    db.commit()
    n_blank.append(n_radio-c_radius[x])

# Need a cumulative histogram

for x in xrange(1,21):
    sql4=("update atlas_dr3.cdfs_q0 set nr_real="+str(c_radius[x])+" where radius="+str(float(x)/2)+";")
    print sql4,"\n"
    db.query(sql4)
    db.commit()
    n_real.append(c_radius[x])

# Close connection to the database

db.close()

quit()

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



