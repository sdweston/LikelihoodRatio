import array
import _mysql
import numpy
import math
import sys
import os

# ask which field to process
answer=raw_input('Which field cdfs/elais ?')
print "\nentered : ",answer,"\n"

radio_image_fits='d:\\'+answer+'\\atlas_'+answer+'_map.fits'

nonradio_image_fits='d:\\'+answer+'\\'+answer+'_s1_factor2.fits'

print "Starting Postage Stamps"

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Find the possible IR multiples, from those radio sources with more than one IR candidate
# between the reliability figures.

sql1="create temporary table if not exists atlas_dr3."+answer+"_ird as ( \
          select cid,swire_index_spitzer,reliability \
          from atlas_dr3."+answer+"_matches  \
          where reliability > 0.3 and reliability < 0.7) ;"

print sql1,"\n"
db.query(sql1)          

# This will give me the cid's

sql2=("select cid,count(cid) as cnt from atlas_dr3."+answer+"_ird \
       group by cid having cnt >1;")
 
print sql2,"\n"
db.query(sql2)

	
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

cat_file_name=answer+'_ir_multiple.cat'
f1=open(cat_file_name,'w')

for row in rows:
    cid1=row[0]


#    print "Match :",cid1

# For each cid find the ir candidates
# we need ra,dec for radio source and ra,dec for ir candidates

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

    sql3="select ra,decl from atlas_dr3."+answer+"_coords \
         where id='"+cid1+"';"
#    print sql3,"\n"
    db.query(sql3)
    r=db.use_result()
    rows=r.fetch_row(maxrows=0)
    db.close()

    for row in rows:
        ra_radio=row[0]
        dec_radio=row[1]
        print "Coords : ",cid1,ra_radio,dec_radio
        f_ra_radio=float(ra_radio)
        f_dec_radio=float(dec_radio)

#------------------------------------------------------------------------------             
#   Create a DS9 region file for this radio source

    region_file_name=cid1+'_'+ra_radio+'_'+dec_radio+'.reg'
    f=open(region_file_name,'w')
    f.write('global color=blue font="helvetica 10 normal "\n')
    # put a cross for the radio source
    f.write('global color=red\n')
    f.write('fk5;circle( '+ra_radio+' , '+dec_radio+' ,1") # point=cross \n')
    f.write('fk5;circle( '+ra_radio+' , '+dec_radio+' ,10") # point=cross \n')
 
#   Define start coords for full txt string for object
    t_ra1=f_ra_radio+0.02
    t_dec1=f_dec_radio+0.01
    idx_sub_row=1
    
# Now for each of these radio sources get a list of the IR candidates

    sql4="select swire_index_spitzer,reliability \
          from atlas_dr3."+answer+"_matches \
          where reliability > 0.3 and reliability < 0.7 \
          and cid='"+cid1+"' ;"

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
    db.query(sql4)
    r=db.use_result()
    rows=r.fetch_row(maxrows=0)
    db.close()

    for row in rows:
        swire_id=row[0]
        rel=row[1]
#        print "IR Candidate : ",swire_id,rel
        db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")


#   So now get coords for spitzer match
        sql5=("SELECT ra_12, dec_12, flux_ap2_36, redshift \
              from fusion."+answer+"  \
              where id_12="+swire_id+";")
        db.query(sql5)
        r=db.use_result()
        sub_rows=r.fetch_row(maxrows=10)
        db.close()
        for sub_row in sub_rows:
            ra_spitzer=sub_row[0]
            dec_spitzer=sub_row[1]
            f_3_6=sub_row[2]
            redshift=sub_row[3]
        
        print >> f1, cid1,ra_radio,dec_radio,idx_sub_row,swire_id,ra_spitzer,dec_spitzer,rel,f_3_6,redshift

        # add lines to the region file to identify the non-radio candidates

        f.write('global color=yellow\n')
        f.write('fk5;circle( '+ra_spitzer+' , '+dec_spitzer+' ,1") # point=cross\n')
        f.write('fk5;circle( '+ra_spitzer+' , '+dec_spitzer+' ,0.05") # text={'+str(idx_sub_row)+'}\n')
        # put in the values of spitzer_index, relibility & likelihood
        #f.write('fk5;circle('+str(t_ra1)+' , '+str(t_dec1)+',0.1") # text={'+str(idx_sub_row)+' : '+swire_id+' '+rel+'}\n')
        idx_sub_row=idx_sub_row+1
                

    # Close ihe region file
    f.close()

        #------------------------------------------------------------------------------
    # Now create DS9 commands and execute

    contour_file_name='d:\\'+answer+'\\dr3_ir_doubles\\atlas_'+cid1+'_'+ra_radio+'_'+dec_radio+'.con'
    postage_stamp_filename1='d:\\'+answer+'\\dr3_ir_doubles\\atlas_'+cid1+'.jpeg'
    
    cmd1='ds9 -zscale -invert '+radio_image_fits+' -crop '+ra_radio+' '+dec_radio+ \
         ' 75 75 wcs fk5 arcsec -contour open -contour loadlevels contour_20mjy.lev -contour yes ' + \
         ' -regions '+region_file_name+ ' -colorbar no ' +\
         '-contour save '+contour_file_name+' -contour close -zoom to fit ' +\
         '-saveimage '+postage_stamp_filename1+' 100 -exit'
#    print cmd1
 
    postage_stamp_filename='d:\\'+answer+'\\dr3_ir_doubles\\'+cid1+'_'+ra_radio+'_'+dec_radio+'.jpeg'
    cmd2='ds9 -zscale -invert  ' +\
         ' -geometry 844x922 '+ nonradio_image_fits+' -crop '+ra_radio+' '+dec_radio+ \
         ' 100 100 wcs fk5 arcsec -contour open -contour load '+contour_file_name+ \
         ' -regions '+region_file_name+ ' -colorbar no ' +\
         ' -contour close -grid load ds9.grd  -zoom to fit ' +\
		 ' -saveimage '+postage_stamp_filename+' 100 -exit '
#    print cmd2

#    os.system(cmd1)
#    os.system(cmd2)
	
f1.close()

        
    
    
