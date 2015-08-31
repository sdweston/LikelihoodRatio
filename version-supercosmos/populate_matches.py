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

    print "Truncate the matches table\n"
	
    db.query("truncate table "+schema+"."+schema+"_matches;")
    db.query("set session wait_timeout=30000;")
    db.query("set session interactive_timeout=30000;")
	
#   limit 0,3000000;
#   First find all matches, change tables to use atlas_dr3 schema.
#   Need to allow for position offset between catalogues, Middelberg 2007
    
    print "find all matches within search radius\n"

# Add "theta" angle of vector between Radio and IR sources.
#     This function returns the arctangent of the two arguments: X and Y. 
#     It is similar to the arctangent of Y/X, except that the signs of both
#     are used to find the quadrant of the result.

    sql1=("insert into "+schema+"."+schema+"_matches(nvss_id,supercosmos_id,dx,dy,r_arcsec,flux,theta) "
              "select t1.id, "
              "t2.id, "
              "(t1.ra_2000-t2.ra_2000)*cos(radians(t1.decl_2000)), "
              "t1.decl_2000-t2.dec_2000, "
              "sqrt(pow((t1.ra_2000-t2.ra_2000)*cos(radians(t1.decl_2000)),2)+pow(t1.decl_2000-t2.dec_2000,2))*3600, "
              "t1.S1_4, "
			  "atan2(t1.decl_2000-t2.dec_2000,(t1.ra_2000-t2.ra_2000)*cos(radians(t1.decl_2000))) "
              "from nvss_gama12.nvss_gama12 as t1, supercosmos_gama12.supercosmos_gama12 as t2 "
              "where pow((t1.ra_2000-t2.ra_2000)*cos(radians(t1.decl_2000)),2)+" 
              "pow(t1.decl_2000-t2.dec_2000,2) <= pow("+str(sr)+"/3600,2) "
              " and   t2.ra_2000 > "+str(ra1)+" and t2.ra_2000 < "+str(ra2)+" "
              " and   t2.dec_2000 > "+str(dec1)+" and t2.dec_2000 < "+str(dec2)+" limit 0,3000000; ")


    print sql1,"\n"
	
    print "This SQL will take a while .... \n"
    db.query(sql1)
    
    db.commit()

# Close connection to the database

#    db.close()

# Next delete field records that are a member of a radio pair

# Connect to the local database with the atlas uid

#    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

    db.close()	
	
    print "End of populate matches\n"





