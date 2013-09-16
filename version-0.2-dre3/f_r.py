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
# for ATLAS DR3 this is table atlasdr3_fullcmpcat and the columns are different !
#     SNR        signal-to-noise ratio of raw dectection
#     DECONV     Deconvolved angular size (arcsec)
#     DECONV_ERR Error in deconvolved angular size (arcsec)
#     

    db.query("select t1.cid,t2.swire_index_spitzer,t1.snr,t1.ra_err,t1.dec_err,t2.r_arcsec \
          from %s.atlasdr3_fullcmpcat as t1, %s.matches as t2 \
          where t2.cid=t1.cid;" % (field,field))

		  
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

#    print rows

    RADIUS=[]
    F_R=[]

    for row in rows:
#        print row[0],row[1],row[2],row[3],row[4],row[5]
        cid=row[0]
        index_spitzer=row[1]
        snr=float(row[2])
        ra_err=float(row[3])
        dec_err=float(row[4])
        r=float(row[5])
    
#    print cid, index_spitzer,dbmaj,dbmin,sint,rms,r
        sys.stdout.write('.')
    
# ACE - ancillary catalogue error, arcsec's

        ACE=0.1

# IRE - intrensic radio error, arcsec's

        IRE=0.6

# Calculate Sigma

        sigma_x=math.sqrt((ra_err/(2*snr))**2 + ACE**2 + IRE**2)
#    print "Sigma X       : ",sigma_x

        sigma_y=math.sqrt((dec_err/(2*snr))**2 + ACE**2 + IRE**2)
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
        db.query("update %s.matches set f_r=%s,snr=%s where cid='%s' \
                  and swire_index_spitzer='%s';" % (field, f_r, snr, cid, index_spitzer))

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


