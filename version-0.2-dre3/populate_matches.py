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
	
    db.query("truncate table %s.matches;" % (field))
    db.query("set session wait_timeout=30000;")
    db.query("set session interactive_timeout=30000;")
	
#	limit 0,3000000;
	
    sql=("insert into "+field+".matches(cid,swire_index_spitzer,dx,dy,r_arcsec,flux) "
              "select t1.cid, "
              "t2.Index_Spitzer, "
              "(t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg), "
              "t1.Dec_Deg-t2.DEC_SPITZER, "
              "sqrt(pow((t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg),2)+pow(t1.Dec_Deg-t2.DEC_SPITZER,2))*3600, "
              "t2.irac_3_6_micron_flux_mujy "
              "from "+field+".atlasdr3_fullcmpcat as t1, "+swire_schema+".swire as t2 "
              "where pow((t1.RA_Deg-t2.RA_SPITZER)*cos(t1.Dec_Deg),2)+" 
              "pow(t1.Dec_Deg-t2.DEC_SPITZER,2) <= pow("+str(sr)+"/3600,2) "
              " and   t2.ra_spitzer > "+str(ra1)+" and t2.ra_spitzer < "+str(ra2)+" "
              " and   t2.dec_spitzer > "+str(dec1)+" and t2.dec_spitzer < "+str(dec2)+" limit 0,3000000; ")

#    sql='select * from '+field+'.matches;'
    print sql,"\n"
	
    print "This SQL will take a while .... \n"
    db.query(sql)
    
    db.commit()

# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
#    r=db.use_result()

# fetch results, returning char we need float !

#    rows=r.fetch_row(maxrows=100)

# Close connection to the database

    db.close()

#    print rows

# rows is a tuple, convert it to a list

#    lst_rows=list(rows)
	
#    for row in lst_rows:
#        print row+"\n"
	
    print "End of populate matches\n"





