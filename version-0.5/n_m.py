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

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
#    print "limits : ",swire_ra1,swire_ra2,swire_dec1,swire_dec2
    print "\n DB Schemas : ",field,swire_schema

# Prior to V 0.4 we took the whole none-radio catalogue
    sql1=("select IRAC_3_6_micron_FLUX_MUJY FROM "+swire_schema+".swire "
          " where IRAC_3_6_micron_FLUX_MUJY != -9.9 "
          " and ra_spitzer > "+str(swire_ra1)+" and ra_spitzer < "+str(swire_ra2)+
          " and dec_spitzer > "+str(swire_dec1)+" and dec_spitzer < "+str(swire_dec2)+";")
#    print sql1,"\n"
#    db.query(sql1)
	
# Version 0.5, use a 100" search radius around each radio source. Exclude a smaller search radius when looking for 
# candidates. So need to take area between SR and 100". This is going to be intensive searching.
# Also need to exclude over-blended radio components and treat as one radio source.

# 26/5/2014 : Allow for catalogue position offset. posn_offset_ra, posn_offset_dec

    sql1a=("select t2.IRAC_3_6_micron_FLUX_MUJY "
           "FROM "+swire_schema+".swire as t2, "+schema+"."+field+"_coords as t1 "
           "WHERE IRAC_3_6_micron_FLUX_MUJY != -9.9 "
           "and   pow((t1.ra-"+str(posn_offset_ra)+"-t2.RA_SPITZER)*cos(t1.decl-"+str(posn_offset_dec)+"),2)+ "
           "      pow(t1.decl-"+str(posn_offset_dec)+"-t2.DEC_SPITZER,2) >= pow("+str(sr)+"/3600,2) "
           "and   pow((t1.ra-"+str(posn_offset_ra)+"-t2.RA_SPITZER)*cos(t1.decl-"+str(posn_offset_dec)+"),2)+ "
           "      pow(t1.decl-"+str(posn_offset_dec)+"-t2.DEC_SPITZER,2) <= pow("+str(sr_out)+"/3600,2) "
           "limit 0,20000000;")
    print sql1a,"\n"
    db.query(sql1a)
	
# Note limit above in sql, mysql is usualy set to only retrieve 1000 rows. We have large 100's of thousands of entrys so
# need a bigger limit to get all records !
# 18446744073709551615 isn't just some number though; it's the max value of a bigint
# Is this a limitation of mysql when we get to v.v.large datasets for XID ?? Well thats 1.8 x 10^19.

# limits for elais_s1		 
#         and ra_spitzer > 8.0 and ra_spitzer < 9.5 ;" % (swire_schema))
		 
#         and dec_spitzer < -43.0 and dec_spitzer > -44.5;")

# limits for ecdfs
#        and ra_spitzer > 51.6 and ra_spitzer < 54.0 \
#         and dec_spitzer > -29.0 and dec_spitzer < -27.0;")

# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=0)

# Lets count how many sources we have from the matching catalogue, in this case IR

    nir=0   
    for row in rows:
        nir += 1
    	
    print "    Number of over IR sources : ",nir
	
# Put sigma_radio into the working table, so don't have to re-run this each time

    sql_update_nir=("update atlas_dr3.atlas_dr3_working "
                      "set nir="+str(nir)+" where field like '"+field+"';")
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

#   a = IRAC_3_6_micron_FLUX_MUJY
        a=map(float,row)
        b=math.log10(a[0])
#    print "Flux %4.8f Log10_Flux %4.8f " % (a[0], b)
        f_rows.append(b)

#    (hist,bins)=numpy.histogram(f_rows,bins=60,range=[-1.0,5.0])
    (hist,bins)=numpy.histogram(f_rows,bins=40,range=[0.0,4.0])
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])/2
#plt.yscale('log')
#plt.xscale('log')
    plt.bar(center, hist, align = 'center',width = width,linewidth=0)
    plot_title=field+' N(m)'
    plt.title(plot_title)
    plt.ylabel('n(f)')
    plt.xlabel('log10(f)')
    plot_fname='atlas_'+field+'_nf_vs_log10f.ps'
    fname=output_dir + plot_fname
    plt.savefig(fname)
    plt.show()
    
# We have the binned data as a histogram, now insert it into table n_m_lookup

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
    db.query("set autocommit=0;")

# first is the lookup table empty, if yes then use insert if no then use update
    sql2=("select count(*) from "+swire_schema+".n_m_lookup;")
    db.query(sql2)
	
    r=db.store_result()
    rows=r.fetch_row(maxrows=1)
    for row in rows:
	    r_count=int(row[0])
	    
# If the row count from above is zero then insert into the db table, if row count is > 0 then update
    print "    Update database with n(m) values"
 	
    i=1
    for item in xrange(len(hist)):
        n_m=hist[item]
#        print " n_m md/area arcsec^2 : %14.9f %14.9f" % (hist[item], n_m) 
        log10_f=bins[item]
#       Update the database with the n(m) values	
        if r_count == 0:	
           sql3=("insert into "+swire_schema+".n_m_lookup(i,n_m,log10_f,md) values ('"+str(i)+"','"+str(n_m)+"','"+str(log10_f)+"','"+str(hist[item])+"');")
           db.query(sql3)
        else:
           sql3=("update "+swire_schema+".n_m_lookup set n_m="+str(n_m)+", log10_f="+str(log10_f)+", md="+str(hist[item])+" where i="+str(i)+";")
           db.query(sql3)
        db.commit()
        i=i+1

    db.commit()

# Close connection to the database
    db.close()

    print "End of n(m)\n"





