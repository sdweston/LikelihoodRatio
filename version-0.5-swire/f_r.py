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

	# Ivison et al 2007
# sigma = 0.6 x (FWHM / SNR)
# select avg(0.6*(FWHM/snr)) 
# FROM atlas_dr3.cdfs_radio_properties;

# Nick Seymour: For our purposes we can assume the PA is 0 deg. 
# It will negligibly affect our normalised errors which take into 
# account the shape of the beam.

# Find sigma_x_radio and sigma_y_radio

    sql2=("select avg(0.6*("+str(beam_maj)+"/snr)),avg(0.6*("+str(beam_min)+"/snr)) "
           "FROM atlas_dr3."+field+"_radio_properties; ")
    db.query(sql2)
    r=db.use_result()
    rows=r.fetch_row()
    for row in rows:
        sigma_y_radio=float(row[0])
        sigma_x_radio=float(row[1])
        print sigma_y_radio
        print sigma_x_radio
 	db.close()
	
    sigma_radio=math.sqrt((sigma_x_radio)**2 + (sigma_y_radio)**2)
    print "Sigma Radio : ",sigma_radio
    print "\n"
    global sigma_radio

			  
# Lets run a querry
# table4 for atlas.elais and atlas.cdfs are not consistent. Rename column dbmaj,dbmin to be majaxis,minaxis for both tables !

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Put sigma_radio into the working table, so don't have to re-run this each time

    sql_update_sigma=("update atlas_dr3.atlas_dr3_working "
                      "set sigma="+str(sigma_radio)+" where field like '"+field+"';")
    print sql_update_sigma,"\n"
    db.query(sql_update_sigma)
	
# We are running against atlas_dr3 now, so need to join tables.
#    sql1=("select t1.cid, t1.swire_index_spitzer, t3.sint, t3.snr, t1.r_arcsec "

# note: theta is stored in radians
    sql1=("select t1.cid, t1.swire_index_spitzer, t3.sp, t3.snr, t1.r_arcsec, t1.theta "
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
        sint=float(row[2])
        snr=float(row[3])
        if row[4]==None:
            continue
        r=float(row[4])
        theta=float(row[5])
    
#    print cid, index_spitzer,dbmaj,dbmin,sint,rms,r
        sys.stdout.write('.')

# ACE - ancillary catalogue error, arcsec's

        ACE=0.1

# IRE - intrensic radio error, arcsec's

        IRE=0.6

# In DR3 we have SNR !
        SNR = snr
		
#    print "SNR           : ",SNR

# Work out FWHM

# Calculate Sigma
#        Will need to allow for beam angle !
#        sigma_x=math.sqrt((0.6*(beam_min/snr))**2)
#        Check Ivison et al 2007, equation B7. should be 0.3 not 0.6
        sigma_x=((0.3*(beam_min/snr)*math.sin(theta))**2 )
#    print "Sigma X       : ",sigma_x

#        sigma_y=math.sqrt((0.6*(beam_maj/snr))**2 )
#        Check Ivison et al 2007, equation B7. should be 0.3 not 0.6
        sigma_y=((0.3*(beam_maj/snr)*math.cos(theta))**2 )
#    print "Sigma Y       : ",sigma_y

#   sigma is the mean of sigma_x and sigma_y, or quadrature (in paper quadrature)
#        sigma=(sigma_x + sigma_y)/2
#       Do we need to sqrt here, when in f_r we square again. Save a calculation by not doing a sqrt.
#        sigma=math.sqrt(sigma_x + sigma_y + ACE**2 + IRE**2)
        sigma=(sigma_x + sigma_y + ACE**2 + IRE**2)
#    print "Sigma         : ",sigma

# r is the radial distance between the radio source and the aux catalogue source
# r was returned from the sql in the matches table

# Calculate f(r)
#        By the formula it should be sigma**2, but see above why sqrt when we will sq again !
#        f_r=(1/(2*math.pi*sigma**2)) * math.exp(-r**2/2*sigma**2)
        f_r=(1/(2*math.pi*sigma)) * math.exp(-r**2/2*sigma)
        F_R.append(f_r)
        RADIUS.append(r)

#       print "cid   index_spitzer sigma r f(r) : ",cid,index_spitzer,sigma,r,f_r
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

    plt.xlim(0.0,10.0)
    plt.ylim(0.0,0.5)

    plot_fname='atlas_' +field+ '_fr_vs_r.eps'
    fname=output_dir + plot_fname
    plt.savefig(fname,format="eps")
    plt.show()

    print "\nEnd of f(r)"


