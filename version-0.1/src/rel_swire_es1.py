#===========================================================================
#
# lr_swire_es1.py
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

import array
import pylab
import _mysql
import numpy
import math
import sys
import matplotlib.pyplot as plt

print "Starting LR calculations and db updates"

execfile('constants.py')

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# select from matches the sum of L_i grouped by radio source

db.query("select elais_s1_cid,sum(lr) \
          from elais_s1.matches \
		  where lr is not null \
		  group by elais_s1_cid;")
          
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
#    print row
    cid=row[0]
    sum_lr=float(row[1])
    
# now select each row from matches for each radio source where the flux is not null

    db.query("select swire_es1_index_spitzer,lr \
              from elais_s1.matches \
	      where lr is not null \
	      and elais_s1_cid like '%s';" % cid)

    r2=db.store_result()
    strings=r2.fetch_row(maxrows=1000)

    for string in strings:
#        print string
        index_spitzer=(string[0])
        lr=float(string[1])   
		
#       and calculate the reliability

        rel= lr / (sum_lr + (1-Q))
        LR.append(lr)
        REL.append(rel)
#        print 'Reliability : %f ' % rel
	
#       Now update the matches table with the reliability

#        db.query("update elais_s1.matches set reliability=%s where elais_s1_cid='%s' \
#                  and swire_es1_index_spitzer='%s';" % (rel, cid, index_spitzer))
	
# End of do block

# Close connection to the database
db.close()

plt.xscale('log')
plt.plot(LR, REL,'k.')
plt.title(' ATLAS/ELAIS_S1     Reliability vs Likelihood Ratio')
plt.ylabel('Reliability')
plt.xlabel('Likelihood Ratio')
plt.savefig("atlas-elasis_s1_rel_vs_lr.ps")
plt.show()

print "End"


