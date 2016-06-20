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
   n_radio=2061
   lamda=0.004112
#   sigma=0.8568
   sigma=0.898
else:
   field='CDFS'
   n_radio=3078
   lamda=0.004274788
#   sigma=1.0678
   sigma=0.949


# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="root",passwd="root")

sql1=("SELECT radius,nb_real,nb_random "
      " from atlas_dr3."+field+"_q0 where radius < 8.0; ")

print sql1,"\n"
db.query(sql1)

r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=20)

# Close connection to the database

db.close()

x=numpy.empty([20],dtype=float)
y=numpy.empty([20],dtype=float)
t=numpy.empty([20],dtype=float)
r=numpy.empty([20],dtype=float)

i=0
print "Radius Real True"
for row in rows:
        print row
        radius=float(row[0])
        nb_real=float(row[1])/n_radio
        nb_random=float(row[2])/n_radio
        random=numpy.exp(-math.pi*radius*radius*lamda)
        x[i]=radius
        y[i]=nb_real
        r[i]=nb_random
        t[i]=y[i]/random
        print x[i],y[i],t[i]
        i=i+1

x1=numpy.linspace(0,10,100)
y1=numpy.exp(-math.pi*x1*x1*lamda)

#
# We need to fit a function to t[i] and x[i]
b=1/(2*sigma**2)
def func(x,a):
    return 1-a+a*numpy.exp(-b*x**2)

# allow x and sigma to be free for fit
#def func(x,a,s):
#    return 1-a+a*numpy.exp(-x**2/(2*s**2))

popt,pcov=curve_fit(func,x,t)
print "q0 = %s " % (popt)
perr = numpy.sqrt(numpy.diag(pcov))
print "perr +- %s " % pcov,perr
xx=numpy.linspace(0.0,6.0,num=100)
yy=func(xx,*popt)

#
# We want the residual between the True and Fit
#print "Radius True Fit Residual"
#for ix in xrange(1,13):
#        fit=1-popt+popt*numpy.exp(-b*(ix*0.5)**2)
#        print x[ix-1],t[ix-1],fit,fit-t[ix-1]
        

#plot_title=field+" Q0 = %s " % (popt[0])
#    plot_title=field+" y = %s * x ** (- r^2/2 Simga^2) " % (popt[0])
plot_title=field+" Q_0="+str(popt[0])+" Variance : "+str(pcov[0])
plt.figure(figsize=(12,9),dpi=100)
plt.title(plot_title)
plt.xlabel('Radius, (arcsec)',fontsize=30)
plt.ylabel('1-Q(r)',fontsize=30)
plt.tick_params(labelsize=20)
plt.plot(x,y,'r+',label="Real")
plt.plot(x,t,'ro',label="True")
plt.plot(x,r,'rx',label="Random")
plt.plot(x1,y1,label="Poisson")
plt.plot(xx,yy,label="Fitted Curve")
plt.axis([0,8.25,0,1])
#plt.legend(loc='upper right',fontsize=20)
plt.legend(loc='upper right')
#    No grid for publication
#plt.grid(b=True, which='major',color='b',linestyle='--')
#plt.grid(b=True, which='minor',axis='y',color='r',linestyle=':')
#plt.minorticks_on()
#output_dir='I:/PhD 2012/Marsfield April 2014/'
output_dir='M:/atlas-cross-identifications/section_3/Figures/'
filename=field+'_q0.pdf'
fullname=output_dir+filename
#plt.savefig(fullname,format="pdf")

plt.show()
