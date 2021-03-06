#===========================================================================
#
# postage_stamp_mysql.py
#
# Python script to query SWIRE_CDFS mysql databasea and create the postage
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


radio_image_fits='d:\\cdfs\\atlas_cdfs_map.fits'

nonradio_image_fits='d:\\cdfs\\swire_cdfs_i1.fits'

print "Starting Postage Stamps"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
# This gets a list of the possible radio pairs  

db.query("select t1.cid,t1.swire_index_spitzer,t2.ra,t2.decl,format(t1.reliability,2) \
          from atlas_dr3.cdfs_matches as t1, atlas_dr3.cdfs_coords as t2 \
          where t1.reliability > 0.8 \
          and t1.cid like 'C%' \
          and t2.id=t1.cid \
          limit 100;")

# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
r=db.use_result()

# fetch results, returning char we need float !

# for testing limit to two
rows=r.fetch_row(maxrows=100)

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
              from fusion.swire_cdfs \
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
    f.write('fk5;circle( '+ra_radio1+' , '+dec_radio1+' ,1") # width = 2 \n')
	# Put in search radius
    f.write('fk5;circle( '+ra_radio1+' , '+dec_radio1+' ,10") # width = 2 \n')
 
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
    f.write('fk5;circle( '+ra_spitzer+' , '+dec_spitzer+' ,1")    # width=2 \n')
    f.write('fk5;circle( '+ra_spitzer+' , '+dec_spitzer+' ,0.05") # point=cross \n')
    # put in the values of spitzer_index, relibility & likelihood
    #f.write('fk5;circle('+str(t_ra1)+' , '+str(t_dec1)+',0.1") # text={'+str(idx_sub_row)+' : '+swire_id+' '+rel+'}\n')

    # Find the other candidates with a rel < 0.8 and put them on as well !
    
    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
    sql=("select t1.cid,t2.ra_spitzer, t2.dec_spitzer, t1.reliability \
                from atlas_dr3.cdfs_matches as t1, fusion.swire_cdfs as t2 \
                where t1.swire_index_spitzer=t2.index_spitzer \
                and t1.reliability < 0.8 \
                and t1.cid='"+cid1+"';")
    print sql,"\n"
    db.query(sql)

    r1=db.use_result()
    sub_rows1=r1.fetch_row(maxrows=10)

    db.close

    for sub_row1 in sub_rows1:
        cid2=sub_row1[0]
        ra_spitzer1=sub_row1[1]
        dec_spitzer1=sub_row1[2]
        reliability2=sub_row1[3]
        print "Spitzer Candidate: ",cid2,ra_spitzer1,dec_spitzer1,reliability2

        f.write('global color=magenta\n')
        f.write('fk5;circle( '+ra_spitzer1+' , '+dec_spitzer1+' ,1") # width=2 \n')
        
    
    # Close ihe region file
    f.close()

#------------------------------------------------------------------------------
    # Now create DS9 commands and execute

    contour_file_name='d:\\cdfs\\dr3\\atlas_'+cid1+'_'+ra_radio1+'_'+dec_radio1+'.con'
    postage_stamp_filename1='d:\\cdfs\\dr3\\images\\atlas_'+cid1+'.jpeg'
    pp_fits='d:\\cdfs\\dr3\\images\\atlas_'+cid1+'.fits'
    
    cmd1='ds9 -zscale -invert '+ \
         ' -geometry 844x922 -fits '+radio_image_fits+ \
         ' -crop '+ra_radio1+' '+dec_radio1+ ' 50 50 wcs fk5 arcsec ' + \
         ' -contour open -contour loadlevels contour_20mjy.lev -contour yes ' + \
         ' -regions '+region_file_name+ ' -colorbar no -zoom to fit ' +\
         ' -contour save '+contour_file_name+' -contour close -exit ' 
#         ' -saveimage '+postage_stamp_filename1+' 100 -exit'
#    print cmd1
 
    cmd2='ds9 -zscale -invert '+ \
         ' -geometry 844x922 -fits '+nonradio_image_fits+' -contour open -contour load '+contour_file_name+ \
         ' -contour close ' + \
         ' -crop '+ra_radio1+' '+dec_radio1+ ' 100 100 wcs fk5 arcsec ' + \
         ' -regions '+region_file_name+ ' -colorbar no -align yes -orient xy ' + \
         ' -zoom to fit -saveimage fits '+pp_fits+' -exit '
#         ' -grid load ds9.grd -zoom to fit -saveimage '+postage_stamp_filename+' 100  '
#    print cmd2

    postage_stamp_filename='d:\\cdfs\\dr3\\images\\'+cid1+'_'+swire_id+'_'+ra_radio1+'_'+dec_radio1+'.jpeg'
    cmd3='ds9 -zscale -invert '+ \
         ' -geometry 1024x1024 -fits '+pp_fits+' -contour open -contour load '+contour_file_name+ \
         ' -contour close ' + \
         ' -crop '+ra_radio1+' '+dec_radio1+ ' 70 70 wcs fk5 arcsec ' + \
         ' -regions '+region_file_name+ ' -colorbar no -align yes -orient xy ' + \
         ' -grid load ds9-nogrid.grd -zoom to fit -saveimage '+postage_stamp_filename+' 100 -exit '
#    print cmd2

# Need to do it again, apply contours etc and crop to say 70 70 !

    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
#    os.system(cmd3)


# End of do block

print "End"

