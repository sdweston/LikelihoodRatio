#===========================================================================
#
# postage_stamp_radio_pairs.py
#
# Python script to query mysql databasea and create the postage
# stamp images of the radio contours overlayed onto the spitzer image.
#
#===========================================================================
#
# S. Weston
# AUT University
# Feb 2014
#===========================================================================

import array
import _mysql
import numpy
import math
import sys
import os

field='cdfs'

radio_image_fits='d:\\'+field+'\\atlas_'+field+'_map.fits'

nonradio_image_fits='d:\\'+field+'\\'+field+'_s1_factor2.fits'


print "Starting Postage Stamps"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
# This gets a list of the possible radio pairs  

sql=("select cid1, \
	        (select ra from atlas_dr3."+field+"_coords where id=cid1) ra1,  \
                (select decl from atlas_dr3."+field+"_coords where id=cid1) dec1, \
	  cid2, \
                (select ra from atlas_dr3."+field+"_coords where id=cid2) ra2, \
	        (select decl from atlas_dr3."+field+"_coords  where id=cid2) dec2 \
      from atlas_dr3."+field+"_radio_pairs \
      where flag='rd';")

print sql,"\n"
db.query(sql)
	
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=1000)

# Close connection to the database
db.close()

#print rows

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

for row in rows:
    cid1=row[0]
    ra_radio1=row[1]
    dec_radio1=row[2]
    cid2=row[3]
    ra_radio2=row[4]
    dec_radio2=row[5]
    print "Radio Pair :",cid1,ra_radio1,dec_radio1,cid2,ra_radio2,dec_radio2
    f_ra_radio1=float(ra_radio1)
    f_dec_radio1=float(dec_radio1)
    f_ra_radio2=float(ra_radio2)
    f_dec_radio2=float(dec_radio2)

            
#   Create a DS9 region file for this radio source


    region_file_name=cid1+'_'+ra_radio1+'_'+dec_radio1+'.reg'
    f=open(region_file_name,'w')
    f.write('global color=blue font="helvetica 10 normal "\n')
    # put a cross for the radio source
    f.write('global color=red\n')
    f.write('fk5;circle( '+ra_radio1+' , '+dec_radio1+' ,1") # point=cross text={'+cid1+'}\n')
    f.write('fk5;circle( '+ra_radio2+' , '+dec_radio2+' ,1") # point=cross text={'+cid2+'}\n')


    # Close the region file
    f.close()


    # Now create DS9 commands and execute

    contour_file_name=cid1+'_'+ra_radio1+'_'+dec_radio1+'.con'
    postage_stamp_filename1='D:\\'+field+'\\radio_pairs\\atlas_'+cid1+'_'+cid2+'.jpeg'
    
    cmd1='ds9 -zscale -invert '+radio_image_fits+' -crop '+ra_radio1+' '+dec_radio1+ \
         ' 150 150 wcs fk5 arcsec -contour open -contour loadlevels contour_ds9.lev -contour yes ' + \
         ' -regions '+region_file_name+ ' -colorbar no ' +\
         '-contour save '+contour_file_name+' -contour close -zoom to fit -grid yes ' +\
         '-saveimage '+postage_stamp_filename1+' 100 '
#    print cmd1
 
    postage_stamp_filename='D:\\'+field+'\\radio_pairs\\swire_'+cid1+'_'+cid2+'_'+ra_radio1+'_'+dec_radio1+'.jpeg'
    cmd2='ds9 -zscale -invert '+ nonradio_image_fits+' -crop '+ra_radio1+' '+dec_radio1+ \
         ' 150 150 wcs fk5 arcsec -contour open -contour load '+contour_file_name+ \
         ' -regions '+region_file_name+ ' -colorbar no ' +\
         ' -contour close -zoom to fit -grid yes -saveimage '+postage_stamp_filename+' 100 '
#    print cmd2

    os.system(cmd1)
    os.system(cmd2)


# End of do block

# Close connection to the database
db.close()

print "End"

