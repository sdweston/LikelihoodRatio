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
    execfile('get_nir.py')

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
#    nrs=nrs-nob+ns
# No longer valid with latest ATLAS DR3.
	
# Find the number of background ir sources between R_s and R_100, 10 <= r <= 100
# select count(*)
# from
# (select t1.id,
#       t2.index_spitzer,
#       t2.IRAC_3_6_micron_FLUX_MUJY, 
#       sqrt(pow((t1.ra-t2.RA_SPITZER)*cos(radians(t1.decl)),2)+pow(t1.decl-t2.DEC_SPITZER,2))*3600 as "angsep arcsec"
# FROM swire_cdfs.swire as t2, atlas_dr3.cdfs_coords as t1
# where IRAC_3_6_micron_FLUX_MUJY != -9.9
# and   pow((t1.ra-t2.RA_SPITZER)*cos(radians(t1.decl)),2)+
#      pow(t1.decl-t2.DEC_SPITZER,2) >= pow("+str(sr)+"/3600,2)
# and   pow((t1.ra-t2.RA_SPITZER)*cos(radians(t1.decl)),2)+
#       pow(t1.decl-t2.DEC_SPITZER,2) <= pow("+str(sr_out)+"/3600,2)
# limit 0,20000000) as a1;
		
    sql2=("select total_m,n_m FROM "+schema+"."+field+"_n_m_lookup;" )
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
# This is for Magnitude Distribution of Background Sources - Method 1 - search radii
# what about method 2 ?

    search_area=(nrs*math.pi * math.pow(sr_out,2))-(nrs*math.pi * math.pow(sr,2))
		
#        bck_grd=(b/(swire_sqsec)) * nrs * math.pi * math.pow(sr,2)
#       NIR is defined in n_m.py

    print "Search Area : ",search_area
    print "NIR         : ",nir
    print "NRS         : ",nrs
	
    total_m=[]
    n_m=[]
    real_m=[]
    background_m=[]
    print "    r(m)           Total(m)       n(m)"
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
	
        c= a - b
        total_m.append(a)
        n_m.append(b)
        print " %14.9f %14.9f %14.9f " % (c, a, b)
        if c < 0:
           c=0
       
        sum_real_m=sum_real_m+c
        real_m.append(c)
#        print " %14.9f %14.9f %14.9f " % (c, a, b)

    print "    Sum real(m) : " ,sum_real_m

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)
    db.query("set autocommit=0;")

    print "    Update database with r(m) values"

    i=1
    for item in xrange(len(total_m)):
        r_m=real_m[item]
        sql_update=("update "+schema+"."+field+"_n_m_lookup set real_m='%f' \
                  where i='%d';" % ( r_m, i))
        print sql_update
        db.query("update "+schema+"."+field+"_n_m_lookup set real_m='%f' \
                  where i='%d';" % ( r_m, i))
        db.commit()
        i=i+1

    db.commit()

# Close connection to the database
    db.close()

# From Steve & Loretta, REAL_M can't be 0. 
# So find the zero values and set them to be 
# 1/2 of the lowest non-zero value.
#
# Next idea make it n(m) * const as this affects selection of low m ir sources
# const=min(real_m)/min(n_m)

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
	
    sql_real_m_min=("select min(real_m) from "+schema+"."+field+"_n_m_lookup "
                    "where real_m > 0.0 and i < 10;")
	
    print sql_real_m_min
    db.query(sql_real_m_min)
	
    r=db.use_result()

    rows=r.fetch_row(maxrows=0)
    lst_rows=list(rows)
    for row in lst_rows:
        real_m_min=row[0]
        print "real(m) min : ",real_m_min

    sql_real_n_min=("select min(n_m) from "+schema+"."+field+"_n_m_lookup "
                    "where real_m ="+real_m_min+";")
	
    print sql_real_n_min
    db.query(sql_real_n_min)
	
    r=db.use_result()

    rows=r.fetch_row(maxrows=0)
    lst_rows=list(rows)
    for row in lst_rows:
        n_m_min=row[0]
        print "n(m)    min : ",n_m_min
    
    const=float(real_m_min)/float(n_m_min)
    print     "const       : ",const

    sql_n_m=("select n_m from "+schema+"."+field+"_n_m_lookup "
                    "where real_m = 0.0 and i < 10;")
	
    print sql_n_m
    db.query(sql_n_m)
	
    r=db.use_result()

    rows=r.fetch_row(maxrows=0)
    lst_rows=list(rows)
    for row in lst_rows:
        n_m=row[0]
        print "n(m)        : ",n_m

        new_real_m=float(n_m)*const
	
        sql_real_m_update=("update "+schema+"."+field+"_n_m_lookup "
                       " set real_m="+str(new_real_m)+ 
                       " where real_m=0.0 and n_m="+n_m+" and i < 10;")

        db.query(sql_real_m_update)

# Repeat for upper end
# Next idea make it n(m) * const as this affects selection of low m ir sources
# const=min(real_m)/min(n_m)

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
	
    sql_real_m_min=("select min(real_m) from "+schema+"."+field+"_n_m_lookup "
                    "where real_m > 0.0 and i > 10;")
	
    print sql_real_m_min
    db.query(sql_real_m_min)
	
    r=db.use_result()

    rows=r.fetch_row(maxrows=0)
    lst_rows=list(rows)
    for row in lst_rows:
        real_m_min=row[0]
        print "real(m) min : ",real_m_min

    sql_real_n_min=("select min(n_m) from "+schema+"."+field+"_n_m_lookup "
                    "where real_m ="+real_m_min+";")
	
    print sql_real_n_min
    db.query(sql_real_n_min)
	
    r=db.use_result()

    rows=r.fetch_row(maxrows=0)
    lst_rows=list(rows)
    for row in lst_rows:
        n_m_min=row[0]
        print "n(m)    min : ",n_m_min
    
    const=float(real_m_min)/float(n_m_min)
    print     "const       : ",const

    sql_n_m=("select n_m from "+schema+"."+field+"_n_m_lookup "
                    "where real_m = 0.0 and i > 10;")
	
    print sql_n_m
    db.query(sql_n_m)
	
    r=db.use_result()

    rows=r.fetch_row(maxrows=0)
    lst_rows=list(rows)
    for row in lst_rows:
        n_m=row[0]
        print "n(m)        : ",n_m

        new_real_m=float(n_m)*const
	
        sql_real_m_update=("update "+schema+"."+field+"_n_m_lookup "
                       " set real_m="+str(new_real_m)+ 
                       " where real_m=0.0 and n_m="+n_m+" and i > 10;")

        db.query(sql_real_m_update)

        
    db.close()

    print "End or real(m)\n"





