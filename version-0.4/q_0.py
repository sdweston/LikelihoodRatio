#===========================================================================
#
# q_0.py
#
# Python script to query mysql database to determine the
# Q (D.J.B. Smith et al, 2010)
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def q_0():

    global Q
    print "\nStarting q0 calculation"

    execfile('constants.py')

# Constants for the non-radio survey area
# sqdeg - square degrees
# sqasec - square arc seconds
    
    sqasec=area_nr

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Count the number of radio sources
# So need to count the number of radio sources, but single count those marked as in a pair.

    sql1=("select "
          "(select count(*) from "+schema+"."+field+"_radio_properties) - "
          "(select count(*)/2 from "+schema+"."+field+"_radio_pairs where flag='rd') "
          "as Radio_Count; ")
    db.query(sql1)

    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
        print row[0]
        nrs=int(float(row[0]))

# Close connection to the database
    db.close()
	
# Count the number of xid's (matches)

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")	
    sql2=("select count(*) from "+schema+"."+field+"_matches;")
    db.query(sql2)

    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
        nxid=int(row[0])

# Close connection to the database
    db.close()
	
# Get Sum_m n(m)

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")	

    sql3=("select sum(n_m) from "+swire_schema+".n_m_lookup;")
    db.query(sql3)
    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
        sum_real_m=int(float(row[0]))

    db.close()

# =============================================================================
	
    print "Area square arcsec      : %f" % swire_sqsec
    print "Number of Radio Sources : %d" % nrs
    print "Number of XID's         : %d" % nxid
    print "Sum Real(m)             : %d" % sum_real_m

#==============================================================================
# Lets calculate Q_0

    q_0=(nxid - ((sum_real_m/swire_sqsec)*math.pi*math.pow(sr,2)*nrs)) / nrs
	
    if q_0 > 1.0: q_0=0.75
	
    print "Q0                      : %f" % q_0
	
    Q=q_0

    print "End or q_0\n"





