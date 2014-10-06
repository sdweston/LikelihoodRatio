#===========================================================================
#
# populate_matches.py
#
# Python script to query mysql database to determine the
# nearest neigbours within search radius between catalogues
#
#===========================================================================
#
# S. Weston
# AUT University
# Sept 2013
#===========================================================================

def pm():

    print "\nStarting finding nearest neighbours between catalogues\n"

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry

    print field,field,swire_schema,sr,ra1,ra2,dec1,dec2

    print "Truncate the matches table\n"
	
    db.query("truncate table "+schema+"."+field+"_matches;")
    db.query("set session wait_timeout=30000;")
    db.query("set session interactive_timeout=30000;")
	
#   limit 0,3000000;
#   First find all matches, change tables to use atlas_dr3 schema.
#   Need to allow for position offset between catalogues, Middelberg 2007
    
    print "find all matches within search radius\n"

# Use SWIRE (cdfs/elais)_swire-sdss-cat-plus-full
# Add "theta" angle of vector between Radio and IR sources.
#     This function returns the arctangent of the two arguments: X and Y. 
#     It is similar to the arctangent of Y/X, except that the signs of both
#     are used to find the quadrant of the result.

    sql1=("insert into "+schema+"."+field+"_matches(cid,swire_index_spitzer,dx,dy,r_arcsec,flux,theta) "
              "select t1.id, "
              "t2.Index_Spitzer, "
              "(t1.ra-"+str(posn_offset_ra)+"-t2.RA_Spitzer)*cos(radians(t1.decl-"+str(posn_offset_dec)+")), "
              "t1.decl-"+str(posn_offset_dec)+"-t2.Dec_Spitzer, "
              "sqrt(pow((t1.ra-"+str(posn_offset_ra)+"-t2.RA_Spitzer)*cos(radians(t1.decl-"+str(posn_offset_dec)+")),2)+pow(t1.decl-"+str(posn_offset_dec)+"-t2.Dec_Spitzer,2))*3600, "
              "t2.IRAC_3_6_micron_Flux_muJy,			  "
			  "atan2(t1.decl-"+str(posn_offset_dec)+"-t2.Dec_Spitzer,(t1.ra-"+str(posn_offset_ra)+"-t2.RA_Spitzer)*cos(radians(t1.decl-"+str(posn_offset_dec)+"))) "
              "from "+schema+"."+field+"_coords as t1, fusion.swire_"+field+" as t2 "
              "where pow((t1.ra-"+str(posn_offset_ra)+"-t2.RA_Spitzer)*cos(radians(t1.decl-"+str(posn_offset_dec)+")),2)+" 
              "pow(t1.decl-"+str(posn_offset_dec)+"-t2.Dec_Spitzer,2) <= pow("+str(sr)+"/3600,2) "
              " and   t2.RA_Spitzer > "+str(ra1)+" and t2.RA_Spitzer < "+str(ra2)+" "
              " and   t2.Dec_Spitzer > "+str(dec1)+" and t2.Dec_Spitzer < "+str(dec2)+" limit 0,3000000; ")


    print sql1,"\n"
	
    print "This SQL will take a while .... \n"
    db.query(sql1)
    
    db.commit()

# Close connection to the database

#    db.close()

# Next delete field records that are a member of a radio pair

# Connect to the local database with the atlas uid

#    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

    sql2=("delete from "+schema+"."+field+"_matches where cid in (select cid1 from "+schema+"."+field+"_radio_pairs where flag='rd');")

    sql3=("delete from "+schema+"."+field+"_matches where cid in (select cid2 from "+schema+"."+field+"_radio_pairs where flag='rd');")

    print sql2,"\n"	
    db.query(sql2)
    print sql3,"\n"	
    db.query(sql3)

    db.commit()

    db.close()	
	
    print "End of populate matches\n"





