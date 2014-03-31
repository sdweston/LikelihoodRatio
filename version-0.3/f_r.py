#===========================================================================
#
# f_r.py
#
# Python script to query SWIRE_ES1 mysql database to determine the
# f(r) for the likelihood ratio.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def f_r():

#print math.pi

    print "Starting f(r) calculations and db updates"

# Connect to the local database with the atlas uid

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Lets run a querry
# table4 for atlas.elais and atlas.cdfs are not consistent. Rename column dbmaj,dbmin to be majaxis,minaxis for both tables !

# We are running against atlas_dr3 now, so need to join tables.
    sql1=("select t1.cid, t1.swire_index_spitzer, t2.deconv, t2.deconv, t3.sint, t3.snr, t1.r_arcsec "
          " from "+schema+"."+field+"_matches as t1, "+schema+"."+field+"_deconv as t2, "+schema+"."+field+"_radio_properties as t3 "
          " where t1.cid=t2.id "
          " and t1.cid=t3.id "
          "order by t1.cid;")
		  
    print sql1,"\n"  
    db.query(sql1)

#    db.query("select t1.cid,t2.swire_index_spitzer,t1.majaxis,t1.minaxis,t1.sint,t1.rms,t2.r_arcsec \
#          from %s.table4 as t1 left outer join %s.matches t2 \
#          on t2.cid=t1.cid \
#          order by t1.cid;" % (field,field))

		  
# store_result() returns the entire result set to the client immediately.
# The other is to use use_result(), which keeps the result set in the server 
#and sends it row-by-row when you fetch.

#r=db.store_result()
# ...or...
    r=db.use_result()

# fetch results, returning char we need float !

    rows=r.fetch_row(maxrows=5000)

# rows is a tuple, convert it to a list

#lst_rows=list(rows)

#print rows

    RADIUS=[]
    F_R=[]

    for row in rows:
        cid=row[0]
        index_spitzer=row[1]
        dbmaj=row[2]
        dbmin=row[3]
        sint=float(row[4])
        snr=float(row[5])
        if row[6]==None:
            continue
        r=float(row[6])
    
#    print cid, index_spitzer,dbmaj,dbmin,sint,rms,r
        sys.stdout.write('.')
    

# if dbmaj or dbmin are a string "None" then continue with next iteration

        if dbmaj==None:
            continue
        if dbmin==None:
            continue

# Need Sint & rms in same units muJy
# Sint is in mJy 10-3
# rms is in muJy 10-6

#    print "CID           : ",cid
        DBMAJ=float(dbmaj)
        DBMIN=float(dbmin)

# ACE - ancillary catalogue error, arcsec's

        ACE=0.1

# IRE - intrensic radio error, arcsec's

        IRE=0.6

# In DR3 we have SNR !
        SNR = snr
		
#    print "SNR           : ",SNR

# Work out FWHM

# Calculate Sigma

        sigma_x=math.sqrt((DBMAJ/(2*SNR))**2 + ACE**2 + IRE**2)
#    print "Sigma X       : ",sigma_x

        sigma_y=math.sqrt((DBMIN/(2*SNR))**2 + ACE**2 + IRE**2)
#    print "Sigma Y       : ",sigma_y

#   sigma is the mean of sigma_x and sigma_y
        sigma=(sigma_x + sigma_y)/2
#    print "Sigma         : ",sigma

# r is the radial distance between the radio source and the aux catalogue source
# r was returned from the sql in the matches table

# Calculate f(r)

        f_r=(1/(2*math.pi*sigma**2)) * math.exp(-r**2/2*sigma**2)
        F_R.append(f_r)
        RADIUS.append(r)
#    print "cid   index_spitzer   f(r) : ",cid,index_spitzer,f_r
#    print "\n"

#        print "    Update the database with the f(r) values"
		
# Populate new table with cid,BS,SNR,f(r), or put back into matches table.
        db.query("update "+schema+"."+field+"_matches set f_r=%s,snr=%s where cid='%s' \
                  and swire_index_spitzer='%s';" % (f_r, SNR, cid, index_spitzer))

# End of do block

# Close connection to the database
    db.close()

    plt.plot(RADIUS, F_R,'k.')
    plot_title='ATLAS ' +field+ ' f(r) vs r'
    plt.title(plot_title)
    plt.ylabel('f(r)')
    plt.xlabel('r (arcsec)')

    plot_fname='atlas_' +field+ '_fr_vs_r.ps'
    fname=output_dir + plot_fname
    plt.savefig(fname)
    plt.show()

    print "\nEnd of f(r)"


