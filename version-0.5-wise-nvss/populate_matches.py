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

#   Search Radius for NN	
    sr=10

# Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)    

# Lets run a querry

    print "Truncate the matches table\n"
	
    db.query("truncate table "+schema+".matches;")
    db.query("set session wait_timeout=30000;")
    db.query("set session interactive_timeout=30000;")
	
#   limit 0,3000000;
#   First find all matches within search radius
    
    print "find all matches within search radius\n"

    sql1=("select name,centroid_ra,centroid_dec from "+schema+".sumss_centroids;")
    print sql1,"\n"
    db.query(sql1)
          

    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=10)

# rows is a tuple, convert it to a list

    for row in rows:
           sumss_name=row[0]
           centroid_ra=row[1]
           centroid_dec=row[2]
           print sumss_name, centroid_ra, centroid_dec

# Change the logic here, for each entry in NVSS ands SUMSS find the NN within the search radius

# Add "theta" angle of vector between Radio and IR sources.
#     This function returns the arctangent of the two arguments: X and Y. 
#     It is similar to the arctangent of Y/X, except that the signs of both
#     are used to find the quadrant of the result.

# Original SQL to find NN
#    sql1=("insert into "+schema+".matches(name,wise_name,dx,dy,r_arcsec,flux,theta) "
#              "select t1.name, "
#              "t2.Index_Spitzer, "
#              "(t1.centroid_ra-t2.ra)*cos(radians(t1.centroid_decl), "
#              "t1.centroid_dec-t2.decl, "
#              "sqrt(pow((t1.ra-t2.RA_Spitzer)*cos(radians(t1.decl)),2)+pow(t1.decl-"+str(posn_offset_dec)+"-t2.Dec_Spitzer,2))*3600, "
#              "t2.IRAC_3_6_micron_Flux_muJy,			  "
#	      "atan2((t1.ra-"+str(posn_offset_ra)+"-t2.RA_Spitzer)*cos(radians(t1.decl-"+str(posn_offset_dec)+")),t1.decl-"+str(posn_offset_dec)+"-t2.Dec_Spitzer) "
#              "from "+schema+"."+field+"_coords as t1, fusion.swire_"+field+" as t2 "
#              "where pow((t1.ra-"+str(posn_offset_ra)+"-t2.RA_Spitzer)*cos(radians(t1.decl-"+str(posn_offset_dec)+")),2)+" 
#              "pow(t1.decl-"+str(posn_offset_dec)+"-t2.Dec_Spitzer,2) <= pow("+str(sr)+"/3600,2) "
#              " and   t2.RA_Spitzer > "+str(ra1)+" and t2.RA_Spitzer < "+str(ra2)+" "
#              " and   t2.Dec_Spitzer > "+str(dec1)+" and t2.Dec_Spitzer < "+str(dec2)+" limit 0,3000000; ")

           sql2=("select source_id,ra,decl, "
		         "sqrt(pow((1.49021-ra)*cos(radians(-56.47542)),2)+pow(-56.47542-decl,2))*3600 "
		        "from "+schema+".wise_5amin_4jy "
                "where pow(("+centroid_ra+"-ra)*cos(radians("+centroid_dec+")),2)+" 
                "pow("+centroid_dec+"-decl,2) <= pow("+str(sr)+"/3600,2); "		)

           print sql2,"\n"
	
    print "This SQL will take a while .... \n"
#    db.query(sql1)
    
#    db.commit()

    db.close()	
	
    print "End of populate matches\n"





