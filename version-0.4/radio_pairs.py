#===========================================================================
#
# radio_pairs.py
#
# Python script to query SWIRE_ES1 mysql database to search for radio
# pair candidates
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2014
#===========================================================================

def rp():

    print "Starting radio pair candidate search"

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# First back out the previous radio doubles data if any

    if field=='elais':
       prefix="E"
    else:
       prefix="C"

# first delete entries from coords
   
    sql1="delete from "+schema+"."+field+"_coords where id not like '"+prefix+"%';"
    print sql1,"\n"
    db.query(sql1)
	
# delete entries from radio_properties

    sql2="delete from "+schema+"."+field+"_radio_properties where id not like '"+prefix+"%';"
    print sql2,"\n"
    db.query(sql2)
	
# truncate the radio pairs table ready for another run

    sql3="truncate table "+schema+"."+field+"_radio_pairs;"
    print sql3,"\n"
    db.query(sql3)
	
# Find pairs based on ang_sep nearest neighbour.

    sql4=("insert into "+schema+"."+field+"_radio_pairs(cid1,cid2,ang_sep_arcsec)"
         " select t1.id, t2.id,"
         " format(sqrt(pow((t1.RA-t2.RA)*cos(t1.Decl),2)+pow(t1.Decl-t2.Decl,2))*3600,6)"
         " from "+schema+"."+field+"_coords as t1, "+schema+"."+field+"_coords as t2"
         " where pow((t1.RA-t2.RA)*cos(t1.Decl),2)+pow(t1.Decl-t2.Decl,2) <= pow(100/3600,2)"
         " and t1.id!=t2.id"
         " limit 0,20000;")
    print sql4,"\n"		 
    db.query(sql4)
	
		 
# now get the fluxs
# sp-peak flux

# set sql_safe_updates=0;
    sql5=("update "+schema+"."+field+"_radio_pairs as t1"
         " inner join "+schema+"."+field+"_radio_properties as t2"
         " on t1.cid1=t2.id"
         " set t1.flux1=t2.sp;")
    print sql5,"\n"
    db.query(sql5)
		 
    sql6=("update "+schema+"."+field+"_radio_pairs as t1"
         " inner join "+schema+"."+field+"_radio_properties as t2"
         " on t1.cid2=t2.id"
         " set t1.flux2=t2.sp;")
    print sql6,"\n"
    db.query(sql6)
	
    sql7=("update "+schema+"."+field+"_radio_pairs as t1"
         " inner join "+schema+"."+field+"_deconv as t2"
         " on t1.cid1=t2.id"
         " set t1.deconv1=t2.deconv;")
    print sql7,"\n"
    db.query(sql7)
	
    sql8=("update "+schema+"."+field+"_radio_pairs as t1"
         " inner join "+schema+"."+field+"_deconv as t2"
         " on t1.cid2=t2.id"
         " set t1.deconv2=t2.deconv;")
    print sql8,"\n"
    db.query(sql8)
	
# Perhaps check selection criteria with user before running this

    f1_f2_lt=2.1
    f1_f2_gt=1.0
    ang_sep_f1_f2_lt=10.0
    ang_sep_f1_f2_gt=2.0
	
    print "Radio Pair Selection Criteria \n"
    print " flux1/flux2         > and < : %f %f \n" % (f1_f2_gt,f1_f2_lt)
    print " ang_sep/sqrt(f1+f2) > and < : %f %f \n" % (ang_sep_f1_f2_gt,ang_sep_f1_f2_lt)
	
    sql9=("update "+schema+"."+field+"_radio_pairs"
         " set flag='rd'"
         " where flux1/flux2 > 1.0"
         " and flux1/flux2 < 2.1"
         " and ang_sep_arcsec/sqrt(flux1+flux2) > 2.0"
         " and ang_sep_arcsec/sqrt(flux1+flux2) < 10.0;")
    db.query(sql9)
	
# From the entries in field_radio_pairs
# add new entries into tables coords and radio_properties
# sum errors in quadrature

    sql11=("insert into "+schema+"."+field+"_coords "
          "  (id, ra, decl, ra_err, decl_err)"
          " select id,"
          "      ((select ra from "+schema+"."+field+"_coords where id=cid1)+(select ra from "+schema+"."+field+"_coords where id=cid2))/2 ,"
          "      ((select decl from "+schema+"."+field+"_coords where id=cid1)+(select decl from "+schema+"."+field+"_coords where id=cid2))/2,"
	      "      sqrt(power((select ra_err from "+schema+"."+field+"_coords where id=cid1),2)+power((select ra_err from "+schema+"."+field+"_coords where id=cid2),2)),"
	      "      sqrt(power((select decl_err from "+schema+"."+field+"_coords where id=cid1),2)+power((select decl_err from "+schema+"."+field+"_coords where id=cid2),2))"
          " from "+schema+"."+field+"_radio_pairs"
          " where flag='rd';")
    db.query(sql11)
	
    sql12=("insert into "+schema+"."+field+"_radio_properties"
          " (id,snr,rms,sp,sint,sp_err,sint_err)"
          " select id,"
          "       sqrt(power((select snr from "+schema+"."+field+"_radio_properties where id=cid1),2)+power((select snr from "+schema+"."+field+"_radio_properties where id=cid2),2)),"
	      "       sqrt(power((select rms from "+schema+"."+field+"_radio_properties where id=cid1),2)+power((select rms from "+schema+"."+field+"_radio_properties where id=cid2),2)),"
	      "      (flux1+flux2)/2,"
          "      ((select sint from "+schema+"."+field+"_radio_properties where id=cid1)+(select sint from "+schema+"."+field+"_radio_properties where id=cid2))/2,"
	      "      sqrt(power((select sp_err from "+schema+"."+field+"_radio_properties where id=cid1),2)+power((select sp_err from "+schema+"."+field+"_radio_properties where id=cid2),2)),"
	      "      sqrt(power((select sint_err from "+schema+"."+field+"_radio_properties where id=cid1),2)+power((select sint_err from "+schema+"."+field+"_radio_properties where id=cid2),2))"
          " from "+schema+"."+field+"_radio_pairs"
          " where flag='rd';")
    db.query(sql12)
		  
# Close connection to the database
    db.close()

    print "\nEnd of Radio Pair Search"


