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


radio_image_fits='d:\\elaiss1\\atlas_elaiss1_map.fits'

nonradio_image_fits='d:\\elaiss1\\elais_s1_factor2.fits'

print "Starting Postage Stamps"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
# This gets a list of the possible radio pairs  

db.query("select cid1 , \
	        (select ra_deg from elais_s1.coords where cid=cid1) ra1,  \
                (select dec_deg from elais_s1.coords where cid=cid1) dec1, \
                cid2, \
                (select ra_deg from elais_s1.coords where cid=cid2) ra2,\
	        (select dec_deg from elais_s1.coords where cid=cid2) dec2 \
          from elais_s1.radio_pairs \
          where flux1/flux2 > 1.0 \
          and flux1/flux2 < 2.1 \
          and ang_sep_arcsec/sqrt(flux1+flux2) > 2.0 \
          and ang_sep_arcsec/sqrt(flux1+flux2) < 10.0;")

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



#   So now find all records for the pair of radio source (cid)

    db.query("SELECT t1.elais_s1_cid,t2.index_spitzer, t2.ra_spitzer, t2.dec_spitzer, \
             format(t1.lr,4), format(t1.reliability,4) \
             FROM elais_s1.matches t1, swire_es1.es1_swire t2 \
             where t1.lr is not null \
             and (t1.elais_s1_cid='%s' or t1.elais_s1_cid='%s') \
	     and t1.swire_index_spitzer=t2.index_spitzer ;" % (cid1,cid2))
             
#   Create a DS9 region file for this radio source


    region_file_name=cid1+'_'+ra_radio1+'_'+dec_radio1+'.reg'
    f=open(region_file_name,'w')
    f.write('global color=blue font="helvetica 10 normal "\n')
    # put a cross for the radio source
    f.write('global color=red\n')
    f.write('fk5;circle( '+ra_radio1+' , '+dec_radio1+' ,1") # point=cross text={'+cid1+'}\n')
    f.write('fk5;circle( '+ra_radio2+' , '+dec_radio2+' ,1") # point=cross text={'+cid2+'}\n')


#   Get the returned rows and print out, for each non-radio candidate
#   within the search radius of the radio source

    r=db.use_result()
    sub_rows=r.fetch_row(maxrows=5000)

#   Define start coords for full txt string for object
    t_ra1=f_ra_radio1+0.02
    t_dec1=f_dec_radio1+0.01
    idx_sub_row=1

    for sub_row in sub_rows:
        index_spitzer=sub_row[1]
        ra_spitzer=sub_row[2]
        dec_spitzer=sub_row[3]
        lr=sub_row[4]
        rel=sub_row[5]
        print "Spitzer Candidate: ",index_spitzer,ra_spitzer,dec_spitzer,lr,rel

        # add lines to the region file to identify the non-radio candidates

        f.write('global color=yellow\n')
        f.write('fk5;circle( '+ra_spitzer+' , '+dec_spitzer+' ,1") # point=cross\n')
        f.write('fk5;circle( '+ra_spitzer+' , '+dec_spitzer+' ,0.05") # text={'+str(idx_sub_row)+'}\n')
        # put in the values of spitzer_index, relibility & likelihood
        f.write('fk5;circle('+str(t_ra1)+' , '+str(t_dec1)+',0.1") # text={'+str(idx_sub_row)+' : '+index_spitzer+', '+lr+', '+rel+'}\n')
        t_dec1=t_dec1-0.002
        idx_sub_row=idx_sub_row+1

    # Close ihe region file
    f.close()


    # Now create DS9 commands and execute

    contour_file_name=cid1+'_'+ra_radio1+'_'+dec_radio1+'.con'
    postage_stamp_filename1='d:\\elaiss1\\150_arcsec\\atlas_'+cid1+'_'+cid2+'.jpeg'
    
    cmd1='ds9 -zscale -invert '+radio_image_fits+' -crop '+ra_radio1+' '+dec_radio1+ \
         ' 150 150 wcs fk5 arcsec -contour open -contour loadlevels contour_ds9.lev -contour yes ' + \
         ' -regions '+region_file_name+ ' -colorbar no ' +\
         '-contour save '+contour_file_name+' -contour close -zoom to fit ' +\
         '-saveimage '+postage_stamp_filename1+' 100 -exit'
#    print cmd1
 
    postage_stamp_filename='d:\\elaiss1\\150_arcsec\\swire_'+cid1+'_'+cid2+'_'+ra_radio1+'_'+dec_radio1+'.jpeg'
    cmd2='ds9 -zscale -invert '+ nonradio_image_fits+' -crop '+ra_radio1+' '+dec_radio1+ \
         ' 150 150 wcs fk5 arcsec -contour open -contour load '+contour_file_name+ \
         ' -regions '+region_file_name+ ' -colorbar no ' +\
         ' -contour close -zoom to fit -saveimage '+postage_stamp_filename+' 100 -exit '
#    print cmd2

    os.system(cmd1)
    os.system(cmd2)


# End of do block

# Close connection to the database
db.close()

print "End"

