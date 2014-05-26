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

# Lets run a querry to find the number of radio sources.

    sql1=("SELECT count(distinct cid) FROM "+schema+"."+field+"_matches;")
    db.query(sql1)
    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
        nrs=int(row[0])
        print "    Number of Radio Sources : ",nrs

# Have to allow for over-blended objects from atlas for number of radio sources NRM
#
# First how many overblended objects - NOB
# SELECT count(*) FROM atlas_dr3.elais_coords
# where length(id) > 6;

    sql1a=("SELECT count(*) FROM "+schema+"."+field+"_matches where length(cid) > 6;")
    db.query(sql1a)
    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
        nob=int(row[0])
        print "    Number of over blended components : ",nob
#
# Second group these to once source - NS
# select count(*)
# from
# (SELECT count(*) FROM atlas_dr3.elais_coords
# where length(id) > 6
# group by substr(id,1,6)) as a1;
#

    sql1b=("SELECT count(*) FROM ( select count(*) from "+schema+"."+field+"_matches where length(cid) > 6 group by substr(cid,1,6)) as a1;")
    db.query(sql1b)
    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
        ns=int(row[0])
        print "    Number of blended sources : ",ns

# True_NRS=NRS - NOB + NS		
    nrs=nrs-nob+ns
	
# Find the number of background ir sources between R_s and R_100, 10 <= r <= 100
# select count(*)
# from
# (select t1.id,
#       t2.index_spitzer,
#       t2.IRAC_3_6_micron_FLUX_MUJY, 
#       sqrt(pow((t1.ra-t2.RA_SPITZER)*cos(t1.decl),2)+pow(t1.decl-t2.DEC_SPITZER,2))*3600 as "angsep arcsec"
# FROM swire_cdfs.swire as t2, atlas_dr3.cdfs_coords as t1
# where IRAC_3_6_micron_FLUX_MUJY != -9.9
# and   pow((t1.ra-t2.RA_SPITZER)*cos(t1.decl),2)+
#      pow(t1.decl-t2.DEC_SPITZER,2) >= pow("+str(sr)+"/3600,2)
# and   pow((t1.ra-t2.RA_SPITZER)*cos(t1.decl),2)+
#       pow(t1.decl-t2.DEC_SPITZER,2) <= pow("+str(sr_out)+"/3600,2)
# limit 0,20000000) as a1;
		
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

# b = ir_density, script to find all ir sources within 100 seconds of a radio source.

    search_area=(nrs*math.pi * math.pow(sr_out,2))-(nrs*math.pi * math.pow(sr,2))
		
#        bck_grd=(b/(swire_sqsec)) * nrs * math.pi * math.pow(sr,2)
#       NIR is defined in n_m.py, so hard coding here for testing. 
#       cdfs nir = 423621
#        nir=423621

    if field == 'cdfs':
       nir=423621
    else:
       nir=223530

    print "Search Area : ",search_area
    print "NIR         : ",nir
    print "NRS         : ",nrs
	
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
#
# swire area = nrs * pi * r(100 sec) ** 2
	
        bck_grd=(nir/(search_area)) * nrs * math.pi * math.pow(sr,2)
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





