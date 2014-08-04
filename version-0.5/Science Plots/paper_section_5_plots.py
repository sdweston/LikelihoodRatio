#===========================================================================
#
# plot_science.py
#
# Python script to query SWIRE_ES1 mysql database to 
# select from matches the IR Flux, Radio Flux, Redshift etc so we can do some science
# Plot the colour colour 
# Plot the colour magnitude
#
#===========================================================================
#
# S. Weston
# AUT University
# Nov 2013
#===========================================================================

import math
import array
import _mysql
import numpy
import scipy
import matplotlib.pyplot as plt
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

print "\nStarting Plot Science"

# ask which field to process
answer=raw_input('Which field cdfs/elais ?')
print "\nentered : ",answer,"\n"

if answer == 'cdfs':
   schema='atlas_dr3' 
   field='cdfs'
   swire_schema='swire_cdfs'
else:
   schema='atlas_dr3' 
   field='elais'
   swire_schema='swire_es1'

# We need two plots:
#
#  Plot 1 - IR_Flux_3_6 / Flux_Radio, binned by number
#
#  Plot 2 - Flux_Radio by Z
#
#  Possibly IR colour colour plots
#
# NOTE: IR flux is uJy and Radio is mJy. Need to be same units, make all mJy.

# select from matches the IR Flux, Radio Flux, Redshift etc so we can do some science

# First get the reliable matches, where Rel > 0.8

#   Connect to the local database with the atlas uid

db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

sql1=("SELECT t1.swire_index_spitzer, t1.cid,  "
      "       (t2.flux_ap2_36/1000)/t3.sp, "
      "       (t2.flux_ap2_80/1000)/t3.sp, "
      "       t2.flux_ap2_36/t2.flux_ap2_45, "
      "       t2.flux_ap2_36,t2.flux_ap2_45,t2.flux_ap2_58,t2.flux_ap2_80  "
      "from "+schema+"."+field+"_matches t1, fusion."+field+" t2, "+schema+"."+field+"_radio_properties t3 "
      "     where t1.swire_index_spitzer=t2.id_12 "
      "     and t1.cid=t3.id  "
      "     and t2.flux_ap2_36 is not null "
      "     and t2.flux_ap2_45 is not null "
      "     and t2.flux_ap2_58 is not null "
      "     and t2.flux_ap2_80 is not null "
      "     and t3.sp > 0.0 "
      "     and t1.reliability > 0.8;")

print sql1,"\n"
db.query(sql1)
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

IR_36_45_rel=[]
IR_36_58_rel=[]
IR_80_45_rel=[]
IR_80_58_rel=[]
IR36_Radio_Sp_rel=[]
IR80_Radio_Sp_rel=[]

for row in rows:
#    print row
    IR36_Radio_Sp_rel.append(float(row[2]))
    IR80_Radio_Sp_rel.append(float(row[3]))
    IR_36_45_rel.append(float(row[4]))
    IR_36_58_rel.append(float(row[5])/float(row[7]))
    IR_80_45_rel.append(float(row[8])/float(row[6]))
    IR_80_58_rel.append(float(row[8])/float(row[7]))
	        	
#    End of do block

# Close connection to the database
db.close()

# Now get the un-reliable matches, where Rel < 0.8

#   Connect to the local database with the atlas uid

db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

sql2=("SELECT t1.swire_index_spitzer, t1.cid,  "
      "       (t2.flux_ap2_36/1000)/t3.sp, "
      "       t2.flux_ap2_36/t2.flux_ap2_45, "
      "       (t2.flux_ap2_36/1000)/t3.sint "
      "from "+schema+"."+field+"_matches t1, fusion."+field+" t2, "+schema+"."+field+"_radio_properties t3 "
      "     where t1.swire_index_spitzer=t2.id_12 "
      "     and t1.cid=t3.id  "
      "     and t2.flux_ap2_36 is not null "
      "     and t2.flux_ap2_45 is not null "
      "     and t2.flux_ap2_58 is not null "
      "     and t2.flux_ap2_80 is not null "
      "    and t1.reliability < 0.8;")

print sql2,"\n"
db.query(sql2)

# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

IR36_Radio_Sp_unrel=[]
IR_36_45_unrel=[]

for row in rows:
       
    IR36_Radio_Sp_unrel.append(float(row[2]))
    IR_36_45_unrel.append(float(row[3]))
	        	
#    End of do block

# Close connection to the database
db.close()

# Now Bin the data !



# Plot the binned data.


# Now plot the data

plt.hist(IR_36_45_rel,bins=20,histtype='step',color='blue')
plt.hist(IR_36_45_unrel,bins=20,histtype='step',color='red')

plt.title(field)
plt.ylabel('N')
plt.xlabel('S_3.6 / S_4.5')
plt.show()

(hist,bins)=numpy.histogram(IR36_Radio_Sp_rel,bins=40)
plt.hist(IR36_Radio_Sp_rel,bins=bins,histtype='step',color='blue')
plt.hist(IR36_Radio_Sp_unrel,bins=bins,histtype='step',color='red')

#plt.yscale('log')
plt.title(field)
plt.grid(True)
plt.ylabel('N')
plt.xlabel('S_3.6 / S_Radio')
plt.show()

# Lets do colour colour IR to Radio
# S_36/S_Radio vs S_80/S_Radio

# Select required columns as some have null ! Select pairs where one is not null

plt.scatter(IR36_Radio_Sp_rel,IR80_Radio_Sp_rel)
plt.title(field)
plt.grid(True)
plt.xlim(0.0)
plt.ylim(0.0)
plt.ylabel('S_8.0 / S_Radio')
plt.xlabel('S_3.6 / S_Radio')
plt.show()

plt.scatter(IR_36_58_rel,IR_80_58_rel)
plt.title(field)
plt.grid(True)
plt.xlim(0.0)
plt.ylim(0.0)
plt.ylabel('S_8.0 / S_5.8')
plt.xlabel('S_3.6 / S_5.8')
plt.show()

plt.scatter(IR_36_45_rel,IR_80_45_rel)
plt.title(field)
plt.grid(True)
plt.xlim(0.0)
plt.ylim(0.0)
plt.ylabel('S_8.0 / S_4.5')
plt.xlabel('S_3.6 / S_4.5')
plt.show()





