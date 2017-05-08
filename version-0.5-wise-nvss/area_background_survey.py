#===========================================================================
#
# area_background_survey.py
#
# Python script to query mysql database to determine the
# area of the survey for a sub-set of the survey.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def area_none_radio_survey():

 
# We are using wise as background with 5amin circles centered on NVSS and SUMSS 
# sources.

    radius_centroids=5

# First count the number of NVSS and SUMSS sources

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)       

    sql1=("select count(*) from "+schema+".nvss_centroids;")
    print sql1,"\n"
    db.query(sql1)
          
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=1)

# rows is a tuple, convert it to a list

    for row in rows:
           num_nvss=row[0]

    print "NVSS  Sources : ",num_nvss
		   
# Close connection to the database
    db.close()

    db=_mysql.connect(host=db_host,user=db_user,passwd=db_passwd)       
    sql2=("select count(*) from "+schema+".sumss_centroids;")
    print sql2,"\n"
    db.query(sql2)
          

    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=1)

# rows is a tuple, convert it to a list

    for row in rows:
           num_sumss=row[0]


    # Close connection to the database
    db.close()

    print "SUMSS Sources : ",num_sumss

# Area = Number of sources (NVSS & SUMSS) * PIE * R^2

    area_arcmin=(int(num_nvss)+int(num_sumss))*math.pi*radius_centroids**2
	
    print "Area amin^2 : ",area_arcmin
	
    area_arcsec=area_arcmin*3600
	
    return area_arcmin,area_arcsec


