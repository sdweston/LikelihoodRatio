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

# ask which field to process
field=raw_input('Which field cdfs/elais ?')
print "\nentered : ",field,"\n"

schema='atlas_dr3'

if field == 'CDFS':
    search_prefix='C'
else:
    search_prefix='E'



radio_image_fits='d:\\'+field+'\\atlas_'+field+'_map.fits'

nonradio_image_fits='d:\\'+field+'\\'+field+'_s1_factor2.fits'

print "Starting Postage Stamps"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
# This gets a list of the possible radio pairs  

sql1=("select t1.cid,t1.swire_index_spitzer,t2.ra,t2.decl,t1.reliability "
      "    from "+schema+"."+field+"_matches as t1, "+schema+"."+field+"_coords as t2 "
      "    where t1.reliability > 0.8 "
      "    and t1.cid=t2.id "
      "    and t1.cid not like '"+search_prefix+"%' "
      "    limit 2000;")
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
    ra_radio=row[2]
    dec_radio=row[3]
    rel=row[4]

    print "Match :",cid1,swire_id,ra_radio,dec_radio
    f_ra_radio1=float(ra_radio)
    f_dec_radio1=float(dec_radio)

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")


#   So now get coords for spitzer match
    sql=("SELECT ra_spitzer, dec_spitzer \
              from fusion.swire_"+field+" \
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

    region_file_name=cid1+'_'+ra_radio+'_'+dec_radio+'.reg'
    f=open(region_file_name,'w')
    f.write('global color=blue font="helvetica 10 normal "\n')
    # put a cross for the radio source
    f.write('global color=red\n')
#   f.write('fk5;circle( '+ra_radio1+' , '+dec_radio1+' ,1") # point=cross text={'+cid1+'}\n')
    f.write('fk5;circle( '+ra_radio+' , '+dec_radio+' ,1") \n')
 
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
    #f.write('fk5;circle( '+ra_spitzer+' , '+dec_spitzer+' ,0.05") # text={'+str(idx_sub_row)+'}\n')
    f.write('fk5;circle( '+ra_spitzer+' , '+dec_spitzer+' ,0.05") \n')
    # put in the values of spitzer_index, relibility & likelihood
    #f.write('fk5;circle('+str(t_ra1)+' , '+str(t_dec1)+',0.1") # text={'+str(idx_sub_row)+' : '+swire_id+' '+rel+'}\n')

# Need to mark the radio sources

# This gets a list of the possible radio pairs

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
    sql=("select cid1, \
	        (select ra from atlas_dr3."+field+"_coords where id=cid1) ra1,  \
                (select decl from atlas_dr3."+field+"_coords where id=cid1) dec1, \
	  cid2, \
                (select ra from atlas_dr3."+field+"_coords where id=cid2) ra2, \
	        (select decl from atlas_dr3."+field+"_coords  where id=cid2) dec2 \
      from atlas_dr3."+field+"_radio_pairs \
      where id="+cid1+";")
    
    print sql,"\n"
    db.query(sql)

    r=db.use_result()
    rows2=r.fetch_row(maxrows=1000)
    db.close()

    for row2 in rows2:
        cid1=row2[0]
        ra_radio1=row2[1]
        dec_radio1=row2[2]
        cid2=row2[3]
        ra_radio2=row2[4]
        dec_radio2=row2[5]
        print "Radio Pair :",cid1,ra_radio1,dec_radio1,cid2,ra_radio2,dec_radio2
    
    # put a cross for the radio source
        f.write('global color=red\n')
        f.write('fk5;point( '+ra_radio1+' , '+dec_radio1+' ) # point=cross text={'+cid1+'}\n')
        f.write('fk5;point( '+ra_radio2+' , '+dec_radio2+' ) # point=cross text={'+cid2+'}\n')

    # Close ihe region file
    f.close()

#------------------------------------------------------------------------------
    # Now create DS9 commands and execute

    contour_file_name=cid1+'_'+ra_radio+'_'+dec_radio+'.con'
    postage_stamp_filename1='D:\\'+field+'\\dr3_radio_pairs\\images\\atlas_'+cid1+'.jpeg'
    
    cmd1='ds9 -zscale -invert '+ \
         ' -geometry 844x922 '+radio_image_fits+' -crop '+ra_radio+' '+dec_radio+ \
         ' 100 100 wcs fk5 arcsec -contour open -contour loadlevels contour_ds9.lev -contour yes ' + \
         ' -regions '+region_file_name+ ' -colorbar no ' +\
         '-contour save '+contour_file_name+' -contour close -zoom to fit -exit ' 
#         '-saveimage '+postage_stamp_filename1+' 100 -exit'
#    print cmd1
 
    postage_stamp_filename='D:\\'+field+'\\dr3_radio_pairs\\images\\'+cid1+'_'+swire_id+'_'+ra_radio+'_'+dec_radio+'.jpeg'
    cmd2='ds9 -zscale -invert '+\
         ' -geometry 844x922 '+nonradio_image_fits+' -crop '+ra_radio+' '+dec_radio+ \
         ' 100 100 wcs fk5 arcsec -contour open -contour load '+contour_file_name+ \
         ' -regions '+region_file_name+ ' -colorbar no -grid load ds9.grd ' +\
         ' -contour close -zoom to fit -saveimage '+postage_stamp_filename+' 100 -exit '
#    print cmd2

    os.system(cmd1)
    os.system(cmd2)


# End of do block

print "End"

