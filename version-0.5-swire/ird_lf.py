import array
import _mysql
import numpy
import math
import sys
import os

# ask which field to process
answer=raw_input('Which field cdfs/elais ?')
print "\nentered : ",answer,"\n"

# open file for writing

filename="d:/temp/" +answer+ "_ird.txt"
f = open(filename,'w')

# Connect to the local database with the atlas uid

db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Preperation, truncate tables etc

# This will give me the cid's

sql2=("select cid,ra,decl,sint,count(cid) from atlas_dr3."+answer+"_ird \
       where reliability > 0.3 and reliability < 0.8 \
       group by cid having count(cid) >1 ;")
 
#print sql2,"\n"
db.query(sql2)

r2=db.use_result()

# fetch results, returning char we need float !

rows=r2.fetch_row(maxrows=0)

for row in rows:
    cid1=row[0]
#    print >> f,row
    print row
	   
# We now have the cid's for the infared multiple candidates
# so go back to matches with these cid's and get the fusion_spitzer_id's, and ra,dec

#    sql3=("select swire_index_spitzer,ra_spitzer,dec_spitzer,irac_3_6_micron_flux_mujy,reliability \
#            from atlas_dr3."+answer+"_ird \
#            where cid='"+cid1+"';")

# We want angular seperation in arc sec between radio and ir
# "sqrt(pow((t1.ra-"+str(posn_offset_ra)+"-t2.RA_Spitzer)*cos(radians(t1.decl-"+str(posn_offset_dec)+")),2)+pow(t1.decl-"+str(posn_offset_dec)+"-t2.Dec_Spitzer,2))*3600, "


    sql3=("SELECT t1.cid, t3.ra, t3.decl, t2.sp , t2.sint, \
                  t1.swire_index_spitzer, t4.ra_spitzer, t4.dec_spitzer, \
                  sqrt(pow((t3.ra-t4.ra_Spitzer)*cos(radians(t3.decl)),2)+pow(t3.decl-t4.dec_spitzer,2))*3600, \
                  t4.irac_3_6_micron_flux_mujy, t4.irac_3_6_micron_flux_error_mujy,t4.redshift, t1.reliability,'1' \
           FROM atlas_dr3."+answer+"_matches t1, atlas_dr3."+answer+"_radio_properties as t2, atlas_dr3."+answer+"_coords as t3, \
                fusion.swire_"+answer+" as t4 \
           where t1.cid='"+cid1+"' \
           and t1.swire_index_spitzer=t4.index_spitzer \
           and t1.cid=t2.id \
           and t1.cid=t3.id \
           and t1.reliability > 0.1 and t1.reliability < 0.9;")

#    print sql3,"\n"
    db.query(sql3)

    r3=db.use_result()

# fetch results, returning char we need float !

    fsis=r3.fetch_row(maxrows=0)

    for fsi in fsis:
         print >> f,fsi
         print fsi
#        f.write(output)
        
# Close connection to the database
db.close()

# close open file

f.close()

