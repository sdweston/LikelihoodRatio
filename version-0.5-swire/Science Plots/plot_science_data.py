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

#   Connect to the local database with the atlas uid

db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# select from matches the IR Flux, Radio Flux, Redshift etc so we can do some science

db.query("SELECT t1.swire_index_spitzer, t1.cid,  \
                     t2.irac_3_6_micron_flux_mujy, \
                     t2.irac_4_5_micron_flux_mujy, \
                     t2.irac_5_8_micron_flux_mujy, \
                     t2.irac_8_0_micron_flux_mujy, \
                     t3.sp, \
                     t3.sint, \
	             t2.redshift \
              from elais_s1.matches t1, swire_es1.swire t2, elais_s1.table4 t3 \
              where t1.swire_index_spitzer=t2.index_spitzer \
              and t1.cid=t3.cid \
              and t2.irac_5_8_micron_flux_mujy > 0.0 \
              and t1.reliability > 0.8;")
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=50000)

# rows is a tuple, convert it to a list

ir_3_6_flux_mujy=[]
ir_4_5_flux_mujy=[]
ir_5_8_flux_mujy=[]
ir_8_0_flux_mujy=[]
r_sp_1_4_flux_mjy=[]
r_sint_1_4_flux_mjy=[]
redshift=[]

# We need :
# 	4.5 - 8.0
S45_S80=[]
S36_S58=[]
S36_S45=[]
S58_S80=[]
S36_S80=[]
S36_S45=[]	
i1_i2=[]
i3_i4=[]

r_sint_mujy=[]

for row in rows:

    ir_3_6_flux_mujy.append(float(row[2]))
    ir_4_5_flux_mujy.append(float(row[3]))
    ir_5_8_flux_mujy.append(float(row[4]))
    ir_8_0_flux_mujy.append(float(row[5]))
    r_sp_1_4_flux_mjy.append(float(row[6]))
    r_sint_1_4_flux_mjy.append(float(row[7]))
    redshift.append(float(row[8]))
	
    i1_i2.append(float(row[5])/float(row[3]))
    i3_i4.append(float(row[4])/float(row[2]))

    S45_S80.append(float(row[3])-float(row[5]))
    S36_S58.append(float(row[2])-float(row[4]))

    S36_S45.append(float(row[2])-float(row[3]))
    S58_S80.append(float(row[4])-float(row[5]))

    S36_S80.append(float(row[2])-float(row[5]))
    S36_S45.append(float(row[2])-float(row[3]))

    r_sint_mujy.append(float(row[7])*1000)
	
	        	
#    End of do block

# Close connection to the database
db.close()

# Now plot the data

# Colour - Colour Plots IR

plt.yscale('log')
plt.xscale('log')
plt.scatter(S36_S58,S45_S80)
#plt.title(field)
plt.grid(True)
#plt.xlim(0.0)
#plt.ylim(0.0)
plt.ylabel('[S_4.5]-[S_8.0]')
plt.xlabel('[S_3.6]-[S_5.8]')
plt.show()

plt.yscale('log')
plt.xscale('log')
plt.plot(i1_i2, i3_i4,'k.')
#plot_title=field+'  ir_8p0/ir_4p5 vs ir_5p8/ir_3p6'
plt.title(' Colour Index ir_8p0/ir_4p5 vs ir_5p8/ir_3p6')
plt.ylabel('ir_8p0/ir_4p5')
plt.xlabel('ir_5p8/ir_3p6')
#    plot_fname='atlas_'+field+'_magnitude_dependance.ps'
#    fname=output_dir + plot_fname
#    plt.savefig(fname)
plt.show()

plt.yscale('log')
plt.xscale('log')
plt.plot(i1_i2,r_sint_mujy,'k.',i3_i4,r_sint_mujy,'g+')
#plot_title=field+'  ir_3_6/ir_4_5 muJy vs Flux 1.4 muJy'
plt.title(' Colour Index ir_3_6/ir_4_5 vs Flux 1.4')
plt.xlabel('ir_3_6/ir_4_5 muJy')
plt.ylabel('Flux 1.4 muJy')
#    plot_fname='atlas_'+field+'_magnitude_dependance.ps'
#    fname=output_dir + plot_fname
#    plt.savefig(fname)
plt.show()
1
print "End Plotting\n"


