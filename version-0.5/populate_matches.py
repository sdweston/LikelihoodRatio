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

# Using FUSION servs-es1-data-fusion-sextractor.readme	18-Jul-2014 14:48, alot of the flus_ap2_36 (SWIRE_2013) entrys are Zero.
# So lets try FLUX_APER_1_1 which is from http://irsa.ipac.caltech.edu/data/SPITZER/SWIRE/docs/delivery_doc_r2_v2.pdf

    sql1=("insert into "+schema+"."+field+"_matches(cid,swire_index_spitzer,dx,dy,r_arcsec,flux) "
              "select t1.id, "
              "t2.ID_12, "
              "(t1.ra-"+str(posn_offset_ra)+"-t2.ra_1_1)*cos(t1.decl-"+str(posn_offset_dec)+"), "
              "t1.decl-"+str(posn_offset_dec)+"-t2.dec_12, "
              "sqrt(pow((t1.ra-"+str(posn_offset_ra)+"-t2.ra_1_1)*cos(t1.decl-"+str(posn_offset_dec)+"),2)+pow(t1.decl-"+str(posn_offset_dec)+"-t2.dec_1_1,2))*3600, "
#			  "t2.flux_ap2_36 "
              "t2.flux_aper_2_1 "
              "from "+schema+"."+field+"_coords as t1, fusion."+field+" as t2 "
              "where pow((t1.ra-"+str(posn_offset_ra)+"-t2.ra_1_1)*cos(t1.decl-"+str(posn_offset_dec)+"),2)+" 
              "pow(t1.decl-"+str(posn_offset_dec)+"-t2.dec_1_1,2) <= pow("+str(sr)+"/3600,2) "
              " and   t2.ra_1_1 > "+str(ra1)+" and t2.ra_1_1 < "+str(ra2)+" "
              " and   t2.dec_1_1 > "+str(dec1)+" and t2.dec_1_1 < "+str(dec2)+" limit 0,3000000; ")


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





