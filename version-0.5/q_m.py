#===========================================================================
#
# q_m.py
#
# Python script to query mysql database to determine the
# q(m) for the likelihood ratio.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def q_m():

    print "\nStarting q(m) calculations and db updates"

# Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# First determine sum[real(m_i)]
# I am wondering why q_m_swire_es1 had a fixed value: sum_real_m=810.785563462 ??

    sql1=("select sum(real_m) from "+swire_schema+".n_m_lookup;")
    db.query(sql1)

    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
        print row[0]
        sum_real_m=float(row[0])
    print "Sum of real_m : ",sum_real_m
	
    db.close()

	# Connect to the local database with the atlas uid

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)
	
# Lets run a querry

    sql2=("select real_m from "+swire_schema+".n_m_lookup;")
    db.query(sql2)

# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=0)

# Close connection to the database

    db.close()

#print rows

#The other oddity is: Assuming these are numeric columns, why are they returned 
#as strings? Because MySQL returns all data as strings and expects you to 
#convert it yourself. This would be a real pain in the ass, but in fact, _mysql 
#can do this for you. (And MySQLdb does do this for you.) To have automatic 
#type conversion done, you need to create a type converter dictionary, and pass 
#this to connect() as the conv keyword parameter.

# what to do when sum_real_m=0.0, can't have divide by Zero.
# Take lowest non-zero value / 2

    q_m=[]
    for row in rows:
        a=float(row[0])
        print a, sum_real_m, Q
        b=(a / sum_real_m ) * Q
#        print "q(m) ",b
        q_m.append(b)

# insert q(m) into the lookup table

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

    db.query("set autocommit=0;")
    
    print "    Update database with q(m) values"
	
    i=1
    for item in xrange(len(q_m)):
#        print item
        db.query("update %s.n_m_lookup set q_m='%f' \
                  where i='%d';" % (swire_schema, q_m[item], i))
        db.commit()
        i=i+1

    db.commit()

# Close connection to the database
    db.close()

    print "End of q(m)\n"





