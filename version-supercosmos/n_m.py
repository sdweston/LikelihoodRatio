#===========================================================================
#
# n_m.py
#
# Python script to query SWIRE_ES1 mysql database to determine the
# n(m) for the likelihood ratio.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def n_m():

    global nir

    print "\nStarting n(m) calculations and db updates"

    execfile('constants.py')
    execfile('get_nrs.py')
    
# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
#    print "limits : ",swire_ra1,swire_ra2,swire_dec1,swire_dec2
    print "\n DB Schemas : ",schema

    sql1=("select B_J FROM supercosmos_gama12.supercosmos_gama12 "
          " where B_J > 0 "
          " and RA_2000 > "+str(sc_ra_min)+" and RA_2000 < "+str(sc_ra_max)+
          " and Dec_2000 > "+str(sc_dec_min)+" and Dec_2000 < "+str(sc_dec_max)+";")
    print sql1,"\n"
 
	
# Version 0.5, use a 100" search radius around each radio source. Exclude a smaller search radius when looking for 
# candidates. So need to take area between SR and 100". This is going to be intensive searching.
# Also need to exclude over-blended radio components and treat as one radio source.

    sql1a=("select t2.B_J "
           "FROM supercosmos_gama12.supercosmos_gama12 as t2, nvss_gama12.nvss_gama12 as t1 "
           "WHERE t2.B_J > 0 "
           "and   pow((t1.ra_2000-t2.RA_2000)*cos(radians(t1.decl_2000)),2)+ "
           "      pow(t1.decl_2000-t2.Dec_2000,2) >= pow("+str(sr)+"/3600,2) "
           "and   pow((t1.ra_2000-t2.RA_2000)*cos(radians(t1.decl_2000)),2)+ "
           "      pow(t1.decl_2000-t2.Dec_2000,2) <= pow("+str(sr_out)+"/3600,2) "
           "limit 0,20000000;")
   
# Note limit above in sql, mysql is usualy set to only retrieve 1000 rows. We have large 100's of thousands of entrys so
# need a bigger limit to get all records !
# 18446744073709551615 isn't just some number though; it's the max value of a bigint
# Is this a limitation of mysql when we get to v.v.large datasets for XID ?? Well thats 1.8 x 10^19.

# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

    if mdbs=='1':
       print sql1a,"\n"
       print "This is going to take some time ! \n"
       db.query(sql1a)
    else:
       print sql1,"\n"
       db.query(sql1)


#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=0)

# Lets count how many sources we have from the matching catalogue, in this case IR

    nir=0   
    for row in rows:
        nir += 1
    	
    print "    Number of optical sources : ",nir
	
# Put sigma_radio into the working table, so don't have to re-run this each time

    sql_update_nir=("update "+foreground_field+"."+foreground_field+"_working "
                      "set nir="+str(nir)+" where field like '"+foreground_field+"';")
    print sql_update_nir,"\n"
    db.query(sql_update_nir)

# Close connection to the database

    db.close()

	
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

#   a = B_J Photographic Magnitude
        a=map(float,row)
#
#   Magnitude is logrithmic
#        b=math.log10(a[0])
        b=a[0]
#        print "Flux %4.8f Log10_Flux %4.8f " % (a[0], b)
        f_rows.append(b)

#    (hist,bins)=numpy.histogram(f_rows,bins=60,range=[-1.0,5.0])
#   Min and Max for B_J is 6.373 - 22.993
    (hist,bins)=numpy.histogram(f_rows,bins=40,range=[6.0,23.0])
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])/2
#plt.yscale('log')
#plt.xscale('log')
#    plt.ylim(0,25000)
    plt.bar(center, hist, align = 'center',width = width,linewidth=0)
    plot_title=schema+' N(m)'
    plt.title(plot_title)
    plt.ylabel('n(B_J)')
    plt.xlabel('B_J')
    plot_fname=schema+'_nf_vs_B_J.eps'
    fname=output_dir + plot_fname
    plt.savefig(fname,format="eps")
    plt.show()
    
# We have the binned data as a histogram, now insert it into table n_m_lookup

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
    db.query("set autocommit=0;")

# first is the lookup table empty, if yes then use insert if no then use update
    sql2=("select count(*) from "+schema+"."+schema+"_n_m_lookup;")
    db.query(sql2)
	
    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
	    r_count=int(row[0])
	    
# If the row count from above is zero then insert into the db table, if row count is > 0 then update
    print "    Update database with n(m) values"
 	
#    print nrs, sr_out,sr

# Search area dependant on method of magnitude distribution of background sources:

    if mdbs=='1':
       search_area=nrs *(math.pi * math.pow(sr_out,2) - math.pi * math.pow(sr,2))
    else:
	   search_area=area_nvss_sqdeg
		
    print "Search Area : ",search_area
	
    i=1
    for item in xrange(len(hist)):

#   The n(m) needs to be a density function per unit arcsec^2
        n_m=hist[item]/search_area

#        print " n_m md/area arcsec^2 : %14.9f %14.9f" % (hist[item], n_m) 
        log10_f=bins[item]
#       Update the database with the n(m) values	
        if r_count == 0:	
           sql3=("insert into "+schema+"."+schema+"_n_m_lookup(i,n_m,log10_f,md) values ('"+str(i)+"','"+str(n_m)+"','"+str(log10_f)+"','"+str(hist[item])+"');")
           db.query(sql3)
        else:
           sql3=("update "+schema+"."+schema+"_n_m_lookup set n_m="+str(n_m)+", log10_f="+str(log10_f)+", md="+str(hist[item])+" where i="+str(i)+";")
           db.query(sql3)
        db.commit()
        i=i+1

    db.commit()

# Close connection to the database
    db.close()

    print "End of n(m)\n"





