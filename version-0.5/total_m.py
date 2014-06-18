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
    execfile('get_nrs.py')

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
# We used to take the whole catalogue but now as Bonzini et al 2012 take the smaller search radius that
# we xid within.

#    sql1=("select flux FROM "+schema+"."+field+"_matches where flux > -8.0;")
	
    sql1a=("select t2.IRAC_3_6_micron_FLUX_MUJY "
           "FROM "+swire_schema+".swire as t2, "+schema+"."+field+"_coords as t1 "
           "WHERE IRAC_3_6_micron_FLUX_MUJY != -9.9 "
           "and   pow((t1.ra-"+str(posn_offset_ra)+"-t2.RA_SPITZER)*cos(t1.decl-"+str(posn_offset_dec)+"),2)+ "
           "      pow(t1.decl-"+str(posn_offset_dec)+"-t2.DEC_SPITZER,2) <= pow("+str(sr)+"/3600,2) "
           "limit 0,20000000;")
    print sql1a,"\n"
    db.query(sql1a)

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

    (hist,bins)=numpy.histogram(f_rows,bins=40,range=[0.0,4.0])
#    print "hist"
#    print hist
#    print "bins"
#    print bins

    
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])/2
    plt.bar(center, hist, align = 'center',width = width,linewidth=0)
    plot_title=field+' total(m)'
    plt.title(plot_title)
    plt.ylabel('total(f)')
    plt.xlabel('log10(f)')
    plot_fname='atlas_'+field+'_totalm_vs_log10f.ps'
    fname=output_dir + plot_fname
    plt.savefig(fname)
    plt.show()

# We have the binned data as a histogram, now insert it into table n_m_lookup

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")
    db.query("set autocommit=0;")

    print "    Update database with n(m) values"

    search_area=nrs*math.pi * math.pow(sr,2)
	
    i=1
    for item in xrange(len(hist)):
	
#   The total(m) needs to be a density function per unit arcsec^2
        total_m=hist[item]/search_area
        log10_f=bins[item]
        db.query("update "+swire_schema+".n_m_lookup set total_m='%f' \
                  where i='%d';" % (total_m, i))
        db.commit()
        i=i+1

    db.commit()

# Close connection to the database
    db.close()
	
    print "End of total(m)\n"





