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

def populate_matches():

    print "\nStarting finding nearest neighbours between catalogues\n"

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry

    print field,field,swire_schema,sr,ra1,ra2,dec1,dec2

    db.query("set session wait_timeout=30000;")
    db.query("set session interactive_timeout=30000;")
	
#	limit 0,3000000;
	
#    db.query("insert into %s.matches(cid,swire_index_spitzer,dx,dy,r_arcsec,flux) \
     db.query("select t1.cid, \
                            t2.Index_Spitzer, \
	                        (t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg), \
	                        t1.Dec_Deg-t2.DEC_SPITZER, \
	                        sqrt(pow((t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg),2)+pow(t1.Dec_Deg-t2.DEC_SPITZER,2))*3600, \
	                        t2.irac_3_6_micron_flux_mujy \
                     from %s.coords as t1, %s.swire as t2 \
                     where pow((t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg),2)+ \
                     pow(t1.Dec_Deg-t2.DEC_SPITZER,2) <= pow(%s/3600,2) \
                     and   t2.ra_spitzer > %s \
                     and   t2.ra_spitzer < %s \
                     and   t2.dec_spitzer < %s \
                     and   t2.dec_spitzer > %s; " % (field,swire_schema,sr,ra1,ra2,dec1,dec2))


	
# Close connection to the database
    db.close()

    print "End of populate matches\n"





