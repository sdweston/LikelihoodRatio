#===========================================================================
#
# postage_stamp_mysql.py
#
# Python script to query SWIRE_ES1 mysql databasea and create the postage
# stamp images of the radio contours overlayed onto the spitzer image.
#
#===========================================================================
#
# S. Weston
# AUT University
# May 2013
#===========================================================================

import array
import _mysql
import numpy
import math
import sys
import os

schema='atlas_dr3' 
field='elais'

radio_image_fits='d:\\elais\\atlas_elais_map.fits'

nonradio_image_fits='d:\\elais\\elais_s1_factor2.fits'

print "Starting Postage Stamps"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
# This gets a list of the possible radio pairs  

sql1=("select t1.cid,t1.swire_index_spitzer,t2.ra,t2.decl,t1.reliability "
      "    from "+schema+"."+field+"_matches as t1, "+schema+"."+field+"_coords as t2 "
      "    where t1.reliability > 0.8 "
      "    and t1.cid=t2.id "
      "    and t1.cid not like 'E%' "
      "    limit 20000;")
print sql1,"\n"
db.query(sql1)

# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

rows=r.fetch_row(maxrows=0)

# Close connection to the database
db.close()

#print rows

for row in rows:
    cid1=row[0]
    swire_id=row[1]
    ra_radio1=row[2]
    dec_radio1=row[3]
    rel=row[4]

    print "Match :",cid1,swire_id,ra_radio1,dec_radio1
    f_ra_radio1=float(ra_radio1)
    f_dec_radio1=float(dec_radio1)

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")


#   So now get coords for spitzer match
    sql=("SELECT ra_spitzer, dec_spitzer \
              from swire_es1.swire \
              where index_spitzer="+swire_id+";")
    print sql,"\n"
    db.query(sql)

#   Get the returned rows and print out, for each non-radio candidate
#   within the search radius of the radio source

    r=db.use_result()
    sub_rows=r.fetch_row(maxrows=2)
    
# Close connection to the database
    db.close()
    
#------------------------------------------------------------------------------             
#   Create a DS9 region file for this radio source

    region_file_name=cid1+'_'+ra_radio1+'_'+dec_radio1+'.reg'
    f=open(region_file_name,'w')
    f.write('global color=blue font="helvetica 10 normal "\n')
    # put a cross for the radio source
    f.write('global color=red\n')
    f.write('fk5;circle( '+ra_radio1+' , '+dec_radio1+' ,1") # point=cross text={'+cid1+'}\n')
 
#   Define start coords for full txt string for object
    t_ra1=f_ra_radio1+0.02
    t_dec1=f_dec_radio1+0.01
    idx_sub_row=1
    print sub_rows
    
    for sub_row in sub_rows:
        ra_spitzer=sub_row[0]
        dec_spitzer=sub_row[1]
        
    print "Spitzer Candidate: ",swire_id,ra_spitzer,dec_spitzer

    # add lines to the region file to identify the non-radio candidates

    f.write('global color=yellow\n')
    f.write('fk5;circle( '+ra_spitzer+' , '+dec_spitzer+' ,1") # point=cross\n')
    f.write('fk5;circle( '+ra_spitzer+' , '+dec_spitzer+' ,0.05") # text={'+str(idx_sub_row)+'}\n')
    # put in the values of spitzer_index, relibility & likelihood
    f.write('fk5;circle('+str(t_ra1)+' , '+str(t_dec1)+',0.1") # text={'+str(idx_sub_row)+' : '+swire_id+' '+rel+'}\n')

    # Close ihe region file
    f.close()

#------------------------------------------------------------------------------
    # Now create DS9 commands and execute

    contour_file_name=cid1+'_'+ra_radio1+'_'+dec_radio1+'.con'
    postage_stamp_filename1='D:\elais\dr3_radio_pairs\\atlas_'+cid1+'.jpeg'
    
    cmd1='ds9 -zscale -invert '+radio_image_fits+' -crop '+ra_radio1+' '+dec_radio1+ \
         ' 100 100 wcs fk5 arcsec -contour open -contour loadlevels contour_ds9.lev -contour yes ' + \
         ' -regions '+region_file_name+ ' -colorbar no ' +\
         '-contour save '+contour_file_name+' -contour close -zoom to fit ' +\
         '-saveimage '+postage_stamp_filename1+' 100 -exit'
#    print cmd1
 
    postage_stamp_filename='D:\elais\dr3_radio_pairs\\'+cid1+'_'+swire_id+'_'+ra_radio1+'_'+dec_radio1+'.jpeg'
    cmd2='ds9 -zscale -invert '+ nonradio_image_fits+' -crop '+ra_radio1+' '+dec_radio1+ \
         ' 100 100 wcs fk5 arcsec -contour open -contour load '+contour_file_name+ \
         ' -regions '+region_file_name+ ' -colorbar no ' +\
         ' -contour close -zoom to fit -grid load D:\elais\dr3_radio_pairs\ds9.grd -saveimage '+postage_stamp_filename+' 100 -exit '
#    print cmd2

    os.system(cmd1)
    os.system(cmd2)


# End of do block

print "End"

