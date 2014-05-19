import math
import array
import _mysql
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import astropysics as astro
import pylab
import sys

# ask which field to process
answer=raw_input('Which field cdfs/elais ?')
print "\nentered : ",answer,"\n"

if answer == 'cdfs':
   schema='atlas_dr3' 
   field='cdfs'
   swire_schema='swire_cdfs'
   beam_y=16.8
   beam_x=6.9
else:
   schema='atlas_dr3' 
   field='elais'
   swire_schema='swire_es1'
   beam_y=12.2
   beam_x=7.6
   
# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

sql1=("SELECT radius,nr_random,nr_real, "
      " (1-(nr_random/(select count(*) from atlas_dr3."+field+"_coords))), "
      " (1-(nr_real/(select count(*) from atlas_dr3."+field+"_coords))), "
      " (1-(nr_real/(select count(*) from atlas_dr3."+field+"_coords)))/(1-(nr_random/(select count(*) from atlas_dr3."+field+"_coords))) "
      " FROM atlas_dr3."+field+"_q0 ")

print sql1,"\n"
db.query(sql1)

r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=10)

# Close connection to the database

db.close()

x=np.empty([10],dtype=float)
y=np.empty([10],dtype=float)

i=0
for row in rows:
    print row
    radius=float(row[0])
    real_random=float(row[5])
    print radius,real_random
    x[i]=radius
    y[i]=real_random
    i=i+1

#def func(x,a,b):
#    return 1-a+a*np.exp(-b*x**2)

def func(x,a,b):
    return a*x**b

popt,pcov=curve_fit(func,x,y)

print "a = %s , b = %s" % (popt[0], popt[1])

xx=np.linspace(1.0,10.0,num=100)
yy=func(xx,*popt)

#plot_title=field+" Q0 = %s " % (popt[0])
plot_title=field+" y = %s * x ** (%s)" % (popt[0], popt[1])
plt.title(plot_title)
plt.xlabel('Radius (arcsec)')
plt.ylabel('Real/Random Normalised')
plt.plot(x,y,'ro',label="Original Data")
plt.plot(xx,yy,label="Fitted Curve")
plt.axis([0,11,0,1])
plt.legend(loc='upper right')
plt.grid()
#output_dir='I:/PhD 2012/Marsfield April 2014/'
output_dir='D:/temp/'
filename=field+'_q0.ps'
fullname=output_dir+filename
plt.savefig(fullname)
plt.show()
