#===========================================================================
#
# r_m.py
#
# Python script to query mysql database to determine the
# real(m) for the likelihood ratio.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def real_m():

    global sum_real_m
    global nrs

    print "\nStarting real(m) calculations and db updates"

    execfile('constants.py')

# Constants for the non-radio survey area
# sqdeg - square degrees
# sqasec - square arc seconds
    
    sqasec=area_nr

# Connect to the local database with the atlas uid

#    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)

# Lets run a querry
    sql1=("SELECT count(distinct cid) FROM "+schema+"."+field+"_matches;")
    db.query(sql1)
    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
        nrs=int(row[0])
        print "    Number of Radio Sources : ",nrs

    sql2=("select total_m,n_m FROM "+swire_schema+".n_m_lookup;" )
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

#The other oddity is: Assuming these are numeric columns, why are they returned 
#as strings? Because MySQL returns all data as strings and expects you to 
#convert it yourself. This would be a real pain in the ass, but in fact, _mysql 
#can do this for you. (And MySQLdb does do this for you.) To have automatic 
#type conversion done, you need to create a type converter dictionary, and pass 
#this to connect() as the conv keyword parameter.

#   nrs=SELECT count(distinct elais_s1_cid) FROM elais_s1.matches;

    area=nrs * math.pi * math.pow(sr,2)
    print "Area              : %f " % area
    print "Back Ground Area  : %f " % atlas_sqasec

    total_m=[]
    n_m=[]
    real_m=[]
    background_m=[]
    print "    Total(m) n(m) r(m) backgrd"
    for row in rows:
    # a is total(m)
        a=float(row[0])
    # b is n(m)
        b=float(row[1])
    # r is 10"
    # c is real(m)

#   For 0.2_dr3 we had the following:
#      Assume a % of area lost due to contamination from forground stars
#      area_pct=0.96   

#        bck_grd=(b/(swire_sqsec * (1-area_pct))) * nrs * math.pi * math.pow(sr,2)
# try loosing the pct area lost correction
        bck_grd=(b/(swire_sqsec)) * nrs * math.pi * math.pow(sr,2)
        c= a - bck_grd
        total_m.append(a)
        n_m.append(b)
        print " %14.9f %14.9f %14.9f %14.9f" % (a, b, c, bck_grd)
        if c < 0:
           c=0
       
        sum_real_m=sum_real_m+c
        real_m.append(c)
        background_m.append(bck_grd)
        print " %14.9f %14.9f %14.9f %14.9f" % (a, b, c, bck_grd)

    print "    Sum real(m) : " ,sum_real_m

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)
    db.query("set autocommit=0;")

    print "    Update database with r(m) values"

    i=1
    for item in xrange(len(total_m)):
        r_m=real_m[item]
        b_m=background_m[item]
        db.query("update "+swire_schema+".n_m_lookup set real_m='%f', bckgrd_m='%f' \
                  where i='%d';" % ( r_m, b_m, i))
        db.commit()
        i=i+1

    db.commit()

# Close connection to the database
    db.close()

    print "End or real(m)\n"





