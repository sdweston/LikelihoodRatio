#===========================================================================
#
# f_r.py
#
# Python script to query NVSS_GAMA12 mysql database to determine the
# f(r) for the likelihood ratio.
#
#===========================================================================
#
# S. Weston
# AUT University
# March 2013
#===========================================================================

def f_r():

    debug=0
	
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

# For GAMA12 : Radio SNR take as AVG(e_S1_4) ?

    SNR="0.94685"
	
# Find sigma_x_radio and sigma_y_radio

    sql2=("select avg(0.3*(MajAxis/"+SNR+")),avg(0.3*(MinAxis/"+SNR+")) "
           "FROM "+foreground_field+"."+foreground_field+"; ")
    db.query(sql2)
    r=db.use_result()
    rows=r.fetch_row()
    for row in rows:
        sigma_y_radio=float(row[0])
        sigma_x_radio=float(row[1])
        print "sigma_y_radio :",sigma_y_radio
        print "sigma_x_radio :",sigma_x_radio
 	db.close()
	
    sigma_radio=math.sqrt((sigma_x_radio)**2 + (sigma_y_radio)**2)
    print "Sigma Radio : ",sigma_radio
    if debug==1: print "\n"
    global sigma_radio
	
#    beam_maj=sigma_x_radio
#    beam_min=sigma_y_radio

			  
# Lets run a querry
# table4 for atlas.elais and atlas.cdfs are not consistent. Rename column dbmaj,dbmin to be majaxis,minaxis for both tables !

    db=_mysql.connect(host="localhost",user="atlas",passwd="atlas")

# Put sigma_radio into the working table, so don't have to re-run this each time

    sql_update_sigma=("update "+foreground_field+"."+foreground_field+"_working "
                      "set sigma="+str(sigma_radio)+" where field like '"+foreground_field+"';")
    if debug==1: print sql_update_sigma,"\n"
    db.query(sql_update_sigma)
	
# We are running against atlas_dr3 now, so need to join tables.
#    sql1=("select t1.cid, t1.swire_index_spitzer, t3.sint, t3.snr, t1.r_arcsec "


# note: theta is stored in radians
    sql1=("select t1.nvss_id, t1.supercosmos_id, t2.s1_4, t2.e_s1_4, t1.r_arcsec, t1.theta, "
          " t2.MajAxis, t2.MinAxis	"
          " from "+schema+"."+schema+"_matches as t1, "+foreground_field+"."+foreground_field+" as t2"
          " where t1.nvss_id=t2.id "
           "order by t1.nvss_id limit 1000000;")
		  

#		  if debug==1: print sql1,"\n" 
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

    rows=r.fetch_row(maxrows=500000)

# rows is a tuple, convert it to a list

#lst_rows=list(rows)

#print rows

    RADIUS=[]
    F_R=[]

    for row in rows:
        foreground_id=row[0]
        background_id=row[1]
        sint=float(row[2])
        serr=float(row[3])
        if row[4]==None:
            continue
        r=float(row[4])
        theta=float(row[5])
        beam_maj=float(row[6])
        beam_min=float(row[7])
    
        if debug==1: print foreground_id, background_id,sint,snr,r,theta
        sys.stdout.write('.')

# ACE - ancillary catalogue error, arcsec's

#        ACE=1.0
        ACE=0.0

# IRE - intrensic radio error, arcsec's
# Looking at http://www.cv.nrao.edu/nvss/paper.ps
# Take the larger rms error in ra,dec of 7"

#        IRE=7.0
        IRE=7.0

# In DR3 we have SNR !
        snr=sint/serr
		
#    print "SNR           : ",SNR

# Work out FWHM

# Calculate Sigma
#        Will need to allow for beam angle !
#        sigma_x=math.sqrt((0.6*(beam_min/snr))**2)
#        Check Ivison et al 2007, equation B7. should be 0.3 not 0.6
        sigma_y=(0.3*((beam_maj*math.sin(theta))/snr))**2 
#    print "Sigma X       : ",sigma_x

#        sigma_y=math.sqrt((0.6*(beam_maj/snr))**2 )
#        Check Ivison et al 2007, equation B7. should be 0.3 not 0.6
        sigma_x=(0.3*((beam_maj*math.cos(theta))/snr))**2 
#    print "Sigma Y       : ",sigma_y

#   sigma is the mean of sigma_x and sigma_y, or quadrature (in paper quadrature)
#        sigma=(sigma_x + sigma_y)/2
#       Do we need to sqrt here, when in f_r we square again. Save a calculation by not doing a sqrt.
#        sigma=math.sqrt(sigma_x + sigma_y + ACE**2 + IRE**2)
        sigma=(sigma_x + sigma_y + ACE**2 + IRE**2)
        if debug==1: print "Sigma         : ",sigma
 
		
# r is the radial distance between the radio source and the aux catalogue source
# r was returned from the sql in the matches table

# Calculate f(r)
#        By the formula it should be sigma**2, but see above why sqrt when we will sq again !
#        f_r=(1/(2*math.pi*sigma**2)) * math.exp(-r**2/2*sigma**2)
        part1=(1/(2*math.pi*sigma))
        part2=math.exp(-r**2/(2*sigma))
        part2a=r**2/(2*sigma)
        if debug==1: print part1, part2, part2a

        f_r=(1/(2*math.pi*sigma)) * math.exp(-r**2/(2*sigma))
        if debug==1: print f_r

        if f_r > 0.0 : 
           log10_f_r=math.log10(f_r)
           F_R.append(f_r)
           RADIUS.append(r)

        if debug==1: print "foreground_id   background_id sigma r f(r) : ",foreground_id,background_id,sigma,r,f_r
        if debug==1: print "\n"

#        print "    Update the database with the f(r) values"
		
# Populate new table with foreground_id,BS,SNR,f(r), or put back into matches table.
        db.query("update "+schema+"."+schema+"_matches set f_r=%s,snr=%s,sigma=%s where nvss_id='%s' \
                  and supercosmos_id='%s';" % (f_r, snr,sigma,foreground_id,background_id))

# End of do block

# Close connection to the database
    db.close()

    plt.plot(RADIUS, F_R,'k.')
    plot_title='NVSS GAMA12 f(r) vs r'
    plt.title(plot_title)
    plt.ylabel('f(r)')
    plt.xlabel('r (arcsec)')
#    plt.yscale('log')

    xlim_h=sr+1.0
    xlim_l=0.0
    plt.xlim(xlim_l,xlim_h)
#    plt.ylim(0.0,0.5)

    plot_fname='nvss_gama12_fr_vs_r.eps'
    fname=output_dir + plot_fname
    plt.savefig(fname,format="eps")
    plt.show()

    print "\nEnd of f(r)"


