#===========================================================================
#
# q_0.py
#
# Python script to query mysql database to determine the
# Q0
#
#===========================================================================
#
# S. Weston
# AUT University
# May 2014
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
import random

from astropysics.constants import c,G

global Q
print "\nStarting q0 calculation"

execfile('constants.py')
	
sigma_foreground=2.4

for loop1 in range (0,30):

#    execfile('get_sigma_foreground.py')
	
#    print "simga_foreground :",sigma_foreground
#    print "\n"
    b=1/(2*(sigma_foreground**2))
#    print "b           :",b

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

    sql1=("SELECT radius,nr_random,nr_real, "
      " (1-(nr_random/(select count(*) from nvss_gama12.nvss_gama12))), "
      " (1-(nr_real/(select count(*) from nvss_gama12.nvss_gama12))), "
      " (1-(nr_real/(select count(*) from nvss_gama12.nvss_gama12)))/(1-(nr_random/(select count(*) from nvss_gama12.nvss_gama12))) "
      " FROM "+schema+"."+schema+"_q0 ")

#    print sql1,"\n"
    db.query(sql1)

    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=40)

# Close connection to the database

    db.close()

    x=numpy.empty([40],dtype=float)
    y=numpy.empty([40],dtype=float)

    i=0
    for row in rows:
#        print row
        radius=float(row[0])
        real_random=float(row[5])
#        print radius,real_random
        x[i]=radius
        y[i]=real_random
        i=i+1


    def func(x,a):
        return 1-a+a*numpy.exp(-b*x**2)

    popt,pcov=curve_fit(func,x,y)

#    print "a = %s " % (popt[0])
	
    perr = numpy.sqrt(numpy.diag(pcov))
#    print "Sigma : %s Q0 : %s    perr +- %s " % (sigma_foreground,popt[0],perr[0])
    print " %s %s %s " % (sigma_foreground,popt[0],perr[0])

#    xx=numpy.linspace(1.0,40.0,num=100)
#    yy=func(xx,*popt)
	
    q0=float(popt[0])
    xx=[None]*400
    yy=[None]*400
    for j in range(10,400,1):
        x1=float(j)/10
        y1=1-q0+q0*numpy.exp(-b*x1**2)
#        print x1,y1
        xx[j]=x1
        yy[j]=y1

#plot_title=field+" Q0 = %s " % (popt[0])
#    plot_title=field+" y = %s * x ** (- r^2/2 Simga^2) " % (popt[0])
#    plot_title="NVSS GAMMA12"
#    plt.title(plot_title)
    plt.xlabel('Radius (arcsec)')
    plt.ylabel('Real/Random Normalised')
    plt.plot(x,y,'ro',label="Original Data")
    plt.plot(xx,yy,label="Fitted Curve")
    plt.axis([0,40,0,1])
#    plt.legend(loc='upper right')
#    No grid for publication
#    plt.grid()
#output_dir='I:/PhD 2012/Marsfield April 2014/'
    output_dir='D:/temp/'
    filename='nvss_q0.eps'
    fullname=output_dir+str(sigma_foreground)+filename
    plt.savefig(fullname,format="eps")
#    plt.show()
 
#    print "Q0                      : %f" % popt[0]
    Q=popt[0]

# Connect to the local database with the atlas uid

#    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
	
# Put Q0 into the working table, so don't have to re-run this each time

#    db.query("update gama12.gama12_working set q0=%s \
#	          where field like '%s';" % (Q,schema))
#    db.close()
    sigma_foreground += 0.1
	

print "End or q_0\n"





