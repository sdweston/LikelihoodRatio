#===========================================================================
#
# plot_rel_bins.py
#
# Python script to query SWIRE_ES1 mysql database to determine the
# LR the likelihood ratio.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

import numpy
import pylab
import _mysql

# Database 
global db_host
db_host='localhost'
global db_user
db_user='atlas'
global db_passwd
db_passwd='atlas'

# ask which field to process
answer=raw_input('Which field cdfs/elais ?')
print "\nentered : ",answer,"\n"

schema='atlas_dr3' 
if answer == 'cdfs':
   field='cdfs'
   range_min=0.0
   range_max=1000.0
else:
   field='elais'
   range_min=0.0
   range_max=100.0

# Location to put plot files etc
global output_dir
output_dir='d:/temp/'

#   Connect to the local database with the atlas uid

db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from matches the sum of L_i grouped by radio source

db.query("select lr,reliability from "+schema+"."+field+"_matches where reliability > 0.0 and reliability < 1.0;" )
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...

r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

LR=[]
REL=[]
  
for row in rows:
        
    LR.append(float(row[0]))
    REL.append(float(row[1]))
 	
#    End of do block

# Close connection to the database
db.close()

# Bin Reliability and plot	
# Smith et al 2011 Figure 4

(hist,bins)=numpy.histogram(REL,bins=20,range=[0.0,1.0])
print bins,'\n'
print hist,'\n'
width = 1.0*(bins[1]-bins[0])
#    center = (bins[:-1]+bins[1:])/2
center = 0.5*(bins[1:]+bins[:-1])

plot_title='ATLAS ' +field+ ' Histogram of the Reliability values'
#pylab.title(plot_title)
pylab.yscale('log')
pylab.grid(True)
pylab.ylabel('N(counterparts)')
pylab.xlabel('Reliability')

pylab.plot(center, hist,drawstyle='steps')

common_params = dict(bins=20,
                range=(0,1))
common_params['histtype'] = 'step'
#pylab.hist(REL,**common_params)

pylab.ylim(0.9999)
pylab.show()

# Bin LR and plot

(hist,bins)=numpy.histogram(LR,bins=100,range=[range_min,range_max])
width = 1.0*(bins[1]-bins[0])
center = 0.5*(bins[:-1]+bins[1:])
print 'bins : ',bins,'\n'
print 'hist : ',hist,'\n'

x=[]
y=[]
i=0
for item in hist:
   if i== 0:
      x.append(0)
   else:
      x.append(bins[i]-0.5*width)
      
   y.append(hist[i])
   x.append(bins[i]+0.5*width)
   y.append(hist[i])
   i=i+1

i=0
f=open('d:\\temp\\n_vs_lr.csv','w')
for item in x:
    f.write('%d , %d \n' % (x[i], y[i]))
    i=i+1
f.close()

pylab.yscale('log')
pylab.xscale('log')
pylab.ylabel('N(counterparts)')
pylab.xlabel('Likelihood Ratio')
#pylab.plot(center, hist,drawstyle='steps')
pylab.plot(x, y,drawstyle='steps')
pylab.ylim(0.9999)
pylab.xlim(0.0)
pylab.grid(True)
pylab.show()


print "End Plotting\n"


