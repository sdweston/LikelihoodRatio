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
# We now have two methods, so based on mdbs

    sql1=("select flux FROM "+schema+"."+field+"_matches where flux > 0;")

# Use SWIRE (cdfs/elais)_swire-sdss-cat-plus-full

    sql1a=("select t2.IRAC_3_6_micron_Flux_muJy "
           "FROM fusion.swire_"+field+" as t2, "+schema+"."+field+"_coords as t1 "
           "WHERE IRAC_3_6_micron_Flux_muJy > 0 "
           "and   pow((t1.ra-"+str(posn_offset_ra)+"-t2.RA_Spitzer)*cos(radians(t1.decl-"+str(posn_offset_dec)+")),2)+ "
           "      pow(t1.decl-"+str(posn_offset_dec)+"-t2.Dec_Spitzer,2) <= pow("+str(sr)+"/3600,2) "
           "limit 0,20000000;")

# Based on answer to which method of Magnitude Distribution to use
# run the appropriate database query

    if mdbs=='1':
       print sql1a,"\n"
       db.query(sql1a)
    else:
       print sql1,"\n"
       db.query(sql1)

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
#         print "%.4f" % a[0]
         b=math.log10(a[0])
#    print "%.4f" % b
         f_rows.append(b)

    (hist,bins)=numpy.histogram(f_rows,bins=nbins,range=[0.0,4.0])
#    print "hist"
#    print hist
#    print "bins"
#    print bins

    
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])/2
#
# Set axis limits so all are to the same scale
#
#    plt.ylim(0,500)
    plt.xlim(0,4)
    plt.bar(center, hist, align = 'center',width = width,linewidth=0)
    plot_title=field+' total(m)'
    plt.title(plot_title)
    plt.ylabel('total(f)')
    plt.xlabel('log10(f)')
    plot_fname='atlas_'+field+'_totalm_vs_log10f.eps'
    fname=output_dir + plot_fname
    plt.savefig(fname,format="eps")
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
        db.query("update "+schema+"."+field+"_n_m_lookup set total_m='%f' \
                  where i='%d';" % (total_m, i))
        db.commit()
        i=i+1

    db.commit()

# Close connection to the database
    db.close()
	
    print "End of total(m)\n"





