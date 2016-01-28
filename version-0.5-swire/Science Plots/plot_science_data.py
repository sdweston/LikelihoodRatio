#===========================================================================
#
# plot_science.py
#
# Python script to query mysql database to 
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
# First CDFS

db.query("SELECT t1.swire_index_spitzer, t1.cid,  \
                     t2.irac_3_6_micron_flux_mujy, \
                     t2.irac_4_5_micron_flux_mujy, \
                     t2.irac_5_8_micron_flux_mujy, \
                     t2.irac_8_0_micron_flux_mujy, \
                     t3.sp, \
                     t3.sint, \
	             t2.redshift \
              from atlas_dr3.cdfs_matches t1, fusion.swire_cdfs t2, atlas_dr3.cdfs_radio_properties t3 \
              where t1.swire_index_spitzer=t2.index_spitzer \
              and t1.cid=t3.id \
              and t2.irac_3_6_micron_flux_mujy > 0.0 \
	      and t2.irac_4_5_micron_flux_mujy > 0.0 \
	      and t2.irac_5_8_micron_flux_mujy > 0.0 \
	      and t2.irac_8_0_micron_flux_mujy > 0.0 \
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

r_sp_1_4_flux_mjy=[]
r_sint_1_4_flux_mjy=[]
redshift=[]

C_S45_S80=[]
C_S36_S58=[]
C_S36_S45=[]
C_S58_S80=[]
C_S36_S80=[]
C_S36_S45=[]	
flux_ratio=[]
r_sint_mujy=[]
rcount=1

for row in rows:


    r_sp_1_4_flux_mjy.append(float(row[6]))
    r_sint_1_4_flux_mjy.append(float(row[7]))
    redshift.append(float(row[8]))
#   For colour-colour plot we need magnitude
#   m1 - m2 = -2.5 log_10 (f1/f2)	
    C_S45_S80.append(-2.5 * math.log10(float(row[3])/float(row[5])))
    C_S36_S58.append(-2.5 * math.log10(float(row[2])/float(row[4])))

    C_S36_S45.append(-2.5 * math.log10(float(row[2])/float(row[3])))
    C_S58_S80.append(-2.5 * math.log10(float(row[4])/float(row[5])))

    C_S36_S80.append(-2.5 * math.log10(float(row[2])/float(row[5])))

    r_sint_mujy.append(float(row[7])*1000)

#   We have milli Jy (radio) and micro Jy (IR)

    flux_ratio.append(float(row[6])/(float(row[2])/1000))
    rcount=rcount+1
	
	        	
#    End of do block
# Now ELAIS

print "Row Count : ",rcount,"\n"

db.query("SELECT t1.swire_index_spitzer, t1.cid,  \
                     t2.irac_3_6_micron_flux_mujy, \
                     t2.irac_4_5_micron_flux_mujy, \
                     t2.irac_5_8_micron_flux_mujy, \
                     t2.irac_8_0_micron_flux_mujy, \
                     t3.sp, \
                     t3.sint, \
	             t2.redshift \
              from atlas_dr3.elais_matches t1, fusion.swire_elais t2, atlas_dr3.elais_radio_properties t3 \
              where t1.swire_index_spitzer=t2.index_spitzer \
              and t1.cid=t3.id \
              and t2.irac_3_6_micron_flux_mujy > 0.0 \
	      and t2.irac_4_5_micron_flux_mujy > 0.0 \
	      and t2.irac_5_8_micron_flux_mujy > 0.0 \
	      and t2.irac_8_0_micron_flux_mujy > 0.0 \
              and t1.reliability > 0.8;")
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=50000)

E_S45_S80=[]
E_S36_S58=[]
E_S36_S45=[]
E_S58_S80=[]
E_S36_S80=[]
E_S36_S45=[]	

rcount=1

for row in rows:


    r_sp_1_4_flux_mjy.append(float(row[6]))
    r_sint_1_4_flux_mjy.append(float(row[7]))
    redshift.append(float(row[8]))
#   For colour-colour plot we need magnitude
#   m1 - m2 = -2.5 log_10 (f1/f2)	
    E_S45_S80.append(-2.5 * math.log10(float(row[3])/float(row[5])))
    E_S36_S58.append(-2.5 * math.log10(float(row[2])/float(row[4])))

    E_S36_S45.append(-2.5 * math.log10(float(row[2])/float(row[3])))
    E_S58_S80.append(-2.5 * math.log10(float(row[4])/float(row[5])))

    E_S36_S80.append(-2.5 * math.log10(float(row[2])/float(row[5])))

    r_sint_mujy.append(float(row[7])*1000)
#   We have milli Jy (radio) and micro Jy (IR)
    flux_ratio.append(float(row[6])/(float(row[2])/1000))
    rcount=rcount+1
	
	        	
#    End of do block

# Close connection to the database
db.close()

print "Row Count : ",rcount,"\n"

# Now plot the data

# Colour - Colour Plots IR

#plt.yscale('log')
#plt.xscale('log')
plt.scatter(C_S36_S58,C_S45_S80,color='blue',s=5)
plt.scatter(E_S36_S58,E_S45_S80,color='red',s=5)
#plt.title(field)
plt.grid(True)
#plt.xlim(0.0)
#plt.ylim(0.0)
plt.ylabel('[S_4.5]-[S_8.0]')
plt.xlabel('[S_3.6]-[S_5.8]')
plot_fname='atlas_color-01.pdf'
fname=plot_fname
plt.savefig(fname,format='pdf')
plt.show()

#plt.yscale('log')
#plt.xscale('log')
plt.scatter(C_S36_S45,C_S36_S80,color='blue',s=5)
plt.scatter(E_S36_S45,E_S36_S80,color='red',s=5)
#plt.title(field)
plt.grid(True)
#plt.xlim(0.0)
#plt.ylim(0.0)
plt.ylabel('[S_3.6]-[S_8.0]')
plt.xlabel('[S_3.6]-[S_4.5]')
plot_fname='atlas_color-02.pdf'
fname=plot_fname
plt.savefig(fname,format='pdf')
plt.show()

#plt.yscale('log')
#plt.xscale('log')
plt.scatter(C_S58_S80,C_S36_S45,color='blue',s=5)
plt.scatter(E_S58_S80,E_S36_S45,color='red',s=5)
#plt.title(field)
plt.grid(True)
#plt.xlim(0.0)
#plt.ylim(0.0)
plt.xlabel('[S_5.8]-[S_8.0]')
plt.ylabel('[S_3.6]-[S_4.5]')
plot_fname='atlas_color-03.pdf'
fname=plot_fname
plt.savefig(fname,format='pdf')
plt.show()

plt.yscale('log')
plt.xlim((0,3))
plt.plot(redshift,flux_ratio,'k.')
plt.title(' ')
plt.ylabel('S[1.4GHz] / S[3.6um]')
plt.xlabel('Redshift')
plot_fname='flux_ratio_redshift.pdf'
fname=plot_fname
plt.savefig(fname,format='pdf')
plt.show()

print "End Plotting\n"


