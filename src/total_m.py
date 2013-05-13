#===========================================================================
#
# total_m.py
#
# Python script to query mysql database to determine the
# total(m) for the likelihood ratio.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def total_m():

    print "\nStarting total(m) calculations and db updates"

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry

    db.query("select flux FROM elais_s1.matches where flux > -8.0;")

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

# rows is a tuple, convert it to a list

    lst_rows=list(rows)

#mag=[]
#numpy.histogram(rows,bins=50)

# fetch_row paramaters, maxrows and how

#The other oddity is: Assuming these are numeric columns, why are they returned 
#as strings? Because MySQL returns all data as strings and expects you to 
#convert it yourself. This would be a real pain in the ass, but in fact, _mysql 
#can do this for you. (And MySQLdb does do this for you.) To have automatic 
#type conversion done, you need to create a type converter dictionary, and pass 
#this to connect() as the conv keyword parameter.

    f_rows=[]
    for row in lst_rows:
         a=map(float,row)
#    print "%.4f" % a[0]
         b=math.log10(a[0])
#    print "%.4f" % b
         f_rows.append(b)

    (hist,bins)=numpy.histogram(f_rows,bins=60,range=[-1.0,5.0])
#    print "hist"
#    print hist
#    print "bins"
#    print bins

# We have the binned data as a histogram, now insert it into table n_m_lookup

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
    db.query("set autocommit=0;")

    print "    Update database with n(m) values"
	
    i=1
    for item in xrange(len(hist)):
        total_m=hist[item]
        log10_f=bins[item]
        db.query("update swire_es1.n_m_lookup set total_m='%f' \
                  where i='%d';" % (total_m, i))
        db.commit()
        i=i+1

    db.commit()

# Close connection to the database
    db.close()

    print "End of total(m)\n"





