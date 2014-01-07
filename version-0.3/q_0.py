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
	
    db.query("select count(*) \
	     FROM %s.table4;" % (field))

    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
        nrs=int(row[0])

# Close connection to the database
    db.close()
	
# Count the number of xid's (matches)

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")	
    db.query("select count(*) \
	     FROM %s.matches;" % (field))

    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
        nxid=int(row[0])

# Close connection to the database
    db.close()
	
# Get Sum_m n(m)

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")	

    db.query("select sum(n_m) from %s.n_m_lookup;" % (swire_schema))
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
	
    print "Q0                      : %f" % q_0
	
    Q=q_0

    print "End or q_0\n"





